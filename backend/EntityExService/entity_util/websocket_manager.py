"""
WebSocket连接管理模块
"""
import asyncio
import json
import sys
import os
import time
from typing import List
from fastapi import WebSocket, WebSocketDisconnect


# 导入日志滚动功能
from entity_log.log_manager import roll_log_file
from entity_util.process_manager import process_pdf_workflow

# 导入配置模块以获取日志文件路径
from entity_config.config import LOG_CONFIG

class ConnectionManager:
    """WebSocket连接管理器"""
    def __init__(self):
        self.active_connections: List[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        """建立WebSocket连接"""
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        """断开WebSocket连接"""
        self.active_connections.remove(websocket)

    async def send_message(self, websocket: WebSocket, message: str):
        """发送消息到客户端"""
        await websocket.send_text(message)

async def heartbeat(websocket: WebSocket, logger, interval: int = 3):
    try:
        while True:
            await websocket.send_text(json.dumps({
                "event": "heartbeat",
                "message": "keep-alive",
                "timestamp": time.time()
            }, ensure_ascii=False))
            # logger.info("心跳一次")
            await asyncio.sleep(interval)
    except Exception:
        # 断开连接时退出
        pass

async def handle_websocket_connection(websocket: WebSocket, logger, PDF_CONFIG, update_config):
    """
    处理WebSocket连接
    
    Args:
        websocket: WebSocket连接
        logger: 日志记录器
        pdf_config: PDF配置
        update_config: 更新配置的函数
    """
    # 创建连接管理器
    manager = ConnectionManager()
    await manager.connect(websocket)

    heartbeat_task = asyncio.create_task(heartbeat(websocket,logger))

    
    try:
        success = False
        # 等待接收参数
        data = await websocket.receive_text()
        params = json.loads(data)
        
        # 提取参数
        pdf_id = params.get("pdf_id", PDF_CONFIG["pdf_id"])
        pdf_url = params.get("pdf_url", PDF_CONFIG["pdf_url"])
        
        # 发送开始处理的消息
        
        await manager.send_message(websocket, json.dumps({
            "event": "status",
            "status": "processing",
            "message": "开始处理PDF文件..."
        }, ensure_ascii=False))
        
        # 更新配置
        update_config("PDF_ID", pdf_id)
        update_config("PDF_URL", pdf_url)
        
        # 执行处理流程
        logger.info(f"开始通过WebSocket处理PDF: id={pdf_id}, url={pdf_url}")
        
        # 发送下载状态
        await manager.send_message(websocket, json.dumps({
            "event": "status",
            "status": "processing",
            "message": "正在下载PDF文件..."
        }, ensure_ascii=False))
        
        # 处理PDF
        process_task = asyncio.create_task(
            process_websocket_task(logger, PDF_CONFIG, manager, websocket)
        )

        success = await process_task

        
        if success:
            # 发送成功消息
            await manager.send_message(websocket, json.dumps({
                "event": "status",
                "status": "success",
                "message": "PDF实体抽取处理成功",
                "pdf_id": pdf_id
            }, ensure_ascii=False))
        else:
            # 发送失败消息
            await manager.send_message(websocket, json.dumps({
                "event": "status",
                "status": "error",
                "message": "PDF实体抽取处理失败",
                "pdf_id": pdf_id
            }, ensure_ascii=False))
            
        
    except WebSocketDisconnect:
        manager.disconnect(websocket)
        logger.warning("WebSocket连接断开")
    except Exception as e:
        logger.error(f"WebSocket处理过程中发生错误: {str(e)}")
        try:
            await manager.send_message(websocket, json.dumps({
                "event": "status",
                "status": "error",
                "message": f"处理失败: {str(e)}"
            }, ensure_ascii=False))
        except:
            pass
        manager.disconnect(websocket)

    finally:
        #  结束前关闭心跳和连接
        heartbeat_task.cancel()
        manager.disconnect(websocket)
        roll_log_file(LOG_CONFIG["log_file"])


async def process_websocket_task(logger, pdf_config, manager, websocket):
    """
    通过WebSocket处理PDF任务
    
    Args:
        logger: 日志记录器
        pdf_config: PDF配置
        manager: WebSocket连接管理器
        websocket: WebSocket连接
    
    Returns:
        bool: 处理结果
    """
    success = True

    try:
        # 执行处理任务
        # success = process_pdf_workflow(logger, pdf_config)
        
        
        # 根据处理结果发送不同的状态消息
        if success:
            await manager.send_message(websocket, json.dumps({
                "event": "status",
                "status": "processing", 
                "message": "处理完成，正在准备实体抽取结果..."
            }, ensure_ascii=False))
        
        return success
    except Exception as e:
        logger.error(f"WebSocket任务处理失败: {str(e)}")
        await manager.send_message(websocket, json.dumps({
            "event": "status",
            "status": "error",
            "message": f"处理失败: {str(e)}"
        }, ensure_ascii=False))
        return False 