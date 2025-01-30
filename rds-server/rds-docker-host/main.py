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
from SystemInfo import router as systeminfo_router
from Docker import router as docker_router
app.include_router(systeminfo_router)
app.include_router(docker_router)
