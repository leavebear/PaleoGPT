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

# 添加项目根目录到sys.path

# 导入日志滚动功能
from qa_log.log_manager import roll_log_file

# 导入配置模块以获取日志文件路径
from qa_config.config import LOG_CONFIG

from qa_util.knowledge_base import get_answer_from_knowledge_base_stream, get_information

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

async def handle_websocket_connection(websocket: WebSocket, logger):
    """
    处理WebSocket连接
    
    Args:
        websocket: WebSocket连接
        logger: 日志记录器
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
        question = params.get("question", "")
        files = params.get("information", [])

        if not question:
            await manager.send_message(websocket, json.dumps({
                "event": "status",
                "status": "error",
                "message": "未提供问题"
            }, ensure_ascii=False))
            await asyncio.sleep(0)
            logger.error(f"用户未提供问题")
            manager.disconnect(websocket)
            return
        

        await manager.send_message(websocket, json.dumps({
            "event": "status",
            "status": "processing",
            "message": "收到问题"
        }, ensure_ascii=False))
        

        logger.info(f"收到问题, 开始通过WebSocket处理问题: question={question}")
        
        # 处理对话，发送对话成功之后返回状态
        # 这里将处理任务创建为后台任务
        process_task = asyncio.create_task(
            process_websocket_task(logger, question, files, manager, websocket)
        )

        success = await process_task
            
        if success:
            # 发送成功消息
            await manager.send_message(websocket, json.dumps({
                "event": "status",
                "status": "success",
                "message": "对话处理成功",
            }, ensure_ascii=False))
        else:
            # 发送失败消息
            await manager.send_message(websocket, json.dumps({
                "event": "status",
                "status": "error",
                "message": "大模型连接失败",
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



# 文件内置处理方法
async def process_websocket_task(logger, question, files, manager, websocket):
    """
    通过WebSocket处理rag任务
    
    Args:
        logger: 日志记录器
        question: 用户的问题
        files: 前端提供的背景资料
        manager: WebSocket连接管理器
        websocket: WebSocket连接
    
    Returns:
        bool: 处理结果
    """
    success = False

    try:
        # 执行处理任务

        # 判断前端文件是否包含背景知识
        if not files:
            logger.info(f"开始从从知识库中找背景知识")

            await manager.send_message(websocket, json.dumps({
                "event": "status",
                "status": "processing",
                "message": "正在搜索背景知识..."
            }, ensure_ascii=False))
            await asyncio.sleep(0)

            files = await get_information(question, logger)
            logger.info(f"从知识库中找到以下背景知识: question={question}, files={files}")

            await manager.send_message(websocket, json.dumps({
            "event": "data",
            "files": files
            }, ensure_ascii=False))
            await asyncio.sleep(0)

            await manager.send_message(websocket, json.dumps({
                "event": "status",
                "status": "processing",
                "message": "背景知识搜索完成，正在生成对话..."
            }, ensure_ascii=False))
            await asyncio.sleep(0)

        else:
            logger.info(f"用户提供了背景知识")

            await manager.send_message(websocket, json.dumps({
                "event": "status",
                "status": "processing",
                "message": "用户提供了背景知识，正在根据背景知识生成对话..."
            }, ensure_ascii=False))
            await asyncio.sleep(0)

        # 打包发送给qwq32B
        query = {
            "question": question,
            "information": files
        }


        async for chunk in get_answer_from_knowledge_base_stream(query):
            # 通过WebSocket发送流式返回的部分答案
            await manager.send_message(websocket,chunk)

            # 判断流中是否包含一个最终状态事件
            payload = json.loads(chunk)
            if payload.get("event") == "status" and payload.get("status") == "error":
                return False
            if payload.get("event") == "status" and payload.get("status") == "success":
                success = True
        
        return success

    except Exception as e:
        logger.error(f"WebSocket任务处理失败: {str(e)}")
        await manager.send_message(websocket, json.dumps({
            "event": "status",
            "status": "error",
            "message": f"处理失败: {str(e)}"
        }, ensure_ascii=False))
        return False 
    