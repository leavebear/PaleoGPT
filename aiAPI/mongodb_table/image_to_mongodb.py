import json
from pymongo import MongoClient

# 连接到 MongoDB 数据库
def connect_to_mongodb(uri="mongodb://paleo_user:jsj201@localhost:27018/?authSource=paleodatabase", database_name="paleodatabase"):
    client = MongoClient(uri)  # 连接到服务器上的 MongoDB 服务
    db = client[database_name]  # 选择数据库
    return db

# 读取 JSON 文件并存储到 MongoDB
def store_json_to_mongodb(file_path, db, collection_name="image_extract"):
    # 读取 JSON 文件
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    
    # 选择或创建集合
    collection = db[collection_name]
    
    # 插入数据到 MongoDB
    result = collection.insert_one(data)
    print(f"Inserted document with ID: {result.inserted_id}")

# 主函数
def main():
    json_file_path = "image1.json"  # 替换为你的 JSON 文件路径
    db = connect_to_mongodb()  # 连接到 MongoDB
    store_json_to_mongodb(json_file_path, db)  # 将 JSON 数据存储到 MongoDB

if __name__ == "__main__":
    main()