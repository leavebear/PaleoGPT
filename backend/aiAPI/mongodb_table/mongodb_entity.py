import json
from pymongo import MongoClient
from bson import ObjectId  # 导入 ObjectId 类型

def connect_to_mongodb(uri="mongodb://paleo_user:jsj201@localhost:27018/?authSource=paleodatabase", database_name="paleodatabase"):
    """连接到 MongoDB 数据库"""
    client = MongoClient(uri)  # 连接到 MongoDB 服务
    db = client[database_name]  # 选择数据库
    return db

def retrieve_data_from_mongodb(db, collection_name="entity_extract"):
    """从 MongoDB 中取出数据"""
    collection = db[collection_name]  # 选择集合
    data = collection.find_one()  # 取出一条数据，你可以根据需要修改查询条件
    return data

def save_to_json_file(data, file_path):
    """将数据保存到 JSON 文件中"""
    # 将 ObjectId 转换为字符串，并删除 _id 字段
    def convert_object_id_to_str(obj):
        if isinstance(obj, dict):
            return {k: convert_object_id_to_str(v) for k, v in obj.items() if k != "_id"}
        elif isinstance(obj, list):
            return [convert_object_id_to_str(item) for item in obj]
        elif isinstance(obj, ObjectId):
            return str(obj)
        else:
            return obj

    data = convert_object_id_to_str(data)

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

# 使用示例
# 连接到 MongoDB
db = connect_to_mongodb()

# 从 MongoDB 中取出数据
data = retrieve_data_from_mongodb(db)

# 将数据保存到 JSON 文件中
output_file_path = 'entity_retrieved_data.json'
save_to_json_file(data, output_file_path)

print(f"Data has been retrieved from MongoDB and saved to {output_file_path}")