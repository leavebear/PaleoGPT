import os
import sys
import shutil

from entity_config.config import logger

def copy_entity_annotation_file():
    """
    将全实体标注.txt文件复制到paleoGPTEntityExService/data目录下
    
    Returns:
        bool: 复制是否成功
    """
    try:
        # 源文件路径
        source_file = '/home/jsj201-2/mount1/xyb/distantSupervision/dataprocess/古生物远程监督/远程监督数据集/zidongbiaozhu/strataAndFossil/全实体标注.txt'
        
        # 目标目录
        target_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data')
        target_file = os.path.join(target_dir, '全实体标注.txt')
        
        # 确保目标目录存在
        os.makedirs(target_dir, exist_ok=True)
        
        # 复制文件
        shutil.copy2(source_file, target_file)
        logger.info(f"成功将[全实体标注.txt]文件复制到 {target_file}")
        return True
    except Exception as e:
        logger.error(f"复制[全实体标注.txt]文件时出错: {str(e)}")
        return False

if __name__ == "__main__":
    # 测试函数
    copy_entity_annotation_file() 