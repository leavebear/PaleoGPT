"""
配置管理模块，用于加载和提供环境变量
"""
import os
from pathlib import Path
from dotenv import load_dotenv, set_key
import logging
import sys

# 添加项目根目录到sys.path，确保能导入log模块
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# 导入日志管理模块
from entity_log.log_manager import setup_logging, roll_log_file

# 加载.env文件中的环境变量
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# 配置常量
COS_CONFIG = {
    "secret_id": os.getenv('SECRET_ID'),
    "secret_key": os.getenv('SECRET_KEY'),
    "region": os.getenv('REGION'),
    "token": os.getenv('TOKEN'),
    "scheme": os.getenv('SCHEME'),
    "bucket": os.getenv('BUCKET'),
}

PDF_CONFIG = {
    "pdf_url": os.getenv('PDF_URL'),
    "pdf_id": os.getenv('PDF_ID', "01xybTest"),
    "input_pdf_dir": os.getenv('INPUT_PDF_DIR', "./inputPdf/"),
    "data_dir": os.getenv('DATA_DIR', "./data/"),
}

LOG_CONFIG = {
    "log_file": os.getenv('LOG_FILE', 'log/paleoGPTEntityExServicexyb.log'),
    "log_level": os.getenv('LOG_LEVEL', 'INFO'),
}

# 使用日志管理模块初始化日志
logger = setup_logging(LOG_CONFIG, clear_on_startup=True)

def update_config(key, value):
    """
    更新配置项，同时更新.env文件和内存中的配置
    
    Args:
        key: 配置项名称
        value: 配置项值
        
    Returns:
        bool: 更新是否成功
    """
    try:
        # 更新.env文件
        set_key(env_path, key, value)
        
        # 更新环境变量
        os.environ[key] = value
        
        # 更新内存中的配置
        if key in ["PDF_URL", "PDF_ID", "INPUT_PDF_DIR", "DATA_DIR"]:
            PDF_CONFIG[key.lower()[4:]] = value
            logger.info(f"已更新配置: {key}={value}")
        
        # 检查并滚动日志文件
        roll_log_file(LOG_CONFIG["log_file"])
        
        return True
    except Exception as e:
        logger.error(f"更新配置失败: {str(e)}")
        return False 