import json
import random
from pymongo import MongoClient

def generate_random_color():
    """生成随机颜色"""
    return "#{:02X}{:02X}{:02X}".format(random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

def bio_to_sentence_and_entities(file_path):
    # 初始化变量
    sentences = []  # 用于存储所有句子及其标注的实体
    current_sentence = []  # 当前句子的单词
    current_entities = []  # 当前句子的实体
    current_entity = []  # 当前实体的单词
    current_entity_type = None  # 当前实体的类型
    ttag = []  # 用于存储所有实体类型，允许重复
    tag_id_counter = 0  # 用于生成唯一的tag_id
    color_map = {}  # 用于存储每个实体类型的颜色
    tag_id_map = {}  # 用于存储每个实体类型的固定tag_id

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
                        tag_id = tag_id_map.get(current_entity_type, f"tag_id{tag_id_counter}")
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
                            "tag_name": current_entity_type,
                            "tag_color": color_map[current_entity_type],  # 使用已分配的颜色
                            "tag_id": tag_id,
                        })
                        if current_entity_type not in tag_id_map:
                            tag_id_map[current_entity_type] = tag_id
                            tag_id_counter += 1
                        current_entity = []
                    # 开始新的实体
                    current_entity_type = tag[2:]
                    if current_entity_type not in color_map:
                        color_map[current_entity_type] = generate_random_color()  # 为新实体类型生成颜色
                    current_entity.append(word)
                elif tag.startswith("I-"):
                    # 继续当前实体
                    current_entity.append(word)
                else:
                    # 非实体部分
                    if current_entity:
                        tag_id = tag_id_map.get(current_entity_type, f"tag_id{tag_id_counter}")
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
                            "tag_name": current_entity_type,
                            "tag_color": color_map[current_entity_type],  # 使用已分配的颜色
                            "tag_id": tag_id,
                        })
                        if current_entity_type not in tag_id_map:
                            tag_id_map[current_entity_type] = tag_id
                            tag_id_counter += 1
                        current_entity = []
            else:  # 如果是空行，表示句子结束
                if current_sentence:
                    # 确保最后一个实体被保存
                    if current_entity:
                        tag_id = tag_id_map.get(current_entity_type, f"tag_id{tag_id_counter}")
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
                            "tag_name": current_entity_type,
                            "tag_color": color_map[current_entity_type],  # 使用已分配的颜色
                            "tag_id": tag_id,
                        })
                        if current_entity_type not in tag_id_map:
                            tag_id_map[current_entity_type] = tag_id
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
                tag_id = tag_id_map.get(current_entity_type, f"tag_id{tag_id_counter}")
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
                    "tag_name": current_entity_type,
                    "tag_color": color_map[current_entity_type],  # 使用已分配的颜色
                    "tag_id": tag_id,
                })
                if current_entity_type not in tag_id_map:
                    tag_id_map[current_entity_type] = tag_id
                    tag_id_counter += 1
            sentences.append({
                "text": " ".join(current_sentence),
                "text_tag": current_entities
            })

    # 构建最终的JSON结构
    result = {
        "pdf_id": 123,
        "textList": sentences,
        "ttag": ttag
    }

    return result

# 连接到 MongoDB 数据库
def connect_to_mongodb(uri="mongodb://paleo_user:jsj201@localhost:27018/?authSource=paleodatabase", database_name="paleodatabase"):
    client = MongoClient(uri)  # 连接到服务器上的 MongoDB 服务
    db = client[database_name]  # 选择数据库
    return db

# 将数据插入到 MongoDB
def insert_data_to_mongodb(db, data):
    collection = db['entity_extract']  # 选择或创建集合
    collection.insert_one(data)  # 插入数据

# 使用示例，不测试的时候需要注释
file_path = 'bio_entity.txt'  # 替换为你的标注文件路径
result = bio_to_sentence_and_entities(file_path)

# 将结果保存为JSON文件
output_file_path = 'entity_output_test.json'
with open(output_file_path, 'w', encoding='utf-8') as f:
    json.dump(result, f, indent=4, ensure_ascii=False)

print(f"Processed content has been saved to {output_file_path}")

# 连接到 MongoDB
db = connect_to_mongodb()

# 将数据插入到 MongoDB
insert_data_to_mongodb(db, result)

print(f"Data has been inserted into MongoDB.")