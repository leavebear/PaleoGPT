import json
from fastapi import FastAPI, File, UploadFile, HTTPException, Request, Query, BackgroundTasks
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel
from typing import Optional, List
from fastapi.middleware.cors import CORSMiddleware
from openpyxl import load_workbook
from pymongo import MongoClient
from io import BytesIO
import uuid
import os
import sys
import shutil
import logging

import websockets


#文件上传保存目录
UPLOAD_FOLDER = '/home/jsj201-2/mount1/lihongjun/PaleoPRO/backend/QAsystem/docs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#数据库->前端 json格式
TABLE_DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "mongodb_table/output_retrieved.json"))
ENTITY_DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "mongodb_table/entity_retrieved_data.json"))
#尚未改成从数据库中取
IMAGE_DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),"../jsonForm/image.json"))  

app = FastAPI()
logger = logging.getLogger("uvicorn")

rag_ws_url = "ws://localhost:5200/generate_answer"
entity_ws_url = "ws://localhost:5000/entity"
image_ws_url = "ws://192.168.149.5:5100/image"
table_ws_url = "ws://localhost:5000/table"

# 配置 CORS 中间件，允许指定的来源进行跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174"],  # 允许所有域进行跨域请求
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
)

# 连接到 MongoDB 数据库
def connect_to_mongodb(uri="mongodb://paleo_user:jsj201@localhost:27018/?authSource=paleodatabase", database_name="paleodatabase"):
    client = MongoClient(uri)  # 连接到服务器上的 MongoDB 服务
    db = client[database_name]  # 选择数据库
    return db

# 定义用户登录请求的数据模型
class LoginRequest(BaseModel):
    email: str
    password: str

# 用户登录接口
@app.post("/api/user/login")
async def user_login(request: LoginRequest):
    try:
        # 连接到 MongoDB 数据库
        db = connect_to_mongodb()
        users_collection = db["paleo_user"]  # 假设用户数据存储在 "users" 集合中

        # 查询用户是否存在且密码匹配
        user = users_collection.find_one({"email": request.email, "password": request.password})

        if user:
            # 登录成功，返回用户信息或其他成功提示
            return {
                "status_code": 0,
                "status_msg": "登录成功",
                "data": {
                    # 假设用户文档中有 "_id" 字段
                    "email": user["email"]
                }
            }
        else:
            # 登录失败，用户名或密码错误
            raise HTTPException(status_code=401, detail="用户名或密码错误")
    except Exception as e:
        # 捕获异常并返回错误信息
        return {
            "status_code": -1,
            "status_msg": f"登录失败: {str(e)}",
            "data": {}
        }

# 定义项目数据模型
class Project(BaseModel):
    projectId: str
    projectName: str
    projectDescription: str
    normalMembers: List[dict]
    approvalMembers: List[dict]
    creatorId: str
    creatorName: str

# 获取所有项目信息的接口
@app.get("/api/project/init")
async def get_projects():
    try:
        # 连接到 MongoDB 数据库
        db = connect_to_mongodb()
        projects_collection = db["project"]  # 假设项目数据存储在 "project" 集合中

        # 查询所有项目
        projects_cursor = projects_collection.find({})
        projects = [project for project in projects_cursor]

        # 将项目数据转换为统一的格式
        formatted_projects = [
            {
                "projectId": project["projectId"],
                "projectName": project["projectName"],
                "projectDescription": project["projectDescription"],
                "normalMembers": project.get("normalMembers", []),
                "approvalMembers": project.get("approvalMembers", []),
                "creatorId": project.get("creatorId", ""),
                "creatorName": project.get("creatorName", "")
            }
            for project in projects
        ]

        # 返回项目数据
        return {
            "status_code": 0,
            "status_msg": "项目数据获取成功",
            "data": formatted_projects
        }
    except Exception as e:
        # 捕获异常并返回错误信息
        return {
            "status_code": -1,
            "status_msg": f"项目数据获取失败: {str(e)}",
            "data": []
        }

# 添加项目成员接口
@app.post("/api/project/addMember")
async def add_member(request: dict):
    try:
        # 连接到 MongoDB 数据库
        db = connect_to_mongodb()
        projects_collection = db["project"]  # 选择 project 集合

        # 获取请求参数
        project_id = request["projectId"]
        member_id = request["memberId"]
        member_name = request["memberName"]
        role = request["role"]  # "普通" 或 "审批"

        # 查询项目
        project = projects_collection.find_one({"projectId": project_id})
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")

        # 添加成员
        if role == "普通":
            project["normalMembers"].append({"id": member_id, "name": member_name})
        elif role == "审批":
            project["approvalMembers"].append({"id": member_id, "name": member_name})
        else:
            raise HTTPException(status_code=400, detail="无效的角色类型")

        # 更新项目
        projects_collection.update_one({"projectId": project_id}, {"$set": project})

        return {
            "status_code": 0,
            "status_msg": "成员添加成功",
            "data": {}
        }
    except Exception as e:
        # 捕获异常并返回错误信息
        return {
            "status_code": -1,
            "status_msg": f"成员添加失败: {str(e)}",
            "data": {}
        }

#删除项目成员接口
@app.post("/api/project/removeMember")
async def remove_member(request: dict):
    try:
        # 连接到 MongoDB 数据库
        db = connect_to_mongodb()
        projects_collection = db["project"]  # 选择 project 集合

        # 获取请求参数
        project_id = request["projectId"]
        member_id = request["memberId"]
        role = request["role"]  # "普通" 或 "审批"

        # 查询项目
        project = projects_collection.find_one({"projectId": project_id})
        if not project:
            raise HTTPException(status_code=404, detail="项目不存在")

        # 删除成员
        if role == "普通":
            project["normalMembers"] = [member for member in project["normalMembers"] if member["id"] != member_id]
        elif role == "审批":
            project["approvalMembers"] = [member for member in project["approvalMembers"] if member["id"] != member_id]
        else:
            raise HTTPException(status_code=400, detail="无效的角色类型")

        # 更新项目
        projects_collection.update_one({"projectId": project_id}, {"$set": project})

        return {
            "status_code": 0,
            "status_msg": "成员删除成功",
            "data": {}
        }
    except Exception as e:
        # 捕获异常并返回错误信息
        return {
            "status_code": -1,
            "status_msg": f"成员删除失败: {str(e)}",
            "data": {}
        }


class process_pdf_data(BaseModel):
    pdf_id:int 
    pdf_url:str

@app.post("/api/imageProcess")
async def process_pdf_image(request: process_pdf_data):
    try:
        pdf_id = request.pdf_id
        pdf_url = request.pdf_url

        async def event_stream():
                try:
                    print(f"[SSE] 准备连接 image WebSocket 服务: {image_ws_url}")
                    async with websockets.connect(image_ws_url) as ws:
                        await ws.send(json.dumps({
                            "pdf_id": pdf_id, 
                            "pdf_url": pdf_url
                        }))
                        print("[SSE] 已发送PDF相关信息")

                        async for message in ws:
                            yield f"data: {message}\n\n"

                except Exception as e:
                    print("[SSE] WebSocket 异常：", e)
                    yield f"data: [ERROR] {str(e)}\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/tableProcess")
async def process_pdf_table(request: process_pdf_data):
    try:
        pdf_id = request.pdf_id
        pdf_url = request.pdf_url

        async def event_stream():
                try:
                    print(f"[SSE] 准备连接 table WebSocket 服务: {table_ws_url}")
                    async with websockets.connect(table_ws_url) as ws:
                        await ws.send(json.dumps({
                            "pdf_id": pdf_id, 
                            "pdf_url": pdf_url
                        }))
                        print("[SSE] 已发送PDF相关信息")

                        async for message in ws:
                            yield f"data: {message}\n\n"

                except Exception as e:
                    print("[SSE] WebSocket 异常：", e)
                    yield f"data: [ERROR] {str(e)}\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/api/entityProcess")
async def process_pdf_entity(request: process_pdf_data):
    try:
        pdf_id = request.pdf_id
        pdf_url = request.pdf_url

        async def event_stream():
                try:
                    print(f"[SSE] 准备连接 Entity WebSocket 服务: {entity_ws_url}")
                    async with websockets.connect(entity_ws_url) as ws:
                        await ws.send(json.dumps({
                            "pdf_id": pdf_id, 
                            "pdf_url": pdf_url
                        }))
                        print("[SSE] 已发送PDF相关信息")

                        async for message in ws:
                            yield f"data: {message}\n\n"

                except Exception as e:
                    print("[SSE] WebSocket 异常：", e)
                    yield f"data: [ERROR] {str(e)}\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


# 定义请求体数据模型(表格抽取接口)
@app.post("/api/project/tableExtra")
async def upload_xlsx():
    try:
        with open(TABLE_DATA_FILE, "r", encoding="utf-8") as f:
            responseTest = json.load(f)
        return responseTest
    except Exception as e:
        return {
            "status_code": -1,
            "status_msg": f"读取 JSON 文件失败: {str(e)}",
            "data": {}
        }
    # 读取上传的 Excel 文件
    # file = File(...)
    # contents = await file.read()
    # wb = load_workbook(filename=BytesIO(contents))
    # sheet = wb.active

    # # 解析 Excel 表格内容
    # table_data = []
    
    # for row in sheet.iter_rows(min_row=1, max_row=sheet.max_row, min_col=1, max_col=sheet.max_column):
    #     row_data = [cell.value for cell in row]
    #     table_data.append(row_data)

    # # 生成 JSON 格式数据
    # response = {"table": table_data}


#实体抽取接口
@app.post("/api/project/entityExtra")
async def entityExtra():
    try:
        with open(ENTITY_DATA_FILE, "r", encoding="utf-8") as f:
            response_data = json.load(f)
        return {
            "status_code": 0,
            "status_msg": "success",
            "data": response_data
        }
    except Exception as e:
        return {
            "status_code": -1,
            "status_msg": f"读取 JSON 文件失败: {str(e)}",
            "data": {}
        }
    
@app.post("/api/project/updateEntity")
async def updateEntity(request: Request):
    try:
        updated_data = await request.json()

        # 覆盖写入文件
        with open(ENTITY_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=4)

        return {
            "status_code": 0,
            "status_msg": "更新成功",
            "data": {}
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status_code": -1,
                "status_msg": f"更新失败: {str(e)}",
                "data": {}
            }
        )

#图片抽取接口
@app.post("/api/project/imageExtra")
async def imageExtra():
    try:
        with open(IMAGE_DATA_FILE, "r", encoding="utf-8") as f:
            response_data = json.load(f)
        return {
            "status_code": 0,
            "status_msg": "success",
            "data": response_data
        }
    except Exception as e:
        return {
            "status_code": -1,
            "status_msg": f"读取 JSON 文件失败: {str(e)}",
            "data": {}
        }
    

# 定义输入数据结构
class ImageUpdateItem(BaseModel):
    ocr: Optional[str] = None
    child_fig: Optional[str] = None
    width: Optional[int] = None
    height: Optional[int] = None
    scale: Optional[float] = None



@app.post("/api/project/updateImage")
async def update_image(request: Request):
    try:
        updated_data = await request.json()

        # 覆盖写入文件
        with open(IMAGE_DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(updated_data, f, ensure_ascii=False, indent=4)

        return {
            "status_code": 0,
            "status_msg": "更新成功",
            "data": {}
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status_code": -1,
                "status_msg": f"更新失败: {str(e)}",
                "data": {}
            }
        )



def parse_xlsx(file_content: BytesIO) -> List[List[str]]:
    """ 解析Excel文件并返回表格数据列表 """
    wb = load_workbook(filename=file_content)
    sheet = wb.active
    
    table_data = []
    for row in sheet.iter_rows(min_row=1, max_row=sheet.max_row, min_col=1, max_col=sheet.max_column):
        row_data = [cell.value for cell in row]
        table_data.append(row_data)
    
    return table_data

@app.post("/upload-xlsx/")
async def upload_xlsx(file1: UploadFile = File(...), file2: UploadFile = File(...)):
    """ 处理两个上传的表格文件并返回JSON """
    
    # 读取第一个文件 (table1.xlsx)
    contents1 = await file1.read()
    table_data1 = parse_xlsx(BytesIO(contents1))
    
    # 读取第二个文件 (table2.xlsx)
    contents2 = await file2.read()
    table_data2 = parse_xlsx(BytesIO(contents2))

    # 构建响应数据
    response_data = {
        "status_code": 0,
        "status_msg": "Success",
        "data": {
            "pdfDownloadUrl": "https://paleodb-1306565154.cos.ap-shanghai.myqcloud.com/123456789/REDTab%20ARelation%20Extraction%20Dataset%20for%20Knowledge%20Extraction%20from%20WebTables.pdf",
            "tableList": [
                {
                    "tableImg": "https://paleodb-1306565154.cos.ap-shanghai.myqcloud.com/123456789/table1.jpg",
                    "table": table_data1
                },
                {
                    "tableImg": "https://paleodb-1306565154.cos.ap-shanghai.myqcloud.com/123456789/table2.jpg",
                    "table": table_data2
                }
            ]
        }
    }
    
    return response_data



sessions = {}


"""
sessionts[session_id]:{
    "question": question,
    "information": [{
        "filename": file_name,
        "content": file_content,
        "segment_index": segment_index
    }
    ]
}

"""


#把RAG模块独立出来 ， url为rag_ws_url 5200端口 6.6  

class QuestionData(BaseModel):
    text:str
    information:list

@app.post("/api/QAsystemStream")
async def submit_question(request: QuestionData):
    try:
        question = request.text
        files = request.information
        print(f"question: {question}, files: {files}")


        async def event_stream():
            try:
                print(f"[SSE] 准备连接 RAG WebSocket 服务: {rag_ws_url}")
                async with websockets.connect(rag_ws_url) as ws:
                    await ws.send(json.dumps({
                        "question": question, 
                        "information": files
                    }))
                    print("[SSE] 已发送初始问题")

                    async for message in ws:
                        yield f"data: {message}\n\n"

            except Exception as e:
                print("[SSE] WebSocket 异常：", e)
                yield f"data: [ERROR] {str(e)}\n\n"

        return StreamingResponse(event_stream(), media_type="text/event-stream")

    
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/uploadFile")
async def upload_file(file: UploadFile = File(...)):
    # 获取上传文件的名称
    file_location = f"{UPLOAD_FOLDER}/{file.filename}"
    
    # 保存文件
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    # main()
    return JSONResponse(content={"message": "文件上传成功", "file_path": file_location}, status_code=200)



#  curl -N -X POST http://localhost:8000/api/QAsystemStream -H "Content-Type: application/json" -d '{"post": {"text": "你好", "information": []}}'

# curl -X POST http://localhost:8000/api/QAsystem -H "Content-Type: application/json" -d '{"question": "你好"}'

# curl -X POST http://localhost:8000/api/project/imageExtra

# ps aux | grep uvicorn


# nohup uvicorn main:app --host 0.0.0.0 --port 8000 &