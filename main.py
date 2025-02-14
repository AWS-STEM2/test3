from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

app = FastAPI()

# 정적 파일 설정 (CSS, JS, 이미지 등)
app.mount("/static", StaticFiles(directory="static"), name="static")

# 템플릿 설정
templates = Jinja2Templates(directory="templates")

# 라우트 설정
@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {"request": request, "title": "홈페이지"}
    )