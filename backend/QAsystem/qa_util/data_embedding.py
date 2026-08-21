import json
import os 
import faiss
import torch
import numpy as np
import re
from transformers import AutoTokenizer, AutoModel
from tqdm import tqdm
from rank_bm25 import BM25Okapi
import pickle

MODEL_PATH = '/home/jsj201-2/mount1/lihongjun/PaleoPRO/backend/QAsystem/model/bge-base-zh-v1.5' #中文模型 bert-base-chinese 新换的模型bge-base-zh-v1.5
DATA_DIR = '/home/jsj201-2/mount1/lihongjun/PaleoPRO/backend/QAsystem/docs'
PROCESSED_FILES_PATH = '/home/jsj201-2/mount1/lihongjun/PaleoPRO/backend/QAsystem/docs/processed_files.json'
BM25_INDEX_PATH = '/home/jsj201-2/mount1/lihongjun/PaleoPRO/backend/QAsystem/index/bm25_index.pkl'
BM25_CORPUS_PATH = '/home/jsj201-2/mount1/lihongjun/PaleoPRO/backend/QAsystem/index/bm25_corpus.pkl'
INDEX_PATH = '/home/jsj201-2/mount1/lihongjun/PaleoPRO/backend/QAsystem/index/faiss_index.bin'
METADATA_PATH = '/home/jsj201-2/mount1/lihongjun/PaleoPRO/backend/QAsystem/index/metadata.npy'

CHUNK_SIZE = 1000
OVERLAP_SIZE = 200

# ================== 初始化模型 ==================

torch.cuda.empty_cache()
tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH, local_files_only=True)
model = AutoModel.from_pretrained(MODEL_PATH, torch_dtype=torch.float16, local_files_only=True)  # 👈 使用float16
model.eval()
device = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')
if torch.cuda.device_count() > 1:
    model = torch.nn.DataParallel(model, device_ids=[0, 1])  # 使用GPU 0和GPU 1
model.to(device)


# ================== 工具函数 ==================

def load_processed_files():
    if os.path.exists(PROCESSED_FILES_PATH):
        with open(PROCESSED_FILES_PATH, 'r') as f:
            return set(json.load(f))
    return set()

def save_processed_files(processed_files):
    with open(PROCESSED_FILES_PATH, 'w') as f:
        json.dump(list(processed_files), f)

def load_papers(data_dir):
    papers = []
    filenames = []
    for filename in os.listdir(data_dir):
        if filename.endswith('.txt'):
            with open(os.path.join(data_dir, filename), 'r', encoding='utf-8') as f:
                papers.append(f.read())
                filenames.append(filename)
    return papers, filenames


# def paragraph_sentence_sliding_split(papers, filenames, window_size=CHUNK_SIZE, stride=OVERLAP_SIZE):
#     segments = []
#     segment_metadata = []

#     for i, paper in enumerate(papers):
#         paragraphs = [p.strip() for p in paper.split('\n') if p.strip()]

#         segment_index = 0

#         for para in paragraphs:
#             sentences = re.split(r'(?<=[。.!?])', para)
#             sentences = [s.strip() for s in sentences if s.strip()]

#             current_segment = ""
#             current_len = 0

#             for sent in sentences:
#                 sent_len = len(sent.split())
#                 if current_len + sent_len <= window_size:
#                     current_segment += sent
#                     current_len += sent_len
#                 else:
#                     segments.append(current_segment.strip())
#                     segment_metadata.append({
#                         'filename': filenames[i],
#                         'segment_index': segment_index,
#                         'content': current_segment.strip()
#                     })
#                     segment_index += 1

#                     # 计算重叠句子，保证上下文连续
#                     overlap_sentences = []
#                     overlap_len = 0
#                     for s in reversed(current_segment.split('。')[:-1]):
#                         s_len = len(s.split())
#                         if overlap_len + s_len > stride:
#                             break
#                         overlap_sentences.insert(0, s + '。')
#                         overlap_len += s_len
#                     current_segment = ''.join(overlap_sentences) + sent
#                     current_len = overlap_len + sent_len

#             if current_segment:
#                 segments.append(current_segment.strip())
#                 segment_metadata.append({
#                     'filename': filenames[i],
#                     'segment_index': segment_index,
#                     'content': current_segment.strip()
#                 })
#                 segment_index += 1

#     return segments, segment_metadata

def sentence_sliding_split(papers, filenames, window_size=CHUNK_SIZE, stride=OVERLAP_SIZE):
    segments = []
    segment_metadata = []

    for i, paper in enumerate(papers):
        # 统一处理换行为空格，避免句子被断裂
        paper_text = paper.replace('\n', ' ')
        # 更稳健地切句（避免括号/英文干扰）
        sentences = re.split(r'(?<=[。！？!?])(?!(?:[^()]*\)))', paper_text)
        sentences = [s.strip() for s in sentences if s.strip()]
        if not sentences:
            continue

        # 滑动窗口切分句子
        segment_index = 0
        start = 0
        while start < len(sentences):
            end = start
            current_len = 0
            while end < len(sentences) and current_len + len(sentences[end]) <= window_size:
                current_len += len(sentences[end])
                end += 1

            segment = ''.join(sentences[start:end])
            segments.append(segment)
            segment_metadata.append({
                'filename': filenames[i],
                'segment_index': segment_index,
                'content': segment
            })
            segment_index += 1
            start += stride  # 滑窗推进

    return segments, segment_metadata


# ================== bm25 ==================

def build_bm25_index(segments):
    tokenized_corpus = [seg.split() for seg in segments]
    bm25 = BM25Okapi(tokenized_corpus)
    with open(BM25_INDEX_PATH, 'wb') as f:
        pickle.dump(bm25, f)
    with open(BM25_CORPUS_PATH, 'wb') as f:
        pickle.dump(segments, f)
    print("📦 BM25 索引已保存")

def load_bm25_index():
    with open(BM25_INDEX_PATH, 'rb') as f:
        bm25 = pickle.load(f)
    with open(BM25_CORPUS_PATH, 'rb') as f:
        corpus = pickle.load(f)
    return bm25, corpus


# ================== embedding ==================   

def embed_batch(texts):
    inputs = tokenizer(texts, return_tensors="pt", truncation=True, padding=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy().astype("float32")
    torch.cuda.empty_cache()
    return embeddings

def embed_text(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True, max_length=512)
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state[:, 0, :].cpu().numpy().astype("float32")
    torch.cuda.empty_cache()  # 👈 清空 GPU 缓存
    return embeddings

def build_faiss_index(segments, metadata, append=False, batch_size=2):
    embedding_list = []
    for i in tqdm(range(0, len(segments), batch_size), desc="🔄 正在生成嵌入"):
        batch_texts = segments[i:i + batch_size]
        batch_embeddings = embed_batch(batch_texts)
        embedding_list.append(batch_embeddings)

    embeddings = np.vstack(embedding_list)
    d = embeddings.shape[1]  # 向量维度

    if append and os.path.exists(INDEX_PATH):
        index = faiss.read_index(INDEX_PATH)
        existing_metadata = np.load(METADATA_PATH, allow_pickle=True).tolist()
        index.add(embeddings)
        metadata = existing_metadata + metadata
    else:
        index = faiss.IndexFlatL2(d)
        index.add(embeddings)

    faiss.write_index(index, INDEX_PATH)
    np.save(METADATA_PATH, np.array(metadata, dtype=object))



def load_index_and_metadata():
    print("📥 加载 FAISS 索引和元数据...")
    index = faiss.read_index(INDEX_PATH)
    metadata = np.load(METADATA_PATH, allow_pickle=True)
    metadata = metadata.tolist()
    return index, metadata




def search_papers(question, top_k=5, bm25_top_n =50, max_distance = 200):
    index, metadata = load_index_and_metadata()
    bm25, corpus = load_bm25_index()
    
    # ---------- Step 1: BM25 粗筛 ----------
    print("🔍 使用 BM25 进行粗筛...")
    tokenized_query = question.split()
    bm25_scores = bm25.get_scores(tokenized_query)
    top_n_indices = np.argsort(bm25_scores)[::-1][:bm25_top_n]

    # ---------- Step 2: 用 FAISS 精排 ----------
    selected_segments = [corpus[i] for i in top_n_indices]
    selected_metadata = [metadata[i] for i in top_n_indices]

    print("🔍 使用向量模型进行精排...")
    embedding = embed_text(question)
    faiss_index = faiss.IndexFlatL2(embedding.shape[1])
    batch_embeddings = []

    for seg in selected_segments:
        emb = embed_text(seg)
        batch_embeddings.append(emb[0])

    batch_embeddings = np.vstack(batch_embeddings).astype('float32')
    faiss_index.add(batch_embeddings)
    top_k = int(top_k)
    distances, indices = faiss_index.search(embedding, top_k)

    # ---------- Step 3: 返回结果 ----------
    print("🔍 搜索完毕，正在返回结果...")
    results = []
    for i, idx in enumerate(indices[0]):
        if idx == -1 or distances[0][i] > max_distance:
            continue
        meta = selected_metadata[idx]
        results.append({
            "filename": meta['filename'],
            "segment_index": meta['segment_index'],
            "content": meta['content'],
            "distances": float(distances[0][i])
        })
    return results


def main():
    all_papers, all_filenames = load_papers(DATA_DIR)
    processed_files = load_processed_files()
    new_filenames = [fn for fn in all_filenames if fn not in processed_files]
    if not new_filenames:
        print("✅ 没有新论文，无需更新")
        return

    new_papers = [all_papers[i] for i, fn in enumerate(all_filenames) if fn in new_filenames]
    new_segments, new_metadata = sentence_sliding_split(new_papers, new_filenames)
    build_faiss_index(new_segments, new_metadata, append=True)

    # 重新构建 BM25 全量索引
    all_segments, _ = sentence_sliding_split(all_papers, all_filenames)
    build_bm25_index(all_segments)

    processed_files.update(new_filenames)
    save_processed_files(processed_files)
    print("✅ 新论文已更新（包含 BM25 索引）")




if __name__ == "__main__":
    # if not os.path.exists(INDEX_PATH) or not os.path.exists(METADATA_PATH):
    main()
    # question = input("请输入你的问题：")
    # results = search_papers(question)
    # if results:
    #     for result in results:
    #         print(f"论文：{result['filename']} - 段落 {result['segment_index']} - 距离：{result['distances']:.4f}")
    # else:
    #     print("❗ 未找到相关段落，请尝试重新输入问题。")