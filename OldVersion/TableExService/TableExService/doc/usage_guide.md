# PaleoGPTEntityExService 食用指南

## 系统架构

```
EntityExService/
├── app.py               # 主应用入口
├── config/              # 配置管理
│   ├── config.py        # 配置加载模块
│   └── .env             # 环境变量配置文件
├── util/                # 工具模块
│   ├── websocket_manager.py  # WebSocket管理
│   ├── process_manager.py    # 处理流程管理
│   ├── pdf_handler.py        # PDF处理工具
│   ├── cos_storage.py        # 云存储工具
│   └── file_copy.py          # 文件复制工具
├── log/                 # 日志管理
│   ├── log_manager.py   # 日志管理工具
│   └── paleoGPTEntityExServicexyb.log  # 日志文件
├── fontendTest/         # 前端测试页面
│   └── ws_test.html     # WebSocket测试页面
├── data/                # 数据输出目录
└── inputPdf/            # PDF输入目录
```
