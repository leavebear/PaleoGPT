"""
FastAPI应用程序主文件
"""
import os
import sys
import threading
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware

# 添加当前目录到Python路径
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from entity_config.config import (
    COS_CONFIG, PDF_CONFIG, LOG_CONFIG,
    logger, update_config
)
from entity_log.log_manager import roll_log_file
from entity_util.websocket_manager import (
    ConnectionManager,
    handle_websocket_connection
)
from entity_util.process_manager import process_pdf_workflow

app = FastAPI()

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 挂载静态文件目录
app.mount("/fontendTest", StaticFiles(directory="fontendTest"), name="fontendTest")

# WebSocket连接管理器
manager = ConnectionManager()

@app.websocket("/entity")
async def websocket_endpoint(websocket: WebSocket):
    print("[Server] WebSocket: Client connected.")
    """WebSocket连接处理"""
    logger.info("WebSocket /entity 连接开始")
    await handle_websocket_connection(websocket, logger, PDF_CONFIG, update_config)
    logger.info("WebSocket /entity 连接结束")



@app.post("/process")
async def process_pdf(pdf_url: str, pdf_id: str):
    """处理PDF文件的HTTP接口"""
    try:
        # 更新配置
        update_config("PDF_URL", pdf_url)
        update_config("PDF_ID", pdf_id)
        
        # 处理PDF
        success = process_pdf_workflow(logger, PDF_CONFIG)
        
        # 检查并滚动日志文件
        roll_log_file(LOG_CONFIG["log_file"])
        
        if success:
            return JSONResponse(
                content={"status": "success", "message": "PDF处理完成"},
                status_code=200
            )
        else:
            return JSONResponse(
                content={"status": "error", "message": "PDF处理失败"},
                status_code=500
            )
            
    except Exception as e:
        logger.error(f"处理PDF时发生错误: {str(e)}")
        # 检查并滚动日志文件
        roll_log_file(LOG_CONFIG["log_file"])
        return JSONResponse(
            content={"status": "error", "message": str(e)},
            status_code=500
        )

if __name__ == "__main__":
    import uvicorn
    # 启动时记录服务启动信息
    logger.info("PaleoGPTEntityExService服务启动")
    uvicorn.run(app, host="0.0.0.0", port=5000)

# nohup uvicorn app:app --host 0.0.0.0 --port 5000 &