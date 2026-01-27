import json
from pymongo import MongoClient

# 连接到 MongoDB 数据库
def connect_to_mongodb(uri="mongodb://paleo_user:jsj201@localhost:27018/?authSource=paleodatabase", database_name="paleodatabase"):
    client = MongoClient(uri)  # 连接到服务器上的 MongoDB 服务
    db = client[database_name]  # 选择数据库
    return db

# 从 MongoDB 中取出数据并保存到 JSON 文件
def retrieve_data_from_mongodb(db, collection_name="image_extract", output_file_path="image_output_data.json"):
    # 选择集合
    collection = db[collection_name]
    
    # 获取所有文档
    cursor = collection.find({})
    
    # 将所有文档转换为列表，并移除 ObjectId 字段
    data_list = []
    for document in cursor:
        # 移除 ObjectId 字段
        document.pop("_id", None)
        data_list.append(document)
    
    # 如果 data_list 不为空，取出第一个文档
    if data_list:
        data = data_list[0]
    else:
        data = {}
    
    # 将数据写入 JSON 文件
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    
    print(f"Data has been written to {output_file_path}")

# 主函数
def main():
    db = connect_to_mongodb()  # 连接到 MongoDB
    retrieve_data_from_mongodb(db)  # 从 MongoDB 中取出数据并保存到 JSON 文件

if __name__ == "__main__":
    main()