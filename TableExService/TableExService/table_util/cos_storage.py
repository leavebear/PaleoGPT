"""
腾讯云COS存储相关功能
"""
import os
from qcloud_cos import (
    CosConfig,
    CosS3Client,
    CosServiceError,
    CosClientError,
)



from qcloud_cos.cos_threadpool import SimpleThreadPool
from table_config.config import COS_CONFIG, logger

# 创建COS客户端
def create_cos_client():
    """创建COS客户端"""
    config = CosConfig(
        Region=COS_CONFIG["region"],
        SecretId=COS_CONFIG["secret_id"],
        SecretKey=COS_CONFIG["secret_key"],
        Token=COS_CONFIG["token"],
        Scheme=COS_CONFIG["scheme"]
    )
    return CosS3Client(config)

# 初始化全局客户端
client = create_cos_client()

def download_file(key, dest_path):
    """
    从COS下载文件
    
    Args:
        key: COS中的文件键名
        dest_path: 本地目标路径
        
    Returns:
        bool: 下载是否成功
    """
    for i in range(0, 10):  # 重试10次
        try:
            response = client.download_file(
                Bucket=COS_CONFIG["bucket"],
                Key=key,
                DestFilePath=dest_path
            )
            return True
        except (CosClientError, CosServiceError) as e:
            logger.info(f"下载失败，尝试重试: {e}")
    
    return False

def upload_file(local_path, key):
    """
    上传单个文件到COS
    
    Args:
        local_path: 本地文件路径
        key: COS目标键名
        
    Returns:
        str or None: 上传成功返回文件的Location，失败返回None
    """
    for i in range(0, 10):  # 重试10次
        try:
            response = client.upload_file(
                Bucket=COS_CONFIG["bucket"],
                Key=key,
                LocalFilePath=local_path
            )
            location = response.get('Location', None)
            if location:
                logger.info(f"文件上传成功. Location: {location}")
                return location
            else:
                logger.info("文件已上传，但响应中缺少Location参数")
                location = f"https://{COS_CONFIG['bucket']}.cos.{COS_CONFIG['region']}.myqcloud.com/{key}"
                return location
        except (CosClientError, CosServiceError) as e:
            logger.info(f"上传失败，尝试重试: {e}")
    
    return None

def upload_directory(cos_prefix, local_dir):
    """
    上传目录下的所有文件到COS
    
    Args:
        cos_prefix: COS中的前缀路径
        local_dir: 本地目录路径
        
    Returns:
        bool: 是否所有文件都上传成功
    """
    bucket = COS_CONFIG["bucket"]
    g = os.walk(local_dir)
    pool = SimpleThreadPool()
    
    for path, dir_list, file_list in g:
        for file_name in file_list:
            # 文件在物理系统中的真实路径
            src_key = os.path.join(path, file_name)
            logger.info(f"源文件路径: {src_key}")
            
            # 构建COS对象键名
            cos_object_key = cos_prefix.strip('/') + "/" + os.path.basename(src_key)
            logger.info(f"COS对象键名: {cos_object_key}")
            
            # 判断COS上文件是否存在
            exists = False
            try:
                response = client.head_object(Bucket=bucket, Key=cos_object_key)
                exists = True
            except CosServiceError as e:
                if e.get_status_code() == 404:
                    exists = False
                else:
                    logger.info("发生错误，重新上传")
            
            if not exists:
                logger.info(f"文件 {cos_object_key} 在COS中不存在，上传")
                pool.add_task(client.upload_file, bucket, cos_object_key, src_key)
    
    pool.wait_completion()
    result = pool.get_result()
    
    if not result['success_all']:
        logger.info("未能成功上传所有文件，需要重试")
        return False
    
    return True

def create_directory(dir_path):
    """
    在COS中创建目录
    
    Args:
        dir_path: 要创建的目录路径
        
    Returns:
        bool: 是否创建成功
    """
    try:
        response = client.put_object(
            Bucket=COS_CONFIG["bucket"],
            Key=dir_path,
            Body=b''
        )
        return True
    except (CosClientError, CosServiceError) as e:
        logger.error(f"创建目录失败: {e}")
        return False 
    
def main():
    location = upload_file("/home/jsj201-2/mount1/lihongjun/PaleoPRO/backend/EntityExService/entity_util/test.txt","test/test.txt")
    print(location)

if __name__ == "__main__":
    main()