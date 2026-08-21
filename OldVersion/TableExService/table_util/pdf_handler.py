"""
PDF处理相关功能
"""
import asyncio
import os
import requests
import subprocess
from pathlib import Path
from table_config.config import PDF_CONFIG, logger

conmmand_sh = '/home/jsj201-11/mount1/zjc/pdf2table.sh'

def download_pdf(url, base_dir):
    """
    下载PDF文件到固定目录 /home/jsj201-11/mount1/zjc/data/pdf/锰矿文献/
    
    Args:
        url: PDF文件URL
        base_dir: 兼容原有参数（实际已固定路径，此参数可忽略）
        
    Returns:
        tuple: (成功标志, 本地文件路径)
    """
    try:
        # 固定PDF下载根目录
        fixed_download_root = "/home/jsj201-11/mount1/zjc/data/pdf/锰矿文献/"
        # 确保固定目录存在
        os.makedirs(fixed_download_root, exist_ok=True)
        
        # 从URL获取文件名（用于生成保存的文件名）
        file_name = os.path.basename(url)
        pdf_name = os.path.splitext(file_name)[0]

        # 最终文件路径：固定目录 + pdf_name.pdf
        local_path = os.path.join(fixed_download_root, f"{pdf_name}.pdf")
        
        # 下载文件
        response = requests.get(url)
        if response.status_code == 200:
            with open(local_path, 'wb') as f:
                f.write(response.content)
            logger.info(f"PDF文件已下载到: {local_path}")
            # 返回固定目录（用于后续处理）
            return True, fixed_download_root
        else:
            logger.error(f"下载PDF失败，状态码: {response.status_code}")
            return False, None
    except Exception as e:
        logger.error(f"下载PDF时发生错误: {str(e)}")
        return False, None


async def process_pdf(input_dir):
    """
    处理PDF文件，调用外部脚本
    
    Args:
        input_dir: 包含PDF文件的目录（固定为/home/jsj201-11/mount1/zjc/data/pdf/锰矿文献/）
        
    Returns:
        bool: 处理是否成功
    """
    try:
        # 获取绝对路径
        abs_input_dir = os.path.abspath(input_dir)
        # abs_input_dir ="60912.pdf"
        # 构建命令
        # 输入为pdf所在文件夹的路径 输出为BIO文件
        print("conmmand_sh:=============================", conmmand_sh)
        print(abs_input_dir)
        command = f'bash {conmmand_sh} "{abs_input_dir}"'
        logger.info(f"执行命令: {command}")
        # 让command和心跳程序并行执行
        process = await asyncio.create_subprocess_shell(
            command,
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )

        stdout, stderr = await process.communicate()

        if process.returncode == 0:
            logger.info(f"命令执行成功，输出: {stdout.decode().strip()}")
            return True
        else:
            logger.error(f"命令执行失败，错误信息: {stderr.decode().strip()}")
            return False
        
    except subprocess.CalledProcessError as e:
        logger.error(f"命令执行失败: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"处理PDF时发生错误: {str(e)}")
        return False 