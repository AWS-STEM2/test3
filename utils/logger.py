import logging
import os
from datetime import datetime

# 로그 디렉토리 생성
if not os.path.exists('logs'):
    os.makedirs('logs')

# 로거 설정
logger = logging.getLogger("fastapi_app")
logger.setLevel(logging.INFO)

# 파일 핸들러
file_handler = logging.FileHandler(
    f"logs/{datetime.now().strftime('%Y-%m-%d')}.log"
)
file_handler.setFormatter(
    logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
)
logger.addHandler(file_handler)