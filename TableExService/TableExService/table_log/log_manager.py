"""
日志管理模块：负责日志的初始化、清空和滚动等功能
"""
import os
import logging
import time
from pathlib import Path


def clear_log_file(log_file_path):
    """
    清空日志文件内容
    
    Args:
        log_file_path: 日志文件路径
    """
    # 确保日志目录存在
    log_dir = os.path.dirname(log_file_path)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # 清空日志文件（如果存在）
    if os.path.exists(log_file_path):
        with open(log_file_path, 'w', encoding='utf-8') as f:
            f.write(f"# 日志已于 {time.strftime('%Y-%m-%d %H:%M:%S')} 清空\n")
        return True
    # 创建新日志文件
    else:
        try:
            with open(log_file_path, 'w', encoding='utf-8') as f:
                f.write(f"# 日志文件创建于 {time.strftime('%Y-%m-%d %H:%M:%S')}\n")
            return True
        except Exception as e:
            print(f"创建日志文件失败: {e}")
            return False


def roll_log_file(log_file_path, max_size_kb=1024):
    """
    日志滚动：当日志文件超过指定大小时，删除一半的内容
    
    Args:
        log_file_path: 日志文件路径
        max_size_kb: 最大日志大小（KB），默认1MB
    """
    if not os.path.exists(log_file_path):
        return False
    
    # 检查文件大小
    file_size_kb = os.path.getsize(log_file_path) / 1024
    if file_size_kb < max_size_kb:
        return False
    
    try:
        # 读取文件内容
        with open(log_file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # 保留后一半的行
        half_point = len(lines) // 2
        remaining_lines = lines[half_point:]
        
        # 写回文件
        with open(log_file_path, 'w', encoding='utf-8') as f:
            f.write(f"# 日志已于 {time.strftime('%Y-%m-%d %H:%M:%S')} 滚动，删除前一半内容\n")
            f.writelines(remaining_lines)
        
        return True
    except Exception as e:
        print(f"日志滚动失败: {e}")
        return False


def setup_logging(log_config, clear_on_startup=True):
    """
    设置日志配置
    
    Args:
        log_config: 日志配置字典，包含 log_file 和 log_level
        clear_on_startup: 是否在启动时清空日志
        
    Returns:
        logger: 日志记录器
    """
    log_file = log_config.get("log_file", "log/paleoGPTEntityExServicexyb.log")
    log_level = log_config.get("log_level", "INFO")
    
    # 确保日志目录存在
    log_dir = os.path.dirname(log_file)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir, exist_ok=True)
    
    # 是否清空日志
    if clear_on_startup:
        clear_log_file(log_file)
    
    # 检查并滚动日志
    roll_log_file(log_file)
    
    # 设置日志配置
    logging.basicConfig(
        filename=log_file,
        level=getattr(logging, log_level),
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    return logging.getLogger(__name__)


def get_logger(name=None):
    """
    获取一个日志记录器
    
    Args:
        name: 日志记录器名称
    
    Returns:
        logger: 日志记录器
    """
    return logging.getLogger(name)


# 创建用于检查日志大小和自动滚动的装饰器
def check_log_size(log_file_path, max_size_kb=1024):
    """
    装饰器：检查日志大小并在需要时执行滚动
    
    Args:
        log_file_path: 日志文件路径
        max_size_kb: 最大日志大小（KB）
    """
    def decorator(func):
        def wrapper(*args, **kwargs):
            # 执行原始函数
            result = func(*args, **kwargs)
            
            # 检查并滚动日志
            roll_log_file(log_file_path, max_size_kb)
            
            return result
        return wrapper
    return decorator 