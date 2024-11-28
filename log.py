import logging
from datetime import datetime

current_time_str = datetime.now().strftime("%Y-%m-%d_%H_%M_%S")
LOG_PATH = "./log/"
# 配置日志记录器
logging.basicConfig(
    level=logging.INFO,  # 设置日志级别
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',  # 设置日志格式
    handlers=[
        logging.FileHandler(LOG_PATH + current_time_str + ".log",encoding='utf-8'),  # 将日志写入文件
        logging.StreamHandler()  # 同时将日志输出到控制台（可选）
    ],
    encoding='utf-8'
)

logger = logging.getLogger(__name__)