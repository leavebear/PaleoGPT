import os
import openpyxl
import json

def convert_excel_to_json(file_path):
    # 加载Excel文件
    workbook = openpyxl.load_workbook(file_path)
    sheet = workbook.active  # 获取活动工作表

    # 初始化结果列表
    result = []

    # 遍历工作表的每一行
    for row in sheet.iter_rows(values_only=True):
        # 将每一行的内容转换为列表，并将每个单元格内容转换为字符串
        row_data = [str(cell) if cell is not None else "null" for cell in row]
        result.append(row_data)

    # 构建单个表格的JSON结构
    table_json = {
        "tableImg": 'https://paleodb-1306565154.cos.ap-shanghai.myqcloud.com/123/123_101.jpg',
        "table": result
    }
    return table_json

def process_all_excel_files_to_single_json(folder_path, output_file_path):
    # 获取文件夹中的所有.xlsx文件，按照文件系统中的顺序
    excel_files = [file_name for file_name in os.listdir(folder_path) if file_name.endswith(".xlsx")]

    # 初始化一个列表，用于存储所有表格的JSON内容
    all_tables = []

    # 遍历排序后的文件列表
    for file_name in excel_files:
        file_path = os.path.join(folder_path, file_name)
        # 转换为JSON格式
        table_json = convert_excel_to_json(file_path)
        # 将当前表格的JSON内容添加到列表中
        all_tables.append(table_json)

    # 构建最终的JSON结构
    final_json = {
        "status_code": 0,
        "status_msg": "Success",
        "data": {
            "pdfDownloadUrl": 'https://paleodb-1306565154.cos.ap-shanghai.myqcloud.com/123/123.pdf',
            "tableList": all_tables
        }
    }

    # 将所有表格的JSON内容保存到一个大的JSON文件中
    with open(output_file_path, "w", encoding="utf-8") as f:
        json.dump(final_json, f, indent=4, ensure_ascii=False)
    print(f"All tables have been processed and saved to {output_file_path}")

# 使用示例
folder_path = "table_text"  # 替换为你的文件夹路径
output_file_path = "output1.json"  # 指定输出的大JSON文件路径
process_all_excel_files_to_single_json(folder_path, output_file_path)