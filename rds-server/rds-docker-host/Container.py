# Container.py
import asyncio
import json
from fastapi import APIRouter, Depends, HTTPException, status, Request
from pydantic import BaseModel
from fastapi.responses import JSONResponse
import docker
import os
router = APIRouter()
client = docker.from_env()


# 運行容器
class RunContainer(BaseModel):
    image: str
    command: str = None
@router.post("/run_container")
async def new_container(request: RunContainer):
    container = client.containers.run(
        request.image,
        command=request.command,
        tty=True,
        detach=True,
        stdout=True,
        stderr=True
    )
    return JSONResponse(content={"container_id": container.id}, status_code=200)


# 停止容器
class StopContainer(BaseModel):
    container_id: str
@router.post("/stop_container")
async def stop_container(request: StopContainer):
    container = client.containers.get(request.container_id)
    container.stop()
    return JSONResponse(content={"message": "Container stopped"}, status_code=200)


# 移除容器
class RemoveContainer(BaseModel):
    container_id: str
@router.post("/remove_container")
async def remove_container(request: RemoveContainer):
    container = client.containers.get(request.container_id)
    container.remove(force=True)
    return JSONResponse(content={"message": "Container removed"}, status_code=200)

