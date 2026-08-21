import json
from pymongo import MongoClient

# 连接到 MongoDB 数据库
def connect_to_mongodb(uri="mongodb://localhost:27017/", database_name="mydatabase", collection_name="mycollection"):
    client = MongoClient(uri)  # 默认连接到本地 MongoDB 服务
    db = client[database_name]  # 选择数据库
    collection = db[collection_name]  # 选择集合
    return collection

# 读取 JSON 文件并解析表格数据
def read_json_and_parse_table(file_path):
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    table_data = data.get("table", [])
    return table_data

# 将表格数据转换为字典列表
def convert_to_dicts(table_data):
    dict_list = []
    for row in table_data:
        row_dict = {str(i): value for i, value in enumerate(row)}
        dict_list.append(row_dict)
    return dict_list

# 将数据存储到 MongoDB
def store_data_in_mongodb(collection, data):
    result = collection.insert_many(data)
    print(f"Inserted {len(result.inserted_ids)} documents into MongoDB.")

# 主函数
def main():
    json_file_path = r"table_text\01zjcTest_121.json"  # 替换为你的 JSON 文件路径
    collection = connect_to_mongodb()  # 连接到 MongoDB
    table_data = read_json_and_parse_table(json_file_path)  # 解析 JSON 文件
    parsed_data = convert_to_dicts(table_data)  # 将表格数据转换为字典列表
    store_data_in_mongodb(collection, parsed_data)  # 存储到 MongoDB

if __name__ == "__main__":
    main()