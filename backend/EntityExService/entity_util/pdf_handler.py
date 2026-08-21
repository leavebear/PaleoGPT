"""
PDF处理相关功能
"""
import os
import requests
import subprocess
from pathlib import Path
from entity_config.config import PDF_CONFIG, logger

conmmand_sh = '/home/jsj201-2/mount1/xyb/distantSupervision/dataprocess/chouqu.sh'

def download_pdf(url, local_dir):
    """
    下载PDF文件到本地目录
    
    Args:
        url: PDF文件URL
        local_dir: 本地存储目录
        
    Returns:
        tuple: (成功标志, 本地文件路径)
    """
    try:
        # 确保目录存在
        os.makedirs(local_dir, exist_ok=True)
        
        # 从URL获取文件名
        file_name = os.path.basename(url)
        local_path = os.path.join(local_dir, file_name)
        
        # 下载文件
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            logger.info(f"PDF文件已下载到: {local_path}")
            return True, local_path
        else:
            logger.error(f"下载PDF失败，状态码: {response.status_code}")
            return False, None
    except Exception as e:
        logger.error(f"下载PDF时发生错误: {str(e)}")
        return False, None


def process_pdf(input_dir):
    """
    处理PDF文件，调用外部脚本
    
    Args:
        input_dir: 包含PDF文件的目录
        
    Returns:
        bool: 处理是否成功
    """
    try:
        # 获取绝对路径
        abs_input_dir = os.path.abspath(input_dir)
        
        # 构建命令
        command = f"bash {conmmand_sh} {abs_input_dir}"
        
        logger.info(f"执行命令: {command}")
        result = subprocess.run(
            command, 
            shell=True, 
            capture_output=True, 
            text=True, 
            check=True
        )
        
        # 记录输出
        logger.info(f"命令执行成功，输出: {result.stdout}")
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"命令执行失败: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"处理PDF时发生错误: {str(e)}")
        return False 