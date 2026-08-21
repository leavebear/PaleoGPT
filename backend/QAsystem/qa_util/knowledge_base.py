import json
import httpx
import asyncio
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from util.data_embedding import search_papers
import re



# 写了两个模式，一个是deepseek的深度思考模式，一个是不需要深度思考的模式，所以这个功能就可以不用了
def extract_answer(text):
    # 尝试匹配 </think> 标签之后的内容
    match = re.search(r"</think>\s*(.*)", text, re.DOTALL)
    if match:
        return match.group(1).strip()  # 返回 </think> 后的内容
    else:
        return text.strip()  # 如果没有 </think>，返回原始内容
    
async def async_search_papers(question, top_k=5, bm25_top_n =50, max_distance = 200):
    loop = asyncio.get_running_loop()
    return await loop.run_in_executor(None,lambda:search_papers(question, top_k, bm25_top_n, max_distance))

# 修改为两个模式，大模型返回深度思考过程或者不返回
# 发送http修改为异步
async def run_prompt_with_llm(prompt, is_think=False):
    if is_think:
        api_url = "http://192.168.148.10:8000/v1/chat/completions"
        data = {
            "model": "qwq-32B",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": 0.6
        }
    else:
        api_url = "http://192.168.148.10:8000/v1/completions"
        prompt_formatted = f"<|begin▁of▁sentence|><|User|>{prompt}<|Assistant|><think>\n</think>\n\n"
        data = {
            "model": "qwq-32B",
            "prompt": prompt_formatted,
            "temperature": 0.6,
            "max_tokens": 1000,
        }

    headers = {
        "Content-Type": "application/json"
    }

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(api_url, headers=headers, json=data, timeout=30)
            response.raise_for_status()
        except httpx.RequestError as exc:
            print(f"请求出错：{exc}")
            return None
        except httpx.HTTPStatusError as exc:
            print(f"HTTP错误状态码 {exc.response.status_code}：{exc}")
            return None

        response_data = response.json()
        if is_think:
            return response_data["choices"][0]["message"]["content"]
        else:
            response_text = response_data["choices"][0]["text"]
            return extract_answer(response_text)
        

async def get_answer_from_knowledge_base_stream(request):
    question = request["question"]
    information = request["information"]

    results = []

    for file in information:
        file_name = file.get("filename")
        file_content = file.get("content")
        segment_index = file.get("segment_index")

        results.append({
            "filename": file_name,
            "content": file_content,
            "segment_index": segment_index
        })


    # # 根据获取到的段落生成Prompt
    if not results:
        print("未找到相关段落，将生成一个无参考资料的Prompt。")
        prompt = (
            "你是一个古生物学领域的专家，请根据你的专业知识回答以下问题。\n"
            "### 问题：\n" + question + "\n\n"
            "⚠️ 注意：未找到相关的参考资料，以下回答仅基于你的已有知识。"
        )
    else:
        print("找到相关段落，生成带有参考资料的Prompt。")
        prompt = "你是一个古生物学领域的专家，请根据以下参考资料回答问题。\n"
        prompt += "### 问题：\n" + question + "\n\n"
        prompt += "### 参考资料：\n"
        
        for i, result in enumerate(results):
            prompt += f"【参考资料 {i+1} - 论文：{result['filename']} - 段落 {result['segment_index']}】\n"
            prompt += result['content'] + "\n\n"
        
        prompt += "请基于上述信息进行回答。如果相关资料无法提供完整信息，可以根据自身内部知识来回答，但是请在回答中明确说明。"

    
    api_url = "http://192.168.148.10:8000/v1/chat/completions"
    headers = {"Content-Type": "application/json"}
    data = {
        "model": "qwq-32B",
        "messages": [
            {
                "role": "user", 
                "content": prompt}
        ],
        "stream": True
    }
    # print(data)

    async with httpx.AsyncClient() as client:
        try:
            async with client.stream("POST", api_url, headers=headers, json=data) as response:
                if response.status_code != 200:
                    err_msg = f"HTTP {response.status_code} - {response.text}"
                    yield json.dumps({
                        "event": "status",
                        "status": "error", 
                        "message": err_msg
                        })
                    return
                
                async for line in response.aiter_lines():
                    line = line.strip()

                    if not line:
                        continue  # 跳过空行
                    
                    # 去掉SSE的data:前缀
                    if line.startswith("data:"):
                        line = line[5:].strip()

                    if line == "[DONE]":
                        # OpenAI 等接口的结束标志，退出循环
                        break

                    try:
                        json_data = json.loads(line)
                        content = json_data.get("choices", [{}])[0].get("delta", {}).get("content", "")
                        
                        if content:
                            yield json.dumps({
                                "event": "data", 
                                "content": content
                                })
                    except json.JSONDecodeError:
                        continue
                    
            yield json.dumps({
                "event": "status", 
                "status": "success"
                })
        except httpx.HTTPError as e:
            yield json.dumps({
                "event": "error", 
                "message": f"HTTP错误: {str(e)}"
                })
        except Exception as e:
            yield json.dumps({
                "event": "error", 
                "message": f"异常错误: {str(e)}"
                })

#get information

async def get_information(question, logger, k=8, user_context=None):
    
    # category = await classify_query(question)
    category = "Contextual"
    logger.info("分类已完成: "+ category)

    if category == "Factual":
        # Use the factual retrieval strategy for precise information
        results = await factual_retrieval_strategy(question, k, logger)
        logger.info("背景知识已搜索完毕")
    elif category == "Analytical":
        # Use the analytical retrieval strategy for comprehensive coverage
        results = await analytical_retrieval_strategy(question, k, logger)
        logger.info("背景知识已搜索完毕")
    elif category == "Opinion":
        # Use the opinion retrieval strategy for diverse perspectives
        results = await opinion_retrieval_strategy(question, k, logger)
        logger.info("背景知识已搜索完毕")
    elif category == "Contextual":
        # Use the contextual retrieval strategy, incorporating user context
        results = await contextual_retrieval_strategy(question, k, logger, user_context)
        logger.info("背景知识已搜索完毕")
    else:
        # Default to factual retrieval strategy if classification fails
        results = await factual_retrieval_strategy(question, k, logger)
        logger.info("背景知识已搜索完毕")

    return results  # Return the retrieved documents

""""
serch_papers_return:
    "filename": meta['filename'],
    "segment_index": meta['segment_index'],
    "content": meta['content'],
    "distances": float(distances[0][i])  # 转换为相似度
"""

async def classify_query(question):
    """
    Classify a query into one of four categories: Factual, Analytical, Opinion, or Contextual.
    
    Args:
        question (str): User query

    Returns:
        str: Query category
    """
    prompt = f"""
    你是一名擅长问题分类的专家。

    请将用户提出的问题精确地归类为以下四类之一：
    - Factual：查询具体、可验证的信息。
    - Analytical：需要全面分析或解释的问题。
    - Opinion：关于主观观点或涉及多种看法的问题。
    - Contextual：依赖用户特定上下文的问题。

    请只输出分类结果，如"Factual"，"Analytical"，"Opinion"或"Contextual。不要输出思考过程，只输出答案。

    请分类以下问题：{question}
    """

    category = await run_prompt_with_llm(prompt, False)
    return category


async def factual_retrieval_strategy(question, k, logger):
    """
    Retrieval strategy for factual queries focusing on precision.
    
    Args:
        query (str): User query
        vector_store (SimpleVectorStore): Vector store
        k (int): Number of documents to return
        
    Returns:
        List[Dict]: Retrieved documents
    """
    # Use LLM to enhance the query for better precision
    prompt = f"""
    你是一名擅长优化检索问题的专家。

    你的任务是将用户提出的事实类问题重新表述，使其更精确、更具体，以提升信息检索的效果。请关注关键实体及其之间的关系。

    请**仅输出**优化后的问题一个句子,如“优化后的问题” 保持与原问题相同的语言（中/英文）。

    原始问题：{question}
    """

    # Extract and print the enhanced query
    enhanced_question = await run_prompt_with_llm(prompt)
    match = re.search(r"优化后的问题：(.+)", enhanced_question)
    if match:
        enhanced_question = match.group(1)

    logger.info(f"问题优化完成: {enhanced_question}")
     

    # 和之前的方法大差不差，区别就是会先找一遍2k个文档，然后让大模型评分，再取前k个
    # Perform initial similarity search to retrieve documents
    initial_results = await async_search_papers(enhanced_question,k*2)
    logger.info("背景知识初步搜索完成")
    
    # Initialize a list to store ranked results
    ranked_results = []
    

    # Score and rank documents by relevance using LLM
    for doc in initial_results:
        relevance_score = await score_document_relevance(enhanced_question, doc["content"])
        if(relevance_score > 0):
            ranked_results.append({
                "filename": doc['filename'],
                "segment_index": doc['segment_index'],
                "content": doc['content'],
                "relevance_score": relevance_score
            })
            logger.info(f"此文档打分完成:{relevance_score}")
    
    # Sort the results by relevance score in descending order
    # print(f"Initial results: {ranked_results}")
    ranked_results.sort(key=lambda x: x["relevance_score"], reverse=True)

    
    # Return the top k results
    return ranked_results[:k]

async def analytical_retrieval_strategy(question, k, logger):
    """
    Retrieval strategy for analytical queries focusing on comprehensive coverage.
    
    Args:
        query (str): User query
        vector_store (SimpleVectorStore): Vector store
        k (int): Number of documents to return
        
    Returns:
        List[Dict]: Retrieved documents
    """
    
    prompt = f"""
    你是一名擅长拆解复杂问题的专家。

    请针对用户提出的分析类问题，生成能够从不同角度展开的子问题。这些子问题应涵盖主题的广度，有助于获取更全面的信息。

    请仅生成拆解的三个子问题，每行一个。不要包含任何其他的思考过程

    原始问题：{question}
    """
    
    # Extract and clean the sub-questions
    sub_questions = await run_prompt_with_llm(prompt,False)
    logger.info(f"子问题拆解完毕： {sub_questions}")

    #处理成结构化的子问题列表
    sub_questions = re.split(r'\d+\.\s*', sub_questions.strip())
    sub_questions = [q.strip() for q in sub_questions if q.strip()]
    
    # 根据子问题先找相关文档，每个子问题找2个相关文档
    # Retrieve documents for each sub-query
    all_results = []
    for sub_question in sub_questions:
        results = await async_search_papers(sub_question, k/2)
        all_results.extend(results)

    logger.info(f"背景知识初步搜索完成")
    
    # Ensure diversity by selecting from different sub-query results
    # Remove duplicates (same filename)
    unique_files = set()
    diverse_results = []
    
    for result in all_results:
        if result["filename"] not in unique_files:
            unique_files.add(result["filename"])
            diverse_results.append(result)
    
    # 如果筛选后文档还是小于k个,再根据主问题来找k个
    # If we need more results to reach k, add more from initial results
    if len(diverse_results) < k:
        # Direct retrieval for the main query
        main_results = await async_search_papers(question, k)
        
        for result in main_results:
            if result["filename"] not in unique_files and len(diverse_results) < k:
                unique_files.add(result["filename"])
                diverse_results.append(result)
    
    # Return the top k diverse results
    return diverse_results[:k]

async def opinion_retrieval_strategy(question, k, logger):
    """
    Retrieval strategy for opinion queries focusing on diverse perspectives.
    
    Args:
        query (str): User query
        vector_store (SimpleVectorStore): Vector store
        k (int): Number of documents to return
        
    Returns:
        List[Dict]: Retrieved documents
    """
    
    prompt = f"""
    你是一名擅长挖掘话题多元观点的专家。

    请针对以下问题，识别出人们可能持有的不同观点或立场，从多个角度进行思考。

    请生成恰好三个不同的观点角度，每行一个。

    待识别的问题：{question}
    """

    # Extract and clean the viewpoints
    viewpoints = await run_prompt_with_llm(prompt)

    #处理成结构化的观点列表
    viewpoints = re.split(r'\d+\.\s*', viewpoints.strip())
    viewpoints = [q.strip() for q in viewpoints if q.strip()]
    logger.info(f"观点问题列表已处理: {viewpoints}")

    
    # Retrieve documents representing each viewpoint
    all_results = []
    for viewpoint in viewpoints:
        # Combine the main query with the viewpoint
        combined_question = f"{question} {viewpoint}"
        print(combined_question)


        results = await async_search_papers(combined_question, k/2)
        
        # Mark results with the viewpoint they represent
        for result in results:
            result["viewpoint"] = viewpoint
        
        # Add the results to the list of all results
        all_results.extend(results)
    
    logger.info(f"背景知识初步搜索完成")

    # Select a diverse range of opinions
    # Ensure we get at least one document from each viewpoint if possible
    selected_results = []
    for viewpoint in viewpoints:
        # Filter documents by viewpoint
        viewpoint_docs = [r for r in all_results if r.get("viewpoint") == viewpoint]
        if viewpoint_docs:
            selected_results.append(viewpoint_docs[0])
    
    remaining_slots = k - len(selected_results)
    if remaining_slots > 0:
        # Sort remaining docs by distances
        remaining_docs = [r for r in all_results if r not in selected_results]
        remaining_docs.sort(key=lambda x: x["distances"], reverse=False)
        selected_results.extend(remaining_docs[:remaining_slots])
    
    # Return the top k results
    return selected_results[:k]

async def contextual_retrieval_strategy(question, k, logger, user_context=None):
    """
    Retrieval strategy for contextual queries integrating user context.
    
    Args:
        query (str): User query
        vector_store (SimpleVectorStore): Vector store
        k (int): Number of documents to return
        user_context (str): Additional user context
        
    Returns:
        List[Dict]: Retrieved documents
    """
    
    # If no user context provided, try to infer it from the query
    if not user_context:
        help_prompt = f"""
        你是一名擅长理解隐含语境的专家。

        请根据以下问题，推测其背后可能隐含但未明确说明的上下文信息。重点思考：哪些背景信息有助于更好地回答这个问题。

        请输出一段简要的语境描述。

        待推理的问题：{question}

        ⚠️ 请保持问题原有的语言风格，不要翻译问题内容。
        """

        
        # Generate the inferred context using the LLM

        user_context = await run_prompt_with_llm(help_prompt)
        # print(f"Inferred context: {user_context}")
    
    # Reformulate the query to incorporate context
    prompt = f"""
    你是一名擅长结合上下文改写问题的专家。

    请根据用户提出的问题和提供的背景信息，将原问题改写为更具体、语义更明确的问题，以便获取更相关的答案。

    请**只输出改写后的问题本体**，不要输出任何解释内容。

    原问题：{question}  
    背景信息：{user_context}

    请基于上述背景，重新组织问题内容：

    ⚠️ 请保持问题使用的原始语言风格，不要翻译问题内容。
    """

    # Generate the contextualized query using the LLM

    contextualized_query = await run_prompt_with_llm(prompt)
    logger.info(f"问题上下文补充完毕: {contextualized_query}")
    
    initial_results = await async_search_papers(contextualized_query, k*2)
    
    logger.info(f"背景知识初步搜索完成")
    # Rank documents considering both relevance and user context
    ranked_results = []
    
    for doc in initial_results:
        # Score document relevance considering the context
        context_relevance = await score_document_context_relevance(question, user_context, doc["content"])
        ranked_results.append({
            "filename": doc["filename"],
            "segment_index": doc["segment_index"],
            "content": doc["content"],
            "distances": doc["distances"],
            "context_relevance": context_relevance
        })

    
    # Sort by context relevance and return top k results
    ranked_results.sort(key=lambda x: x["context_relevance"], reverse=True)
    return ranked_results[:k]

async def score_document_relevance(question, document):
    """
    Score document relevance to a query using LLM.
    
    Args:
        query (str): User query
        document (str): Document text
        model (str): LLM model
        
    Returns:
        float: Relevance score from 0-10
    """
    doc_preview = document[:1500] + "..." if len(document) > 1500 else document
    
    prompt = f"""
    你是一名擅长评估文档与问题相关性的专家。

    请根据以下标准，在 0 到 10 的范围内对文档与问题的相关性进行评分：
    0 分：完全无关  
    10 分：完全符合，准确回答了问题

    请**仅返回一个 0 到 10 之间的数字分数**，不要输出任何解释说明。

    问题：{question}  
    文档内容预览：{doc_preview}  

    相关性评分（0-10）：
    """

    
    score_text = await run_prompt_with_llm(prompt)
    
    # Extract numeric score using regex
    match = re.search(r'(\d+(\.\d+)?)', score_text)
    if match:
        score = float(match.group(1))
        return min(10, max(0, score))  # Ensure score is within 0-10
    else:
        # Default score if extraction fails
        return 5.0

async def score_document_context_relevance(question, context, document):
    """
    Score document relevance considering both query and context.
    
    Args:
        query (str): User query
        context (str): User context
        document (str): Document text
        model (str): LLM model
        
    Returns:
        float: Relevance score from 0-10
    """
    doc_preview = document[:1500] + "..." if len(document) > 1500 else document

    # System prompt to instruct the model on how to rate relevance considering context
    prompt = f"""
    你是一名擅长结合上下文评估文档相关性的专家。

    请根据以下标准，在综合考虑提供的上下文后，对文档对问题的回答程度进行 0 到 10 的评分：
    0 分：完全无关  
    10 分：在给定上下文中完美回答了问题

    请**仅返回一个 0 到 10 之间的数字分数**，不要输出任何解释说明。

    问题：{question}  
    上下文：{context}  
    文档内容预览：{doc_preview}  

    结合上下文的相关性评分（0-10）：
    """

    
    # Generate response from the model
    score_text = await run_prompt_with_llm(prompt)
    
    # Extract numeric score using regex
    match = re.search(r'(\d+(\.\d+)?)', score_text)
    if match:
        score = float(match.group(1))
        return min(10, max(0, score))  # Ensure score is within 0-10
    else:
        # Default score if extraction fails
        return 5.0


async def main():
    # async for data in get_answer_from_knowledge_base_stream("hello"):
    #     print(data)
    # question = "你好"
    # results = await get_information(question)
    # print(results)

    prompt = "苏北南黄海盆地有哪些化石，在哪些地区"

    # # 深度思考（使用 /v1/chat/completions，返回 message.content）
    await opinion_retrieval_strategy(prompt,1)

    # response_think = await run_prompt_with_llm(prompt, is_think=True)

    # print(response_think)

    # # 不思考（使用 /v1/completions，返回 text）
    # response_no_think = await run_prompt_with_llm(prompt, is_think=False)

    # print(response_no_think)


if __name__ == "__main__":
    asyncio.run(main())


