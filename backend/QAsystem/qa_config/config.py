"""
配置管理模块，用于加载和提供环境变量
"""
import os
from pathlib import Path
from dotenv import load_dotenv, set_key
import logging

# 加载.env文件中的环境变量
env_path = Path(__file__).parent.parent / "config" / ".env"
load_dotenv(dotenv_path=env_path)


LOG_CONFIG = {
    "log_file": os.getenv('LOG_FILE', 'log/paleoGPT-RAG.log'),
    "log_level": os.getenv('LOG_LEVEL', 'INFO'),
}

# 初始化日志配置
def setup_logging():
    """设置日志配置"""
    logging.basicConfig(
        filename=LOG_CONFIG["log_file"],
        level=getattr(logging, LOG_CONFIG["log_level"]),
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    return logging.getLogger(__name__)

logger = setup_logging()

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
        
        return True
    except Exception as e:
        logger.error(f"更新配置失败: {str(e)}")
        return False 