from .config import settings
from .database import Base, engine, SessionLocal
from . import models, schemas, auth

# 버전 정보
__version__ = "1.0.0"

# 앱 초기화 함수
def init_app():
    # 데이터베이스 테이블 생성
    Base.metadata.create_all(bind=engine)