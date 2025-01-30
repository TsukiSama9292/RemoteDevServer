# main.py
from fastapi import FastAPI, Depends, APIRouter
import logging

# 設置日誌級別
logging.basicConfig(level=logging.INFO)

app = FastAPI(
    root_path="/",
    docs_url=None,        # 關閉 docs
    redoc_url=None,       # 關閉 ReDoc
    openapi_url=None,     # 關閉 OpenAPI JSON
    debug=False           # 關閉 debug 模式
)
import SystemInfo
import Docker
from SystemInfo import router as login_router
from Docker import router as AI_Agent_router
app.include_router(login_router)
app.include_router(AI_Agent_router)

@app.on_event("startup")
def startup():
    print("Docker Host is running.")

@app.on_event("shutdown")
def shutdown():
    print("Docker Host is shutting down.")