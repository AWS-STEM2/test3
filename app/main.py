from fastapi import FastAPI, Depends, HTTPException, File, UploadFile
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import os
from datetime import timedelta
from typing import List
import aiofiles
from . import models, schemas, auth, database
from .config import settings
from .middleware import LoggingMiddleware
from .utils.logger import logger

app = FastAPI()

# 미들웨어 추가
app.add_middleware(LoggingMiddleware)

# 정적 파일 서빙
app.mount("/static", StaticFiles(directory="static"), name="static")

# 데이터베이스 초기화
models.Base.metadata.create_all(bind=database.engine)

# 인증 관련 엔드포인트
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(database.get_db)
):
    user = db.query(models.User).filter(models.User.email == form_data.username).first()
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=400,
            detail="Incorrect email or password"
        )
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

# 파일 업로드 엔드포인트
@app.post("/uploadfile/")
async def create_upload_file(
    file: UploadFile = File(...),
    current_user: models.User = Depends(auth.get_current_user)
):
    if not os.path.exists(settings.UPLOAD_DIR):
        os.makedirs(settings.UPLOAD_DIR)
    
    file_location = f"{settings.UPLOAD_DIR}/{file.filename}"
    async with aiofiles.open(file_location, 'wb') as out_file:
        content = await file.read()
        await out_file.write(content)
    
    return {"filename": file.filename}

# 아이템 CRUD 엔드포인트
@app.post("/items/", response_model=schemas.Item)
async def create_item(
    item: schemas.ItemCreate,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    db_item = models.Item(**item.dict(), owner_id=current_user.id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    logger.info(f"Item created: {db_item.id} by user {current_user.email}")
    return db_item

@app.get("/items/", response_model=List[schemas.Item])
async def read_items(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(database.get_db),
    current_user: models.User = Depends(auth.get_current_user)
):
    items = db.query(models.Item).filter(
        models.Item.owner_id == current_user.id
    ).offset(skip).limit(limit).all()
    return items

# 사용자 관련 엔드포인트
@app.post("/users/", response_model=schemas.User)
async def create_user(user: schemas.UserCreate, db: Session = Depends(database.get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    hashed_password = auth.get_password_hash(user.password)
    db_user = models.User(email=user.email, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user