import json
from pymongo import MongoClient

# 连接到 MongoDB 数据库
def connect_to_mongodb(uri="mongodb://paleo_user:jsj201@localhost:27018/?authSource=paleodatabase", database_name="paleodatabase"):
    client = MongoClient(uri)  # 连接到服务器上的 MongoDB 服务
    db = client[database_name]  # 选择数据库
    return db

# 从 MongoDB 中读取数据并恢复为 JSON 格式
def retrieve_data_from_mongodb(db, collection_name):
    collection = db[collection_name]  # 选择集合
    cursor = collection.find({})  # 获取所有文档
    data_list = []

    for document in cursor:
        # 提取 pdfDownloadUrl
        pdf_download_url = document.get("pdfDownloadUrl", "")
        
        # 初始化 tableList
        table_list = []
        
        # 遍历每个 table_x 字段
        for key, value in document.items():
            if key.startswith("table_"):
                table_info = {
                    "tableImg": value.get("tableImg", ""),
                    "table": value.get("table", [])
                }
                # 将字典形式的表格数据转换回二维列表
                table_data = []
                for row_dict in table_info["table"]:
                    row = [row_dict[str(i)] for i in range(len(row_dict))]
                    table_data.append(row)
                table_info["table"] = table_data
                table_list.append(table_info)
        
        # 构建最终的 JSON 数据结构
        data = {
            "status_code": 0,
            "status_msg": "Success",
            "data": {
                "pdfDownloadUrl": pdf_download_url,
                "tableList": table_list
            }
        }
        data_list.append(data)
    
    return data_list

# 将恢复的 JSON 数据写入文件
def write_json_to_file(data, output_file_path):
    with open(output_file_path, 'w', encoding='utf-8') as file:
        json.dump(data, file, ensure_ascii=False, indent=4)
    print(f"Data has been written to {output_file_path}")

# 主函数
def main():
    db = connect_to_mongodb()  # 连接到 MongoDB
    collection_name = "table_extract"  # 指定 collection 名称
    data_list = retrieve_data_from_mongodb(db, collection_name)  # 从 MongoDB 中读取数据
    if data_list:
        output_file_path = r"output_retrieved.json"  # 输出文件路径
        write_json_to_file(data_list[0], output_file_path)  # 将第一个数据写入文件
    else:
        print("No data found in the collection.")

if __name__ == "__main__":
    main()