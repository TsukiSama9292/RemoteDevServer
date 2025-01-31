# Image.py
import asyncio
import json
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import docker
import os
router = APIRouter()
client = docker.from_env()


# 拉取鏡像
class PullImage(BaseModel):
    image: str
@router.post("/pull_image")
async def pull_image(request: PullImage):
    try:
        client.images.get(request.image)
        return JSONResponse(content={"message": "Image already exists"}, status_code=200)
    except docker.errors.ImageNotFound:
        try:
            client.images.pull(request.image)
            return JSONResponse(content={"message": "Image pulled"}, status_code=200)
        except docker.errors.APIError as e:
            return JSONResponse(content={"message": str(e)}, status_code=500)


# 更新鏡像
class UpdataImage(BaseModel):
    image: str
@router.post("/update_image")
async def update_image(request: UpdataImage):
    try:
        client.images.get(request.image)
        try:
            client.images.pull(request.image)
            return JSONResponse(content={"message": "Image updated"}, status_code=200)
        except docker.errors.APIError as e:
            return JSONResponse(content={"message": str(e)}, status_code=500)
    except docker.errors.APIError as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)


# 移除鏡像
class RemoveImage(BaseModel):
    image: str
@router.post("/remove_image")
async def remove_image(request: RemoveImage):
    try:
        client.images.remove(request.image)
        return JSONResponse(content={"message": "Image removed"}, status_code=200)
    except docker.errors.APIError as e:
        return JSONResponse(content={"message": str(e)}, status_code=500)