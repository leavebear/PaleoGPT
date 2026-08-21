# PaleoGPTQAsystemService 食用指南

## 系统架构

```
QAsystem/
├── app.py               # 主应用入口
├── qa_config/              # 配置管理
│   ├── config.py        # 配置加载模块
│   └── .env             # 环境变量配置文件
├── qa_util/                # 工具模块
│   ├── websocket_manager.py  # WebSocket管理
│   ├── data_embadding.py     # 向量嵌入工具
│   ├── knowledge_base.py     # 知识索引工具
│   ├── pdf2txt.py            # pdf转txt工具（弃用）
├── qa_log/               # 日志管理
│   ├── log_manager.py    # 日志管理工具
│   └── paleoGPT-RAG.log  # 日志文件
├── docs/                 # 测试知识库
├── index/                # 向量索引存储文件夹
├── model/                # 文本嵌入向量模型
├── nltk_data             # bm25索引工具数据
└── triviaqa-unfiltered/  # QA测试数据集
```
