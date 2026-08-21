"""
处理管理模块
负责协调PDF处理流程
"""
import asyncio
import json
import os
import sys
from pathlib import Path
import shutil

from table_util.cos_storage import upload_file
from table_util.file_copy import copy_entity_annotation_file
from table_util.pdf_handler import download_pdf, process_pdf
from table_util.config import logger, PDF_CONFIG

async def process_pdf_workflow(pdf_id, pdf_url, manager, websocket):
    """
    执行完整的PDF处理工作流
    
    Args:
        pdf_id: 需要处理的PDF的id
        pdf_url: 需要处理的PDF的url
        manager: WebSocket连接管理器
        websocket: WebSocket连接
        
    Returns:
        bool: 处理是否成功
    """
    logger.info("开始执行PDF实体抽取处理工作流...")
    
    # 1. 下载PDF文件（路径已固定，base_dir参数仅为兼容）
    await manager.send_message(websocket, json.dumps({
        "event": "status",
        "status": "processing",
        "message": "正在下载PDF..."
    }, ensure_ascii=False))
    await asyncio.sleep(0)
    logger.info(f"开始下载PDF: {pdf_url}")
    
    # 调用下载函数（base_dir参数实际未使用，仅保持函数调用兼容）
    success, target_pdf_dir = download_pdf(pdf_url, "")
    # 从URL提取pdf_name（用于打包路径）
    file_name = os.path.basename(pdf_url)
    pdf_name = os.path.splitext(file_name)[0]
    
    if not success:
        logger.error("PDF下载失败")
        await manager.send_message(websocket, json.dumps({
            "event": "status",
            "status": "error",
            "message": "PDF下载失败"
        }, ensure_ascii=False))
        await asyncio.sleep(0)
        return False
    await manager.send_message(websocket, json.dumps({
        "event": "status",
        "status": "processing",
        "message": "PDF下载完成，开始处理实体抽取..."
    }, ensure_ascii=False))
    await asyncio.sleep(0)


    # 2. 处理PDF文件（输入目录为固定下载目录）
    logger.info(f"开始处理PDF文件，输入目录: {target_pdf_dir}")
    success = await process_pdf(target_pdf_dir)
    if not success:
        logger.error("PDF处理失败")
        return False
    await manager.send_message(websocket, json.dumps({
        "event": "status",
        "status": "processing",
        "message": "实体抽取完成，准备打包..."
    }, ensure_ascii=False))
    
    # 3. 上传处理结果到COS（打包路径固定为指定目录 + pdf_name）
    # 固定打包源目录前缀
    fixed_zip_root = "/home/jsj201-11/mount1/zjc/PaddleDetection/output/test1/"
    # 完整打包目录：固定前缀 + pdf_name
    dir_to_zip = os.path.join(fixed_zip_root, pdf_name)
    # 确保打包目录存在
    os.makedirs(dir_to_zip, exist_ok=True)
    
    # 输出zip文件路径（与源目录同层，自动添加.zip后缀）
    zip_output_path = os.path.join(fixed_zip_root, pdf_name)

    # 打包目录
    shutil.make_archive(zip_output_path, 'zip', dir_to_zip)
    logger.info(f"打包完成: {zip_output_path}.zip")

    # 上传到COS
    zip_path = f"{zip_output_path}.zip"
    cos_key = f"ExTable/{pdf_name}.zip"

    logger.info(f"PDF处理成功，正在准备结果下载链接")
    location = upload_file(zip_path, cos_key)
    print(location)
    logger.info(f"结果下载链接:{location}")
    os.remove(zip_path)  # 上传后删除本地zip文件
    await manager.send_message(websocket, json.dumps({
        "event": "status",
        "status": "ready",
        "location": location
    }, ensure_ascii=False))
    
    logger.info("PDF处理工作流成功完成!")
    return True 