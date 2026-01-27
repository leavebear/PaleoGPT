import json
import os
import uuid
from datetime import datetime
from pymongo import MongoClient
from bson import ObjectId

# 从mongodb_entity.py导入连接数据库的函数
def connect_to_mongodb(uri="mongodb://paleo_user:jsj201@localhost:27018/?authSource=paleodatabase", database_name="paleodatabase"):
    """连接到 MongoDB 数据库"""
    client = MongoClient(uri)  # 连接到 MongoDB 服务
    db = client[database_name]  # 选择数据库
    return db

def parse_entity_annotation(file_path):
    """解析全实体标注.txt文件，提取实体标注信息"""
    sentences = []
    current_sentence_parts = []
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line:
            # 处理完一个句子
            if current_sentence_parts:
                sentences.append(' '.join(current_sentence_parts))
                current_sentence_parts = []
            continue
        
        parts = line.split(' ')
        if len(parts) >= 3:
            text = ' '.join(parts[:-2])
            current_sentence_parts.append(text)
    
    # 处理最后一个句子
    if current_sentence_parts:
        sentences.append(' '.join(current_sentence_parts))
    
    return sentences

def extract_entities_from_annotation(file_path):
    """从标注文件中提取实体信息，包括位置、内容和类型"""
    sentences = []
    entities = []
    current_sentence_parts = []
    sentence_start_index = 0
    
    with open(file_path, 'r', encoding='utf-8') as f:
        lines = f.readlines()
    
    for line in lines:
        line = line.strip()
        if not line:
            # 处理完一个句子
            if current_sentence_parts:
                sentences.append(' '.join(current_sentence_parts))
                current_sentence_parts = []
                sentence_start_index += 1
            continue
        
        parts = line.split(' ')
        if len(parts) >= 3:
            text = parts[0]  # 第一个部分是文本内容
            tag1 = parts[1]  # 第二个部分是标签1
            tag2 = parts[2]  # 第三个部分是标签2
            
            # 计算当前token在句子中的位置
            token_start = sum(len(part) + 1 for part in current_sentence_parts) if current_sentence_parts else 0
            token_end = token_start + len(text)
            
            # 处理实体标注 - 从tag2提取实体信息
            if tag2.startswith('B-'):
                entity_type = tag2[2:]
                entities.append({
                    'text_id': str(sentence_start_index),
                    'start': token_start,
                    'end': token_end,
                    'mark_content': text,
                    'tag_type': entity_type
                })
            elif tag2.startswith('I-') and entities:
                # 继续当前实体
                last_entity = entities[-1]
                if last_entity['text_id'] == str(sentence_start_index):
                    # 确保实体类型匹配
                    expected_type = tag2[2:]
                    if last_entity['tag_type'] == expected_type:
                        # 在同一个句子中，扩展实体
                        last_entity['end'] = token_end
                        last_entity['mark_content'] += ' ' + text
            
            current_sentence_parts.append(text)
    
    # 处理最后一个句子
    if current_sentence_parts:
        sentences.append(' '.join(current_sentence_parts))
    
    return sentences, entities

def convert_to_mongodb_format(sentences, entities, file_path):
    """将实体数据转换为MongoDB集合要求的格式"""
    # 生成唯一标识
    pdf_id = str(uuid.uuid4())
    predef_id = "default_template"
    
    # 构建textList
    textList = []
    sentence_entities_map = {}
    
    # 按句子ID分组实体
    for entity in entities:
        text_id = entity['text_id']
        if text_id not in sentence_entities_map:
            sentence_entities_map[text_id] = []
        sentence_entities_map[text_id].append(entity)
    
    # 构建textList
    for idx, sentence in enumerate(sentences):
        text_id = str(idx)
        text_tag = []
        
        # 添加该句子的所有实体
        if text_id in sentence_entities_map:
            for entity in sentence_entities_map[text_id]:
                text_tag.append({
                    'tag_name': entity['tag_type'],  # 使用实体类型作为tag_id
                    'start': entity['start'],
                    'end': entity['end'],
                    'mark_content': entity['mark_content']
                })
        
        textList.append({
            'text': sentence,
            'text_tag': text_tag
        })
    
    # 构建完整的MongoDB文档
    return {
        'pdf_id': pdf_id,
        'predef_id': predef_id,
        'textList': textList,
        'relations': [],  # 初始没有关系数据
        'created_at': datetime.now(),
        'updated_at': datetime.now()
    }

def save_to_mongodb(data, db, collection_name="entity_extract"):
    """将数据保存到MongoDB"""
    collection = db[collection_name]
    result = collection.insert_one(data)
    print(f"数据已保存到MongoDB，ID: {result.inserted_id}")
    return result.inserted_id

def save_to_json_file(data, file_path):
    """将数据保存到JSON文件（用于备份）"""
    # 转换datetime对象为字符串
    def convert_datetime(obj):
        if isinstance(obj, dict):
            return {k: convert_datetime(v) for k, v in obj.items()}
        elif isinstance(obj, list):
            return [convert_datetime(item) for item in obj]
        elif isinstance(obj, datetime):
            return obj.isoformat()
        elif isinstance(obj, ObjectId):
            return str(obj)
        else:
            return obj
    
    data = convert_datetime(data)
    
    # 确保输出目录存在
    os.makedirs(os.path.dirname(os.path.abspath(file_path)), exist_ok=True)
    
    try:
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"数据已保存到JSON文件: {file_path}")
    except PermissionError:
        # 如果没有权限，尝试保存到用户主目录
        fallback_path = os.path.expanduser(f"~/{os.path.basename(file_path)}")
        with open(fallback_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
        print(f"权限错误，数据已保存到备用路径: {fallback_path}")

if __name__ == "__main__":
    # 配置文件路径 - 修改为biotext.txt
    annotation_file = "/data/user/lihongjun/mount/PaleoPRO/backend/aiAPI/mongodb_table/biotext.txt"
    json_output_file = "/data/user/lihongjun/mount/PaleoPRO/backend/aiAPI/mongodb_table/entity_output_v2.json"
    
    # 解析实体标注文件
    print(f"正在解析实体标注文件: {annotation_file}")
    try:
        sentences, entities = extract_entities_from_annotation(annotation_file)
        print(f"找到 {len(entities)} 个实体，{len(sentences)} 个句子")
        
        # 打印找到的实体信息
        if entities:
            print("提取到的实体信息:")
            for entity in entities:
                print(f"  - 类型: {entity['tag_type']}, 内容: {entity['mark_content']}, 位置: {entity['start']}-{entity['end']}")
        
        # 转换为MongoDB格式
        mongodb_data = convert_to_mongodb_format(sentences, entities, annotation_file)
        
        # 保存到JSON文件（备份）
        save_to_json_file(mongodb_data, json_output_file)
        
        # 连接MongoDB并保存数据
        print("正在连接MongoDB...")
        try:
            db = connect_to_mongodb()
            save_to_mongodb(mongodb_data, db)
            print("实体数据已成功处理并存储到MongoDB！")
        except Exception as e:
            print(f"连接MongoDB或保存数据时出错: {e}")
            print("数据已保存到JSON文件，但未能存储到MongoDB")
    
    except Exception as e:
        print(f"处理实体标注文件时出错: {e}")