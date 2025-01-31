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
    command: str
    cpus: int = 50
    mem_limit: str = "512m"
    privileged: bool = False
@router.post("/run_container")
async def new_container(request: RunContainer):
    if request.cpus <= 0 or request.cpus > 100:
        return JSONResponse(content={"message": "CPU 計算資源必須大於0且小於等於100"}, status_code=400)
    container = client.containers.run(
        request.image,
        command=request.command,
        cpu_quota=int(100000*(request.cpus / 100)),
        cpu_period=100000,
        mem_limit=request.mem_limit,
        privileged=request.privileged,
        network="rds-vpn",
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
