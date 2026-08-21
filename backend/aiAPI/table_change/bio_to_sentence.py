import json

def bio_to_sentence_and_entities(file_path):
    # 初始化变量
    sentences = []  # 用于存储所有句子及其标注的实体
    current_sentence = []  # 当前句子的单词
    current_entities = []  # 当前句子的实体
    current_entity = []  # 当前实体的单词
    current_entity_type = None  # 当前实体的类型
    ttag = []  # 用于存储所有实体类型，允许重复
    tag_id_counter = 0  # 用于生成唯一的tag_id

    # 读取文件内容
    with open(file_path, 'r', encoding='utf-8') as file:
        for line in file:
            line = line.strip()
            if line:  # 如果不是空行
                parts = line.split()
                if len(parts) < 3:
                    continue  # 跳过格式不正确的行

                word, _, tag = parts

                # 提取单词部分
                current_sentence.append(word)

                # 处理实体标注
                if tag.startswith("B-"):
                    # 如果当前已经有实体，保存当前实体
                    if current_entity:
                        tag_id = f"tag_id{tag_id_counter}"
                        entity_text = " ".join(current_entity)
                        start = " ".join(current_sentence).find(entity_text)
                        end = start + len(entity_text)
                        current_entities.append({
                            "tag_id": tag_id,
                            "start": start,
                            "end": end,
                            "mark_content": entity_text
                        })
                        ttag.append({
                            "tag_id": tag_id,
                            "tag_name": current_entity_type
                        })
                        tag_id_counter += 1
                        current_entity = []
                    # 开始新的实体
                    current_entity_type = tag[2:]
                    current_entity.append(word)
                elif tag.startswith("I-"):
                    # 继续当前实体
                    current_entity.append(word)
                else:
                    # 非实体部分
                    if current_entity:
                        tag_id = f"tag_id{tag_id_counter}"
                        entity_text = " ".join(current_entity)
                        start = " ".join(current_sentence).find(entity_text)
                        end = start + len(entity_text)
                        current_entities.append({
                            "tag_id": tag_id,
                            "start": start,
                            "end": end,
                            "mark_content": entity_text
                        })
                        ttag.append({
                            "tag_id": tag_id,
                            "tag_name": current_entity_type
                        })
                        tag_id_counter += 1
                        current_entity = []
            else:  # 如果是空行，表示句子结束
                if current_sentence:
                    # 确保最后一个实体被保存
                    if current_entity:
                        tag_id = f"tag_id{tag_id_counter}"
                        entity_text = " ".join(current_entity)
                        start = " ".join(current_sentence).find(entity_text)
                        end = start + len(entity_text)
                        current_entities.append({
                            "tag_id": tag_id,
                            "start": start,
                            "end": end,
                            "mark_content": entity_text
                        })
                        ttag.append({
                            "tag_id": tag_id,
                            "tag_name": current_entity_type
                        })
                        tag_id_counter += 1
                        current_entity = []
                    sentences.append({
                        "text": " ".join(current_sentence),
                        "text_tag": current_entities
                    })
                    current_sentence = []
                    current_entities = []

        # 检查是否有剩余的句子
        if current_sentence:
            # 确保最后一个实体被保存
            if current_entity:
                tag_id = f"tag_id{tag_id_counter}"
                entity_text = " ".join(current_entity)
                start = " ".join(current_sentence).find(entity_text)
                end = start + len(entity_text)
                current_entities.append({
                    "tag_id": tag_id,
                    "start": start,
                    "end": end,
                    "mark_content": entity_text
                })
                ttag.append({
                    "tag_id": tag_id,
                    "tag_name": current_entity_type
                })
                tag_id_counter += 1
            sentences.append({
                "text": " ".join(current_sentence),
                "text_tag": current_entities
            })

    # 构建最终的JSON结构
    result = {
        "textList": sentences,
        "ttag": ttag  # 将列表转换为所需的格式
    }

    return result

# 使用示例
file_path = 'biotext.txt'  # 替换为你的标注文件路径
result = bio_to_sentence_and_entities(file_path)

# 将结果保存为JSON文件
output_file_path = 'entity_output2.json'
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

print(f"Processed content has been saved to {output_file_path}")