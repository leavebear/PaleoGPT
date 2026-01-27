from datetime import datetime
import json
from fastapi import FastAPI, File, Form, UploadFile, HTTPException, Request, Query, BackgroundTasks
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
import asyncio
import aiohttp
import zipfile
from pydantic import BaseModel, Field, validator
from typing import  Dict, Any
from datetime import datetime
from bson import ObjectId
### 9.22
## from utils import bio_to_sentence
### 

from qcloud_cos import (
    CosConfig,
    CosS3Client,
    CosServiceError,
    CosClientError,
)

COS_CONFIG = {
    "region": "ap-shanghai",
    "secret_id": "YOUR_TENCENT_SECRET_ID",
    "secret_key": "YOUR_TENCENT_SECRET_KEY",
    "bucket": "paleodb-1306565154",
    "TOKEN": "",
    "SCHEME": "https"
}

# 创建COS客户端
def create_cos_client():
    """创建COS客户端"""
    config = CosConfig(
        Region=COS_CONFIG["region"],
        SecretId=COS_CONFIG["secret_id"],
        SecretKey=COS_CONFIG["secret_key"],
        Token=COS_CONFIG["TOKEN"],
        Scheme=COS_CONFIG["SCHEME"]
    )
    return CosS3Client(config)

# 初始化全局客户端
client = create_cos_client()

#文件上传保存目录
UPLOAD_FOLDER = '/home/jsj201-2/mount1/lihongjun/PaleoPRO/backend/QAsystem/docs'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#数据库->前端 json格式（好像都没从数据库取出）
TABLE_DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "mongodb_table/output_retrieved.json"))
# ENTITY_DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "mongodb_table/entity_retrieved_data.json"))
ENTITY_DATA_FILE = "/home/jsj201-2/mount1/lihongjun/PaleoPRO/backend/aiAPI/mongodb_table/entity_output2.json"
#尚未改成从数据库中取
IMAGE_DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__),"../jsonForm/image.json")) 
FILE_LIST = "/home/jsj201-2/mount1/lihongjun/PaleoPRO/backend/jsonForm/fileList.json" 

# 模型直接输出结果
ENTITY_OUTPUT = "/home/jsj201-2/mount1/lihongjun/PaleoPRO/backend/aiAPI/output_data/entity"
IMAGE_OUTPUT = "/home/jsj201-2/mount1/lihongjun/PaleoPRO/backend/aiAPI/output_data/image"
TABLE_OUTPUT = "/home/jsj201-2/mount1/lihongjun/PaleoPRO/backend/aiAPI/output_data/table"

app = FastAPI()
logger = logging.getLogger("uvicorn")
# 定义 WebSocket 连接 URL
rag_ws_url = "ws://localhost:5200/generate_answer"
entity_ws_url = "ws://localhost:5000/entity"
image_ws_url = "ws://192.168.149.8:5100/image"   # 六号机
table_ws_url = "ws://192.168.149.3:5100/table"  # 四号机

# 配置 CORS 中间件，允许指定的来源进行跨域请求
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:5174", "http://localhost:5175"],  # 允许所有域进行跨域请求（其实只允许这三个）
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有 HTTP 方法
    allow_headers=["*"],  # 允许所有 HTTP 头
)

# 如果遇到连不上mongodb的情况，查看一下是否开启了mongodb服务
# 连接到 MongoDB 数据库
def connect_to_mongodb(uri="mongodb://paleo_user:jsj201@localhost:27018/?authSource=paleodatabase", database_name="paleodatabase"):
    client = MongoClient(uri)  # 连接到服务器上的 MongoDB 服务
    db = client[database_name]  # 选择数据库
    return db

# 定义用户登录请求的数据模型
class LoginRequest(BaseModel):
    email: str
    password: str

# 用户注册请求的数据模型
class UserRegister(BaseModel):
    username: str
    password: str
    email: str

# 定义项目数据模型
class Project(BaseModel):
    projectId: str
    projectName: str
    projectDescription: str
    normalMembers: List[dict]
    approvalMembers: List[dict]
    creatorId: str
    creatorName: str

class process_pdf_data(BaseModel):
    pdf_id:int 
    pdf_url:str

class EntityExtraRequest(BaseModel):
    pdf_id: str = Field(..., description="PDF文档唯一标识")
    predef_id: str = Field(..., description="预定义模板ID")

# 在合适的位置定义更新实体请求模型
class EntityTagInText(BaseModel):
    tag_name: str
    start: int
    end: int
    content: str

class TextItem(BaseModel):
    text: str
    text_tag: List[EntityTagInText]

class RelationEntity(BaseModel):
    entity1_name: str
    entity1_color: str
    entity2_name: str
    entity2_color: str
    relation_color: str

class RelationFromTo(BaseModel):
    text_id: str
    start: int
    end: int

class RelationItem(BaseModel):
    from_: RelationFromTo = Field(..., alias="from")  # 使用别名避免与Python关键字冲突
    to: RelationFromTo
    relation: RelationEntity

class UpdateEntityRequest(BaseModel):
    pdf_id: str
    predef_id: str
    textList: List[TextItem]
    relations: List[RelationItem]

# 定义预定义实体标签模型
class EntityTag(BaseModel):
    tag_name: str = Field(..., description="标签名称")
    tag_color: str = Field(..., description="标签颜色")
    description: Optional[str] = Field("", description="标签描述")

# 定义关系模型
class Relation(BaseModel):
    relation_id: Optional[str] = Field(None, description="关系ID")  # 添加relation_id字段
    entity1_name: str = Field(..., description="源实体名称")
    entity1_color: str = Field(..., description="源实体颜色")
    entity2_name: str = Field(..., description="目标实体名称")
    entity2_color: str = Field(..., description="目标实体颜色")
    relation_color: str = Field(..., description="关系颜色")

# 获取单个预定义模板请求模型 - 将_id改为id
class GetPredefinitionRequest(BaseModel):
    id: str = Field(..., description="模板ID")

# 创建预定义模板请求模型
class CreatePredefinitionRequest(BaseModel):
    name: str = Field(..., description="模板名称", min_length=1)
    description: Optional[str] = Field("", description="模板描述")
    ttag: List[EntityTag] = Field(default_factory=list, description="预定义实体标签列表")
    relationList: List[Relation] = Field(default_factory=list, description="关系列表")
    
    @validator('ttag', each_item=True)
    def validate_ttag(cls, v):
        if not v.tag_name:
            raise ValueError('每个标签必须有tag_name')
        if not v.tag_color:
            raise ValueError('每个标签必须有tag_color')
        return v

# 更新预定义模板请求模型 - 将_id改为id
class UpdatePredefinitionRequest(BaseModel):
    id: str = Field(..., description="模板ID")
    name: Optional[str] = Field(None, description="模板名称", min_length=1)
    description: Optional[str] = Field(None, description="模板描述")
    ttag: Optional[List[EntityTag]] = Field(None, description="预定义实体标签列表")
    relationList: Optional[List[Relation]] = Field(None, description="关系列表")
    
    @validator('ttag', each_item=True)
    def validate_ttag_update(cls, v):
        if not v.tag_name:
            raise ValueError('每个标签必须有tag_name')
        if not v.tag_color:
            raise ValueError('每个标签必须有tag_color')
        return v

# 删除预定义模板请求模型 - 将_id改为id
class DeletePredefinitionRequest(BaseModel):
    id: str = Field(..., description="模板ID")

class QuestionData(BaseModel):
    text:str
    information:list

# TextChunk数据模型定义
class TextChunk(BaseModel):
    text_id: str = Field(..., description="文本段唯一标识")
    text: str = Field(..., description="文本段内容")

# TextChunk列表模型
TextChunkList = List[TextChunk]

# 创建文本段请求模型
class CreateTextChunkRequest(BaseModel):
    pdf_id: str = Field(..., description="PDF文档唯一标识")
    textList: TextChunkList = Field(..., description="文本段列表")

# 更新文本段请求模型
class UpdateTextChunkRequest(BaseModel):
    pdf_id: str = Field(..., description="PDF文档唯一标识")
    textList: TextChunkList = Field(..., description="更新后的文本段列表")

# 查询文本段请求模型
class GetTextChunkRequest(BaseModel):
    pdf_id: str = Field(..., description="PDF文档唯一标识")

# 删除文本段请求模型
class DeleteTextChunkRequest(BaseModel):
    pdf_id: str = Field(..., description="PDF文档唯一标识")


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

@app.post("/api/user/register",summary="用户注册")
def register_user(user: UserRegister):

    db = connect_to_mongodb()
    users_collection = db["paleo_user"]  # 假设用户数据存储在 "users" 集合中
    # 检查用户名或邮箱是否已存在
    if users_collection.find_one({"username": user.username}):
        raise HTTPException(status_code=400, detail="用户名已存在")
    if users_collection.find_one({"email": user.email}):
        raise HTTPException(status_code=400, detail="邮箱已注册")

    # 构造用户数据
    new_user = {
        "username": user.username,
        "userId": "",  # 可根据需要生成唯一ID
        "password": user.password,  # 实际项目中建议加密存储
        "email": user.email,
        "type": ""
    }

    # 插入数据库
    result = users_collection.insert_one(new_user)
    return {"msg": "注册成功", "user_id": str(result.inserted_id)}

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

@app.post("/api/getFileList")
async def getFileList(request: Request):
    body = await request.json()  # 读取请求体 JSON
    project_id = body.get("project_id")  # 从请求体里取 project_id

    # 需要改成根据projcet_id从mongoDB数据库中查找

    try:
        with open(FILE_LIST, "r", encoding="utf-8") as f:
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

@app.post("/api/uploadAndGetURL")
async def uploadFileToCos(
    file: UploadFile = File(...), project_id: int = Form(...)
):
    try:
        filename = file.filename
        dirname = os.path.splitext(filename)[0]

        target_file = f"{dirname}/{filename}"
        response = client.put_object(
            Bucket=COS_CONFIG["bucket"],
            Body=file.file,
            Key=target_file,  # 例如：test1/test1.pdf
        )
        location = response.get('Location', None)
        if location:
            print(f"文件上传成功. Location: {location}")
        else:
            print("文件已上传，但响应中缺少Location参数")
            location = f"https://{COS_CONFIG['bucket']}.cos.{COS_CONFIG['region']}.myqcloud.com/{target_file}"
            print(location)
        
        update_time = datetime.now().strftime('%Y-%m-%d')

        # 后续还要上传uploader等信息
        new_items = {
            "id": 5,
            "name": filename,
            "pdf_id": 5,
            "pdf_url": location,
            "uploader": "User1",
            "updateTime": update_time,
            "imageStatus": "Unready",
            "tableStatus": "Unready",
            "entityStatus": "Unready",
            "correction": "未修正",
            "approval": "未审批"
        }


        # 先读取原文件
        try:
            with open(FILE_LIST, "r", encoding="utf-8") as f:
                data = json.load(f)
                print(data)
        except FileNotFoundError:
            data = {
                "projcet_id": None,
                "fileList": []
            }

        # 确保 fileList 是列表
        file_list = data.get("fileList", [])
        if not isinstance(file_list, list):
            file_list = []

        # 如果 new_items 是字典，包装成列表；或者根据实际传参调整
        if isinstance(new_items, dict):
            new_items = [new_items]

        # 追加新条目
        file_list.extend(new_items)

        # 赋回 data
        data["fileList"] = file_list

        print(data)

        # 写回文件
        with open(FILE_LIST, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=4)


        return {
            "status_code": 0,
            "status_msg": "上传文件成功"
        }
    except Exception as e:
        return {
            "status_code": -1,
            "status_msg": f"上传文件失败: {str(e)}"
        }

async def download_file(url: str, output_dir):
    """异步下载文件到 OUTPUT_DIR"""
    filename = os.path.join(output_dir, os.path.basename(url))
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    with open(filename, "wb") as f:
                        f.write(await resp.read())
                    print(f"[INFO] 文件已下载到 {filename}")
                     # 如果是 zip 文件，解压并删除 zip
                    if filename.lower().endswith(".zip"):
                        folder_name = os.path.splitext(os.path.basename(filename))[0]
                        extract_path = os.path.join(output_dir, folder_name)
                        os.makedirs(extract_path, exist_ok=True)

                        try:
                            with zipfile.ZipFile(filename, 'r') as zip_ref:
                                zip_ref.extractall(extract_path)
                            os.remove(filename)
                            print(f"[INFO] 已解压 zip 到 {extract_path} 并删除 {filename}")
                        except Exception as e:
                            print(f"[ERROR] 解压 {filename} 异常: {e}")
                else:
                    print(f"[ERROR] 下载失败 {url}，状态码: {resp.status}")
    except Exception as e:
        print(f"[ERROR] 下载 {url} 异常: {e}")

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
                            try:
                                data = json.loads(message)
                                # 当 status 是 ready 时，记录 location
                                if data.get("event") == "status" and data.get("status") == "ready" and "location" in data:
                                    location = data.get("location")
                                    asyncio.create_task(download_file(location,IMAGE_OUTPUT))
                                    continue
                            except json.JSONDecodeError:
                                # 如果不是 JSON，就直接跳过
                                pass
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

        print(pdf_id)
        print(pdf_url)

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
                            # 尝试解析为 JSON
                            try:
                                data = json.loads(message)
                                # 当 status 是 ready 时，记录 location
                                if data.get("event") == "status" and data.get("status") == "ready" and "location" in data:
                                    location = data.get("location")
                                    asyncio.create_task(download_file(location,ENTITY_OUTPUT))
                                    continue
                            except json.JSONDecodeError:
                                # 如果不是 JSON，就直接跳过
                                pass
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

@app.post("/api/project/entityExtra")
async def entityExtra(request: EntityExtraRequest):
    try:
        # 连接MongoDB数据库
        db = connect_to_mongodb()
        entity_extract_collection = db["entity_extract"]
        text_chunks_collection = db["text_chunks"]
        entity_predefinitions_collection = db["entity_predefinitions"]
        
        # 根据pdf_id查询text_chunks集合获取文本信息
        text_result = text_chunks_collection.find_one({"pdf_id": request.pdf_id}, {"_id": 0})
        
        if not text_result:
            return {
                "status_code": 1,
                "status_msg": "未找到对应PDF的文本数据",
                "data": {}
            }
        
        # 根据pdf_id和predef_id联合查询entity_extract集合
        entity_result = entity_extract_collection.find_one(
            {"pdf_id": request.pdf_id, "predef_id": ObjectId(request.predef_id)}, 
            {"_id": 0, "created_at": 0, "updated_at": 0}  # 不返回_id、created_at和updated_at字段
        )
        
        if not entity_result:
            # 创建新的实体标注文档
            new_entity_data = {
                "pdf_id": request.pdf_id,
                "predef_id": ObjectId(request.predef_id),
                "textList": [
                    {
                        "text_id": item["text_id"],
                        "text_tag": []  # 空的标注信息
                    } for item in text_result["textList"]
                ],
                "relations": [],  # 空的关系信息
                "created_at": datetime.now(),
                "updated_at": datetime.now()
            }
            
            # 插入到数据库
            entity_extract_collection.insert_one(new_entity_data)
            
            # 返回创建的空数据
            return {
                "status_code": 0,
                "status_msg": "未找到对应PDF和预定义模板的实体标注数据，已创建空数据",
                "data": {
                    "textList": [
                        {
                            "text": item["text"],
                            "text_tag": []
                        } for item in text_result["textList"]
                    ],
                    "relations": []
                }
            }
        
        # 获取预定义模板信息，用于解析关系
        predef_result = entity_predefinitions_collection.find_one(
            {"_id": ObjectId(request.predef_id)},
            {"_id": 0, "relationList": 1}
        )
        
        if not predef_result:
            return {
                "status_code": 1,
                "status_msg": "未找到对应预定义模板信息",
                "data": {}
            }
        
        # 创建文本ID到文本内容的映射
        text_map = {item["text_id"]: item["text"] for item in text_result["textList"]}
        
        # 创建关系ID到关系详情的映射
        relation_map = {str(rel["relation_id"]): rel for rel in predef_result["relationList"]}
        
        # 构建符合要求格式的textList
        formatted_text_list = []
        for entity_item in entity_result["textList"]:
            text_id = entity_item["text_id"]
            if text_id in text_map:
                formatted_item = {
                    "text": text_map[text_id],  # 添加文本内容
                    "text_tag": entity_item["text_tag"]  # 保留实体标注
                }
                formatted_text_list.append(formatted_item)
        
        # 构建符合要求格式的relations
        formatted_relations = []
        for relation in entity_result["relations"]:
            relation_id = str(relation["relation_id"])
            if relation_id in relation_map:
                relation_info = relation_map[relation_id]
                formatted_relation = {
                    "from": relation["from"],
                    "to": relation["to"],
                    "relation": {
                        "entity1_name": relation_info["entity1_name"],
                        "entity1_color": relation_info["entity1_color"],
                        "entity2_name": relation_info["entity2_name"],
                        "entity2_color": relation_info["entity2_color"],
                        "relation_color": relation_info["relation_color"]
                    }
                }
                formatted_relations.append(formatted_relation)

        final_result = {
            "pdf_id": request.pdf_id,
            "predef_id": request.predef_id,
            "textList": formatted_text_list,
            "relations": formatted_relations
        }
        
        return {
            "status_code": 0,
            "status_msg": "success",
            "data": final_result
        }
    except Exception as e:
        return {
            "status_code": -1,
            "status_msg": f"数据库查询失败: {str(e)}",
            "data": {}
        }

# 更新实体标签名称请求模型
class UpdateEntityTagNameRequest(BaseModel):
    predef_id: str = Field(..., description="预定义模板ID")
    old_tag_name: str = Field(..., description="旧的实体标签名称")
    new_tag_name: str = Field(..., description="新的实体标签名称")

@app.post("/api/project/updateEntityTagName")
async def updateEntityTagName(request_data: UpdateEntityTagNameRequest):
    try:
        # 连接MongoDB数据库
        db = connect_to_mongodb()
        entity_predefinitions_collection = db["entity_predefinitions"]
        entity_extract_collection = db["entity_extract"]
        
        # 验证必要参数
        if not request_data.predef_id or not request_data.old_tag_name or not request_data.new_tag_name:
            return {
                "status_code": 1,
                "status_msg": "predef_id、old_tag_name和new_tag_name都是必填参数",
                "data": {}
            }
        
        # 更新实体标签名称（在预定义集合中）
        tag_update_result = entity_predefinitions_collection.update_one(
            {"_id": ObjectId(request_data.predef_id), "ttag.tag_name": request_data.old_tag_name},
            {"$set": {"ttag.$.tag_name": request_data.new_tag_name}}
        )
        
        # 更新关系中的实体1名称（在预定义集合中）
        relation1_update_result = entity_predefinitions_collection.update_many(
            {"_id": ObjectId(request_data.predef_id), "relationList.entity1_name": request_data.old_tag_name},
            {"$set": {"relationList.$.entity1_name": request_data.new_tag_name}}
        )
        
        # 更新关系中的实体2名称（在预定义集合中）
        relation2_update_result = entity_predefinitions_collection.update_many(
            {"_id": ObjectId(request_data.predef_id), "relationList.entity2_name": request_data.old_tag_name},
            {"$set": {"relationList.$.entity2_name": request_data.new_tag_name}}
        )
        
        # 更新entity_extract集合中的tag_name字段（在抽取结果集合中）
        entity_extract_update_result = entity_extract_collection.update_many(
            {"predef_id": ObjectId(request_data.predef_id), "textList.text_tag.tag_name": request_data.old_tag_name},
            {"$set": {"textList.$[text].text_tag.$[tag].tag_name": request_data.new_tag_name}},
            array_filters=[
                {"text.text_tag.tag_name": request_data.old_tag_name},
                {"tag.tag_name": request_data.old_tag_name}
            ]
        )
        
        # 检查是否有任何更新
        if (tag_update_result.modified_count == 0 and 
            relation1_update_result.modified_count == 0 and 
            relation2_update_result.modified_count == 0 and
            entity_extract_update_result.modified_count == 0):
            return {
                "status_code": 1,
                "status_msg": "未找到对应的实体标签或没有需要更新的关系",
                "data": {}
            }
        
        return {
            "status_code": 0,
            "status_msg": "实体名称更新成功",
            "data": {
                "tag_updated_count": tag_update_result.modified_count,
                "relation1_updated_count": relation1_update_result.modified_count,
                "relation2_updated_count": relation2_update_result.modified_count,
                "entity_extract_updated_count": entity_extract_update_result.modified_count
            }
        }
    except Exception as e:
        return {
            "status_code": -1,
            "status_msg": f"更新实体名称失败: {str(e)}",
            "data": {}
        }

# 删除实体标签请求模型
class DeleteEntityTagRequest(BaseModel):
    predef_id: str = Field(..., description="预定义模板ID")
    tag_name: str = Field(..., description="要删除的实体标签名称")

@app.post("/api/project/deleteEntityTag")
async def deleteEntityTag(request_data: DeleteEntityTagRequest):
    try:
        # 连接MongoDB数据库
        db = connect_to_mongodb()
        entity_predefinitions_collection = db["entity_predefinitions"]
        entity_extract_collection = db["entity_extract"]

        # 验证predef_id是否有效
        if not ObjectId.is_valid(request_data.predef_id):
            return {
                "status_code": 1,
                "status_msg": "无效的predef_id格式",
                "data": {}
            }
        
        predef_id_obj = ObjectId(request_data.predef_id)
        
        # 1. 删除预定义集合中的实体标签
        tag_delete_result = entity_predefinitions_collection.update_one(
            {"_id": predef_id_obj},
            {"$pull": {"ttag": {"tag_name": request_data.tag_name}}}
        )
        
        # 2. 删除预定义集合中与该实体标签相关的所有关系
        relation_delete_result = entity_predefinitions_collection.update_one(
            {"_id": predef_id_obj},
            {"$pull": {
                "relationList": {
                    "$or": [
                        {"entity1_name": request_data.tag_name},
                        {"entity2_name": request_data.tag_name}
                    ]
                }
            }}
        )
        
        # 3. 收集所有需要删除的关系条件（在删除text_tag之前进行）
        # 首先获取所有包含该实体标签的text_tag的位置信息
        entity_extract_docs = entity_extract_collection.find(
            {"predef_id": predef_id_obj, "textList.text_tag.tag_name": request_data.tag_name},
            {"textList": 1}
        )
        
        # 收集所有需要删除的关系条件
        tag_positions = []
        for doc in entity_extract_docs:
            for text_item in doc.get("textList", []):
                text_id = text_item.get("text_id")
                for tag in text_item.get("text_tag", []):
                    if tag.get("tag_name") == request_data.tag_name:
                        tag_positions.append({
                            "text_id": text_id,
                            "start": tag.get("start"),
                            "end": tag.get("end")
                        })
        
        # 4. 删除entity_extract集合中与该实体标签相关的所有text_tag
        text_tag_delete_result = entity_extract_collection.update_many(
            {"predef_id": predef_id_obj},
            {"$pull": {"textList.$[].text_tag": {"tag_name": request_data.tag_name}}}
        )
        
        # 5. 删除entity_extract集合中与该实体标签相关的所有关系
        # 删除匹配的关系
        relation_delete_count = 0
        for position in tag_positions:
            # 关键修复：将text_id转换为字符串类型，确保与RelationFromTo模型中的类型一致
            text_id_str = str(position["text_id"])
            
            # 显式比较每个字段，确保匹配正确
            from_condition = {
                "from.text_id": text_id_str,  # 使用转换后的字符串类型
                "from.start": position["start"],
                "from.end": position["end"]
            }
            to_condition = {
                "to.text_id": text_id_str,  # 使用转换后的字符串类型
                "to.start": position["start"],
                "to.end": position["end"]
            }

            # 添加调试输出
            print(f"尝试删除关系，条件:")
            print(f"  from条件: text_id={text_id_str}, start={position['start']}, end={position['end']}")
            print(f"  to条件: text_id={text_id_str}, start={position['start']}, end={position['end']}")
            
            result = entity_extract_collection.update_many(
                {"predef_id": predef_id_obj},
                {"$pull": {
                    "relations": {
                        "$or": [
                            from_condition,
                            to_condition
                        ]
                    }
                }}
            )
            
            # 累加删除的关系数量
            relation_delete_count += result.modified_count
        
        # 构建返回结果
        return {
            "status_code": 0,
            "status_msg": "实体标签及相关关系删除成功",
            "data": {
                "tag_deleted": tag_delete_result.modified_count > 0,
                "relations_deleted_in_predef": relation_delete_result.modified_count,
                "text_tags_deleted": text_tag_delete_result.modified_count,
                "relations_deleted_in_entity": relation_delete_count
            }
        }
    except Exception as e:
        return {
            "status_code": 1,
            "status_msg": f"删除实体标签失败: {str(e)}",
            "data": {}
        }
# 修改实体更新接口

# 删除关系请求模型
class DeleteRelationRequest(BaseModel):
    predef_id: str = Field(..., description="预定义模板ID")
    relation_id: str = Field(..., description="要删除的关系ID")

@app.post("/api/project/deleteRelation")
async def deleteRelation(request_data: DeleteRelationRequest):
    try:
        # 连接MongoDB数据库
        db = connect_to_mongodb()
        entity_predefinitions_collection = db["entity_predefinitions"]
        entity_extract_collection = db["entity_extract"]

        # 验证predef_id是否有效
        if not ObjectId.is_valid(request_data.predef_id):
            return {
                "status_code": 1,
                "status_msg": "无效的predef_id格式",
                "data": {}
            }
        
        predef_id_obj = ObjectId(request_data.predef_id)
        
        # 验证relation_id是否有效
        if not ObjectId.is_valid(request_data.relation_id):
            return {
                "status_code": 1,
                "status_msg": "无效的relation_id格式",
                "data": {}
            }
        
        relation_id_obj = ObjectId(request_data.relation_id)
        
        # 1. 从预定义集合中删除指定的关系
        predef_delete_result = entity_predefinitions_collection.update_one(
            {"_id": predef_id_obj},
            {"$pull": {"relationList": {"relation_id": relation_id_obj}}}
        )
        
        # 2. 从抽取结果集合中删除具有相同relation_id的所有关系
        extract_delete_result = entity_extract_collection.update_many(
            {"predef_id": predef_id_obj},
            {"$pull": {"relations": {"relation_id": relation_id_obj}}}
        )
        
        # 构建返回结果
        return {
            "status_code": 0,
            "status_msg": "关系删除成功",
            "data": {
                "predef_relation_deleted": predef_delete_result.modified_count > 0,
                "extract_relations_deleted": extract_delete_result.modified_count
            }
        }
    except Exception as e:
        return {
            "status_code": 1,
            "status_msg": f"删除关系失败: {str(e)}",
            "data": {}
        }
        
@app.post("/api/project/updateEntity")
async def updateEntity(request_data: UpdateEntityRequest):
    try:
        # 连接MongoDB数据库
        db = connect_to_mongodb()
        entity_extract_collection = db["entity_extract"]
        text_chunks_collection = db["text_chunks"]
        entity_predefinitions_collection = db["entity_predefinitions"]
        
        # 根据pdf_id查询text_chunks集合，获取text_id与text的映射
        text_result = text_chunks_collection.find_one({"pdf_id": request_data.pdf_id}, {"_id": 0, "textList": 1})
        
        if not text_result:
            return {
                "status_code": 1,
                "status_msg": "未找到对应PDF的文本数据，无法关联text_id",
                "data": {}
            }
        
        # 创建text到text_id的映射
        text_to_id_map = {item["text"]: item["text_id"] for item in text_result["textList"]}
        
        # 根据predef_id查询entity_predefinitions集合，获取relation详情与relation_id的映射
        predef_result = entity_predefinitions_collection.find_one(
            {"_id": ObjectId(request_data.predef_id)},
            {"_id": 0, "relationList": 1}
        )
        
        if not predef_result:
            return {
                "status_code": 1,
                "status_msg": "未找到对应预定义模板信息，无法关联relation_id",
                "data": {}
            }
        
        # 创建relation详情到relation_id的映射
        relation_to_id_map = {}
        for rel in predef_result["relationList"]:
            # 创建一个可哈希的键，表示relation的内容
            relation_key = (
                rel["entity1_name"],
                rel["entity1_color"],
                rel["entity2_name"],
                rel["entity2_color"],
                rel["relation_color"]
            )
            relation_to_id_map[relation_key] = rel["relation_id"]
        
        # 处理textList，将text替换为text_id
        processed_textList = []
        for text_item in request_data.textList:
            if text_item.text not in text_to_id_map:
                return {
                    "status_code": 1,
                    "status_msg": f"未找到文本内容对应的text_id: {text_item.text[:50]}...",
                    "data": {}
                }
            
            text_id = text_to_id_map[text_item.text]
            processed_textList.append({
                "text_id": text_id,
                "text_tag": [tag.dict() for tag in text_item.text_tag]
            })
        
        # 处理relations，将relation详情替换为relation_id
        processed_relations = []
        for relation_item in request_data.relations:
            # 创建relation_key用于查找relation_id
            relation_key = (
                relation_item.relation.entity1_name,
                relation_item.relation.entity1_color,
                relation_item.relation.entity2_name,
                relation_item.relation.entity2_color,
                relation_item.relation.relation_color
            )
            
            if relation_key not in relation_to_id_map:
                return {
                    "status_code": 1,
                    "status_msg": f"未找到关系详情对应的relation_id: {relation_key}",
                    "data": {}
                }
            
            relation_id = relation_to_id_map[relation_key]
            processed_relations.append({
                "from": relation_item.from_.dict(),
                "to": relation_item.to.dict(),
                "relation_id": relation_id
            })
        
        # 准备更新数据
        update_data = {
            "predef_id": ObjectId(request_data.predef_id),
            "textList": processed_textList,
            "relations": processed_relations,
            "updated_at": datetime.now()
        }
        
        # 使用upsert操作 - 如果存在则更新，不存在则插入
        # 查询条件改为pdf_id和predef_id的联合查询
        result = entity_extract_collection.update_one(
            {"pdf_id": request_data.pdf_id, "predef_id": ObjectId(request_data.predef_id)},  # 查询条件
            {
                "$set": update_data,
                "$setOnInsert": {"created_at": datetime.now()}  # 仅在插入时设置创建时间
            },
            upsert=True  # 启用upsert
        )
        
        # 检查操作结果
        if result.modified_count > 0:
            status_msg = "更新成功"
        elif result.upserted_id:
            status_msg = "新建成功"
        else:
            status_msg = "数据未变更"
        
        return {
            "status_code": 0,
            "status_msg": status_msg,
            "data": {}
        }
    except Exception as e:
        return {
            "status_code": -1,
            "status_msg": f"数据库更新失败: {str(e)}",
            "data": {}
        }

# 添加获取所有预定义模板列表的接口
@app.post("/api/entity/predefinition/list")
async def get_all_predefinitions():
    try:
        # 连接到MongoDB
        db = connect_to_mongodb()
        predef_collection = db["entity_predefinitions"]
        
        # 查询所有模板
        predefined_templates = list(predef_collection.find())
        
        # 转换ObjectId为字符串
        for template in predefined_templates:
            template["_id"] = str(template["_id"])
            # 转换relation_id为字符串
            if "relationList" in template:
                for relation in template["relationList"]:
                    if "relation_id" in relation:
                        relation["relation_id"] = str(relation["relation_id"])
        
        return {
            "status_code": 0,
            "status_msg": "success",
            "data": predefined_templates
        }
    except Exception as e:
        return {
            "status_code": -1,
            "status_msg": f"获取模板列表失败: {str(e)}",
            "data": []
        }

# 修改后的创建新的预定义模板接口
@app.post("/api/entity/predefinition/create")
async def create_predefinition(request: CreatePredefinitionRequest):
    try:
        # 验证必要参数
        name = request.name
        description = request.description
        ttag = [tag.dict() for tag in request.ttag]
        relationList = [rel.dict() for rel in request.relationList]
        
        if not name:
            return {
                "status_code": -1,
                "status_msg": "模板名称不能为空",
                "data": {}
            }
        
        # 连接到MongoDB
        db = connect_to_mongodb()
        predef_collection = db["entity_predefinitions"]
        
        # 检查模板名称是否已存在
        if predef_collection.find_one({"name": name}):
            return {
                "status_code": -1,
                "status_msg": "模板名称已存在",
                "data": {}
            }
        
        # 为每个关系生成relation_id
        from bson import ObjectId
        for relation in relationList:
            relation["relation_id"] = ObjectId()
        
        # 创建模板数据
        predef_data = {
            "name": name,
            "description": description,
            "ttag": ttag,
            "relationList": relationList,
            "created_at": datetime.now(),
            "updated_at": datetime.now()
        }
        
        # 插入数据
        result = predef_collection.insert_one(predef_data)
        
        # 返回创建的模板（包含_id和转换后的relation_id）
        predef_data["_id"] = str(result.inserted_id)
        for relation in predef_data["relationList"]:
            relation["relation_id"] = str(relation["relation_id"])
        
        return {
            "status_code": 0,
            "status_msg": "模板创建成功",
            "data": predef_data
        }
    except Exception as e:
        return {
            "status_code": -1,
            "status_msg": f"创建模板失败: {str(e)}",
            "data": {}
        }

# 修改后的更新预定义模板接口
@app.post("/api/entity/predefinition/update")
async def update_predefinition(request: UpdatePredefinitionRequest):
    try:
        # 获取请求参数 - 使用id而不是_id
        predef_id = request.id
        
        if not predef_id:
            return {
                "status_code": -1,
                "status_msg": "缺少模板ID参数",
                "data": {}
            }
        
        # 连接到MongoDB
        db = connect_to_mongodb()
        predef_collection = db["entity_predefinitions"]
        
        # 准备更新数据
        update_data = {}
        if request.name is not None:
            update_data["name"] = request.name
        if request.description is not None:
            update_data["description"] = request.description
        if request.ttag is not None:
            update_data["ttag"] = [tag.dict() for tag in request.ttag]
        if request.relationList is not None:
            relationList = [rel.dict() for rel in request.relationList]
            # 为没有relation_id的关系生成新的relation_id
            from bson import ObjectId
            for relation in relationList:
                if not relation.get("relation_id"):
                    relation["relation_id"] = ObjectId()
                else:
                    # 如果提供了relation_id，将其转换为ObjectId类型
                    relation["relation_id"] = ObjectId(relation["relation_id"])
            update_data["relationList"] = relationList
        
        update_data["updated_at"] = datetime.now()  # 更新时间戳
        
        # 执行更新
        from bson import ObjectId
        try:
            result = predef_collection.update_one(
                {"_id": ObjectId(predef_id)},
                {"$set": update_data}
            )
        except:
            # 如果不是有效的ObjectId格式，尝试以字符串形式查询
            result = predef_collection.update_one(
                {"_id": predef_id},
                {"$set": update_data}
            )
        
        if result.modified_count > 0:
            # 获取更新后的模板
            try:
                updated_predef = predef_collection.find_one({"_id": ObjectId(predef_id)})
            except:
                updated_predef = predef_collection.find_one({"_id": predef_id})
            
            if updated_predef:
                updated_predef["_id"] = str(updated_predef["_id"])
                # 转换relation_id为字符串
                if "relationList" in updated_predef:
                    for relation in updated_predef["relationList"]:
                        if "relation_id" in relation:
                            relation["relation_id"] = str(relation["relation_id"])
                return {
                    "status_code": 0,
                    "status_msg": "模板更新成功",
                    "data": updated_predef
                }
        
        return {
            "status_code": -1,
            "status_msg": "未找到指定模板或更新失败",
            "data": {}
        }
    except Exception as e:
        return {
            "status_code": -1,
            "status_msg": f"更新模板失败: {str(e)}",
            "data": {}
        }

# 修改后的删除预定义模板接口
@app.post("/api/entity/predefinition/delete",description="删除预定义模板")
async def delete_predefinition(request: DeletePredefinitionRequest):
    try:
        # 获取请求参数 - 使用id而不是_id
        predef_id = request.id
        
        if not predef_id:
            return {
                "status_code": -1,
                "status_msg": "缺少模板ID参数",
                "data": {}
            }
        
        # 连接到MongoDB
        db = connect_to_mongodb()
        predef_collection = db["entity_predefinitions"]
        entity_extract_collection = db["entity_extract"]
        
        # 执行删除操作
        from bson import ObjectId
        try:
            # 将预定义ID转换为ObjectId格式
            object_id = ObjectId(predef_id)
            
            # 1. 删除预定义模板
            predef_result = predef_collection.delete_one({"_id": object_id})
            
            # 2. 删除与该模板关联的所有实体抽取数据
            entity_result = entity_extract_collection.delete_many({"predef_id": object_id})
            
        except:
            # 如果不是有效的ObjectId格式，尝试以字符串形式查询
            predef_result = predef_collection.delete_one({"_id": predef_id})
            entity_result = entity_extract_collection.delete_many({"predef_id": predef_id})
        
        if predef_result.deleted_count > 0:
            return {
                "status_code": 0,
                "status_msg": "模板删除成功",
                "data": {
                    "deleted_template_count": predef_result.deleted_count,
                    "deleted_entity_extract_count": entity_result.deleted_count
                }
            }
        else:
            return {
                "status_code": -1,
                "status_msg": "未找到指定模板或删除失败",
                "data": {}
            }
    except Exception as e:
        return {
            "status_code": -1,
            "status_msg": f"删除模板失败: {str(e)}",
            "data": {}
        }

# 处理bio_entity.txt文件并保存到数据库的接口，这个接口后面会改，目的是为了将文本格式进行保存
@app.post("/api/text_chunks/create",description="结果转文本并存储")
async def process_bio_entity():
    try:
        # 读取bio_entity.txt文件
        file_path = '/home/lujie/mount/backend/aiAPI/mongodb_table/bio_entity.txt'
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = [line.strip() for line in f.readlines()]
        
        # 将这些行按空行分隔成多个文本段
        text_segments = []
        current_segment = []
        for line in lines:
            if line:  # 如果不是空行，添加到当前文本段
                current_segment.append(line)
            else:  # 如果是空行，保存当前文本段并开始新的文本段
                if current_segment:
                    text_segments.append(current_segment)
                    current_segment = []
        # 保存最后一个文本段
        if current_segment:
            text_segments.append(current_segment)
        
        # 处理每个文本段，提取单词并组合成连贯的文本
        processed_segments = []
        for segment in text_segments:
            words = [line.split()[0] for line in segment if line.split()]  # 确保行不为空且有足够的字段
            text_content = ' '.join(words)
            if text_content:  # 确保文本内容不为空
                processed_segments.append(text_content)
        
        # 准备数据
        pdf_id = str(uuid.uuid4())
        text_list = []
        for text_content in processed_segments:
            text_id = str(uuid.uuid4())
            text_list.append(TextChunk(
                text_id=text_id,
                text=text_content
            ))
        
        # 使用现有的create_text_chunks逻辑保存数据
        db = connect_to_mongodb()
        text_chunks_collection = db["text_chunks"]
        
        # 检查是否已存在该pdf_id的记录（理论上不会发生，因为使用了新的uuid）
        existing_chunk = text_chunks_collection.find_one({"pdf_id": pdf_id})
        if existing_chunk:
            return JSONResponse(
                status_code=400,
                content={
                    "status_code": -1,
                    "status_msg": "该PDF文档已存在文本段记录",
                    "data": {}
                }
            )
        
        # 创建新的文本段记录
        new_chunk = {
            "pdf_id": pdf_id,
            "textList": [chunk.dict() for chunk in text_list]
        }
        
        result = text_chunks_collection.insert_one(new_chunk)
        
        return {
            "status_code": 0,
            "status_msg": "bio_entity.txt文件处理成功并保存到数据库",
            "data": {
                "_id": str(result.inserted_id),
                "pdf_id": pdf_id,
                "processed_segments": len(processed_segments),
                "total_lines": len(lines)
            }
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status_code": -1,
                "status_msg": f"处理bio_entity.txt文件失败: {str(e)}",
                "data": {}
            }
        )

# 查询文本段接口
@app.post("/api/text_chunks/get")
async def get_text_chunks(request: GetTextChunkRequest):
    try:
        db = connect_to_mongodb()
        text_chunks_collection = db["text_chunks"]
        
        # 根据pdf_id查询文本段
        chunk = text_chunks_collection.find_one({"pdf_id": request.pdf_id})
        if not chunk:
            return JSONResponse(
                status_code=404,
                content={
                    "status_code": -1,
                    "status_msg": "未找到该PDF文档的文本段记录",
                    "data": {}
                }
            )
        
        # 转换ObjectId为字符串
        chunk["_id"] = str(chunk["_id"])
        
        return {
            "status_code": 0,
            "status_msg": "文本段查询成功",
            "data": chunk
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status_code": -1,
                "status_msg": f"文本段查询失败: {str(e)}",
                "data": {}
            }
        )

# 更新文本段接口
@app.post("/api/text_chunks/update")
async def update_text_chunks(request: UpdateTextChunkRequest):
    try:
        db = connect_to_mongodb()
        text_chunks_collection = db["text_chunks"]
        
        # 检查是否存在该pdf_id的记录
        existing_chunk = text_chunks_collection.find_one({"pdf_id": request.pdf_id})
        if not existing_chunk:
            return JSONResponse(
                status_code=404,
                content={
                    "status_code": -1,
                    "status_msg": "未找到该PDF文档的文本段记录",
                    "data": {}
                }
            )
        
        # 更新文本段记录
        update_data = {
            "textList": [chunk.dict() for chunk in request.textList]
        }
        
        text_chunks_collection.update_one(
            {"pdf_id": request.pdf_id},
            {"$set": update_data}
        )
        
        return {
            "status_code": 0,
            "status_msg": "文本段更新成功",
            "data": {}
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status_code": -1,
                "status_msg": f"文本段更新失败: {str(e)}",
                "data": {}
            }
        )

# 删除文本段接口
@app.post("/api/text_chunks/delete")
async def delete_text_chunks(request: DeleteTextChunkRequest):
    try:
        db = connect_to_mongodb()
        text_chunks_collection = db["text_chunks"]
        
        # 检查是否存在该pdf_id的记录
        existing_chunk = text_chunks_collection.find_one({"pdf_id": request.pdf_id})
        if not existing_chunk:
            return JSONResponse(
                status_code=404,
                content={
                    "status_code": -1,
                    "status_msg": "未找到该PDF文档的文本段记录",
                    "data": {}
                }
            )
        
        # 删除文本段记录
        text_chunks_collection.delete_one({"pdf_id": request.pdf_id})
        
        return {
            "status_code": 0,
            "status_msg": "文本段删除成功",
            "data": {}
        }
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "status_code": -1,
                "status_msg": f"文本段删除失败: {str(e)}",
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

#把RAG模块独立出来 ， url为rag_ws_url 5200端口 6.6  
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

async def main():
    test_url = "http://paleodb-1306565154.cos.ap-shanghai.myqcloud.com/ExImage/代旭-2018-JP-Ammonoid.zip"  # 替换成你真实的文件链接
    await download_file(test_url,IMAGE_OUTPUT)

if __name__ == "__main__":
    asyncio.run(main())

#  curl -N -X POST http://localhost:8000/api/QAsystemStream -H "Content-Type: application/json" -d '{"post": {"text": "你好", "information": []}}'

# curl -X POST http://localhost:8000/api/QAsystem -H "Content-Type: application/json" -d '{"question": "你好"}'

# curl -X POST http://localhost:8000/api/project/imageExtra

# 查看nohup后台运行端口命令
# ps aux | grep uvicorn

# nohup 后台启动命令
# nohup uvicorn main:app --host 0.0.0.0 --port 8000 &
# uvicorn main:app --reload
# 本环境所用 conda fastapi