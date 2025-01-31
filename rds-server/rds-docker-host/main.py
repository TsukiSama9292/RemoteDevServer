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
from Info import router as info_router
from Container import router as container_router
from Image import router as image_router
app.include_router(info_router, prefix="/info")
app.include_router(container_router, prefix="/container")
app.include_router(image_router, prefix="/image")