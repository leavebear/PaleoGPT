"""
处理管理模块
负责协调PDF处理流程
"""
import os
import sys

from entity_util.cos_storage import upload_directory
from entity_util.file_copy import copy_entity_annotation_file
from entity_util.pdf_handler import download_pdf, process_pdf

# 导入工具模块

def process_pdf_workflow(logger, PDF_CONFIG):
    """
    执行完整的PDF处理工作流
    
    Args:
        logger: 日志记录器
        PDF_CONFIG: PDF配置项
        
    Returns:
        bool: 处理是否成功
    """
    logger.info("开始执行PDF实体抽取处理工作流...")
    
    # 获取PDF ID和目录路径
    pdf_id = PDF_CONFIG["pdf_id"]
    input_pdf_dir = PDF_CONFIG["input_pdf_dir"]
    pdf_url = PDF_CONFIG["pdf_url"]
    data_dir = PDF_CONFIG["data_dir"]
    
    # 1. 下载PDF文件
    logger.info(f"开始下载PDF: {pdf_url}")
    success, local_path = download_pdf(pdf_url, input_pdf_dir)
    if not success:
        logger.error("PDF下载失败")
        return False
    
    # 2. 处理PDF文件
    logger.info(f"开始处理PDF文件，输入目录: {input_pdf_dir}")
    if not process_pdf(input_pdf_dir):
        logger.error("PDF处理失败")
        return False
    
    # 3. 复制全实体标注文件
    # 添加当前目录到PATH
    sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    logger.info("开始复制全实体标注文件...")
    if not copy_entity_annotation_file():
        logger.warning("复制[全实体标注.txt]文件失败，但继续执行")
    
    # 4. 上传处理结果到COS
    logger.info(f"开始上传处理结果到COS: {data_dir} -> {pdf_id}/")
    success = upload_directory(f"{pdf_id}/", data_dir)
    if not success:
        logger.error("上传到COS失败")
        return False
    
    logger.info("PDF处理工作流成功完成!")
    return True 