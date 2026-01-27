import json
import uuid
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

# 连接到 MongoDB 数据库
def connect_to_mongodb(uri="mongodb://paleo_user:jsj201@localhost:27018/?authSource=paleodatabase", database_name="paleodatabase"):
    """连接到 MongoDB 数据库"""
    client = MongoClient(uri)  # 连接到 MongoDB 服务
    db = client[database_name]  # 选择数据库
    return db

# 解析 bio_entity.txt 文件，提取文本内容和实体信息
def parse_bio_entity(file_path):
    """解析 bio_entity.txt 文件，提取文本内容和实体信息"""
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    # 按空行分隔文本段
    text_segments = []
    current_segment = []
    for line in lines:
        line = line.strip()
        if line:
            current_segment.append(line)
        else:
            if current_segment:
                text_segments.append(current_segment)
                current_segment = []
    if current_segment:
        text_segments.append(current_segment)
    
    # 处理每个文本段，提取文本内容和实体信息
    processed_segments = []
    entities = []
    
    for segment_idx, segment in enumerate(text_segments):
        # 提取单词部分
        words = [line.split()[0] for line in segment if line.split()]
        text_content = ' '.join(words)
        
        # 提取实体信息
        segment_entities = []
        current_entity = None
        current_entity_text = []
        current_entity_start = 0
        
        # 构建完整文本和记录每个单词的位置
        full_text = []
        word_positions = []
        current_pos = 0
        
        for j, line in enumerate(segment):
            if not line:
                continue
            
            parts = line.split()
            if len(parts) < 3:
                continue
                
            word = parts[0]
            full_text.append(word)
            word_positions.append((current_pos, current_pos + len(word)))
            current_pos += len(word) + 1  # +1 表示空格
        
        full_text_str = ' '.join(full_text)
        
        # 再次遍历，提取实体
        for j, line in enumerate(segment):
            if not line:
                continue
                
            parts = line.split()
            if len(parts) < 3:
                continue
                
            word = parts[0]
            tag = parts[2]
            
            if tag.startswith("B-"):
                # 如果当前已经有实体，保存当前实体
                if current_entity:
                    entity_text = " ".join(current_entity_text)
                    segment_entities.append({
                        "tag_name": current_entity,
                        "start": current_entity_start,
                        "end": word_positions[j-1][1],
                        "content": entity_text
                    })
                    
                # 开始新的实体
                current_entity = tag[2:]
                current_entity_text = [word]
                current_entity_start = word_positions[j][0]
            elif tag.startswith("I-"):
                # 继续当前实体
                if current_entity == tag[2:]:
                    current_entity_text.append(word)
                else:
                    # 实体类型不匹配，保存当前实体并开始新实体
                    if current_entity:
                        entity_text = " ".join(current_entity_text)
                        segment_entities.append({
                            "tag_name": current_entity,
                            "start": current_entity_start,
                            "end": word_positions[j-1][1],
                            "content": entity_text
                        })
                    current_entity = tag[2:]
                    current_entity_text = [word]
                    current_entity_start = word_positions[j][0]
            else:
                # 非实体部分
                if current_entity:
                    entity_text = " ".join(current_entity_text)
                    segment_entities.append({
                        "tag_name": current_entity,
                        "start": current_entity_start,
                        "end": word_positions[j-1][1],
                        "content": entity_text
                    })
                    current_entity = None
                    current_entity_text = []
        
        # 保存最后一个实体（如果有的话）
        if current_entity:
            entity_text = " ".join(current_entity_text)
            segment_entities.append({
                "tag_name": current_entity,
                "start": current_entity_start,
                "end": word_positions[-1][1],
                "content": entity_text
            })
        
        # text_id 从 0 开始编号
        processed_segments.append({
            "text_id": segment_idx,  # 使用序号作为 text_id，从 0 开始
            "text": full_text_str,
            "entities": segment_entities
        })
    
    return processed_segments

# 将文本内容存储到 text_chunks 集合
def save_to_text_chunks(db, pdf_id, processed_segments):
    """将文本内容存储到 text_chunks 集合"""
    text_chunks_collection = db["text_chunks"]
    
    # 构建 text_chunks 文档
    text_chunks_data = {
        "pdf_id": pdf_id,
        "textList": [
            {
                "text_id": segment["text_id"],
                "text": segment["text"]
            } for segment in processed_segments
        ]
    }
    
    # 插入到 text_chunks 集合
    result = text_chunks_collection.insert_one(text_chunks_data)
    print(f"文本内容已保存到 text_chunks 集合，ID: {result.inserted_id}")
    return result.inserted_id

# 将实体信息存储到 entity_extract 集合
def save_to_entity_extract(db, pdf_id, processed_segments):
    """将实体信息存储到 entity_extract 集合"""
    entity_extract_collection = db["entity_extract"]
    
    # 生成预定义模板 ID（这里使用一个固定的 ID，实际应用中可能需要从数据库获取）
    predef_id = ObjectId("692a86479182f3ca25356a0d")
    
    # 构建 entity_extract 文档
    entity_extract_data = {
        "pdf_id": pdf_id,
        "predef_id": predef_id,
        "textList": [
            {
                "text_id": segment["text_id"],
                "text_tag": segment["entities"]
            } for segment in processed_segments
        ],
        "relations": [],  # 初始没有关系数据
        "created_at": datetime.now(),
        "updated_at": datetime.now()
    }
    
    # 插入到 entity_extract 集合
    result = entity_extract_collection.insert_one(entity_extract_data)
    print(f"实体信息已保存到 entity_extract 集合，ID: {result.inserted_id}")
    return result.inserted_id

# 主函数
def main():
    # 配置文件路径
    bio_entity_file = "/home/lujie/mount/backend/aiAPI/mongodb_table/bio_entity.txt"
    
    # 连接 MongoDB
    print("正在连接 MongoDB...")
    db = connect_to_mongodb()
    
    # 生成 PDF ID
    pdf_id = str(uuid.uuid4())
    print(f"生成的 PDF ID: {pdf_id}")
    
    # 解析 bio_entity.txt 文件
    print("正在解析 bio_entity.txt 文件...")
    processed_segments = parse_bio_entity(bio_entity_file)
    print(f"解析完成，共处理 {len(processed_segments)} 个文本段")
    
    # 将文本内容存储到 text_chunks 集合
    print("正在将文本内容存储到 text_chunks 集合...")
    text_chunks_id = save_to_text_chunks(db, pdf_id, processed_segments)
    
    # 将实体信息存储到 entity_extract 集合
    print("正在将实体信息存储到 entity_extract 集合...")
    entity_extract_id = save_to_entity_extract(db, pdf_id, processed_segments)
    
    print("\n所有数据已成功存储到 MongoDB！")
    print(f"PDF ID: {pdf_id}")
    print(f"text_chunks 文档 ID: {text_chunks_id}")
    print(f"entity_extract 文档 ID: {entity_extract_id}")

if __name__ == "__main__":
    main()