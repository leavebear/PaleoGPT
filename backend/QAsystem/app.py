import os
import sys
from fastapi import FastAPI, WebSocket, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from qa_config.config import (
    logger, LOG_CONFIG, update_config
)
from qa_util.websocket_manager import (
    ConnectionManager,
    handle_websocket_connection
)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有域进行跨域请求
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
)

# WebSocket连接管理器
manager = ConnectionManager()

@app.websocket("/generate_answer")
async def websocket_endpoint(websocket: WebSocket):
    print("[Server] WebSocket: Client connected.")
    """WebSocket连接处理"""
    logger.info("WebSocket /generate_answer 连接开始")
    await handle_websocket_connection(websocket, logger)
    logger.info("WebSocket /generate_answer 连接结束")

@app.post("/hello")
async def hello():
    logger.info("POST /hello 接口被调用")
    return JSONResponse(content={"message": "Hello, World!"})

    
if __name__ == "__main__":
    import uvicorn
    # 启动时记录服务启动信息
    logger.info("PaleoGPT对话RAG系统服务启动")
    uvicorn.run(app, host="0.0.0.0", port=5200, access_log=True)

# nohup uvicorn app:app --host 0.0.0.0 --port 5200 &
