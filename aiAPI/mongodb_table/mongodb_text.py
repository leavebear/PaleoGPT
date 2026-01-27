import json
from pymongo import MongoClient

# 连接到 MongoDB 数据库
def connect_to_mongodb(uri="mongodb://paleo_user:jsj201@localhost:27018/?authSource=paleodatabase", database_name="paleodatabase"):
    client = MongoClient(uri)  # 连接到服务器上的 MongoDB 服务
    db = client[database_name]  # 选择数据库
    return db

# 读取 JSON 文件并解析表格数据
def read_json_and_parse_table(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:  # 显式指定文件编码为 UTF-8
        data = json.load(file)
    
    pdf_download_url = data.get("data", {}).get("pdfDownloadUrl", "")
    table_list = data.get("data", {}).get("tableList", [])
    return pdf_download_url, table_list

# 将表格数据转换为字典列表
def convert_to_dicts(table_data):
    dict_list = []
    for row in table_data:
        row_dict = {str(i): value for i, value in enumerate(row)}
        dict_list.append(row_dict)
    return dict_list

# 将数据存储到 MongoDB
def store_data_in_mongodb(db, collection_name, pdf_download_url, table_list):
    collection = db[collection_name]  # 选择或创建集合
    document = {"pdfDownloadUrl": pdf_download_url}
    for index, table_info in enumerate(table_list, start=1):
        table_field_name = f"table_{index}"
        document[table_field_name] = {
            "tableImg": table_info.get("tableImg", ""),
            "table": convert_to_dicts(table_info.get("table", []))
        }
    result = collection.insert_one(document)
    print(f"Inserted document into {collection_name}. ID: {result.inserted_id}")

# 主函数
def main():
    json_file_path = r"output1.json"  # 替换为你的 JSON 文件路径
    db = connect_to_mongodb()  # 连接到 MongoDB
    pdf_download_url, table_list = read_json_and_parse_table(json_file_path)  # 解析 JSON 文件
    store_data_in_mongodb(db, "table_extract", pdf_download_url, table_list)  # 存储到 MongoDB

if __name__ == "__main__":
    main()