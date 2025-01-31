# SystemInfo.py
import asyncio
import json
from fastapi import APIRouter, Depends, HTTPException, status, Request
from fastapi.responses import JSONResponse
import os
import subprocess
import docker
import re
from dotenv import load_dotenv
import psutil
import pyopencl as cl

router = APIRouter()
client = docker.from_env()
# 主機系統資訊，取得 CPU/RAM/GPU/DISK 資訊
@router.get("/system")
async def get_system_info():
    # 取得 CPU 資訊
    cpu_count = psutil.cpu_count()
    cpu_percent = psutil.cpu_percent(interval=1)

    # 取得 RAM 資訊
    mem_info = psutil.virtual_memory()
    mem_total = mem_info.total // (1024 ** 2)  # 轉換為 MB
    mem_used = mem_info.used // (1024 ** 2)    # 轉換為 MB
    mem_percent = mem_info.percent

    # 取得 GPU 數量
    gpu_count = 0
    try:
        platforms = cl.get_platforms()
        for platform in platforms:
            devices = platform.get_devices(device_type=cl.device_type.GPU)
            gpu_count += len(devices)
    except cl.Error as e:
        # 如果無法獲取 GPU 資訊，則視為無 GPU
        gpu_count = 0

    # 取得硬碟資訊
    disk_info = psutil.disk_usage('/')
    disk_total = disk_info.total // (1024 ** 3)  # 轉換為 GB
    disk_used = disk_info.used // (1024 ** 3)    # 轉換為 GB
    disk_percent = disk_info.percent

    return {
        "CPU_COUNT": cpu_count,
        "CPU_USAGE_PERCENT": cpu_percent,
        "RAM_TOTAL_MB": mem_total,
        "RAM_USED_MB": mem_used,
        "RAM_USAGE_PERCENT": mem_percent,
        "GPU_COUNT": gpu_count,
        "DISK_TOTAL_GB": disk_total,
        "DISK_USED_GB": disk_used,
        "DISK_USAGE_PERCENT": disk_percent,
    }
# Docker 容器池網路資訊，取得 rds-container-pool Subnet
@router.get("/network")
async def get_network_info():
    network_name = 'rds-container-pool'
    try:
        # 獲取名為 'rds-container-pool' 的網路
        network = client.networks.get(network_name)
        # 取得子網路資訊
        subnet = network.attrs['IPAM']['Config'][0]['Subnet']
        return {"GATEWAY": subnet}
    except docker.errors.NotFound:
        return {"error": f"Network '{network_name}' not found"}
    except KeyError:
        return {"error": "Subnet information not available"}
# Docker 容器池資訊，取得容器 運行和停止 數量
@router.get("/container")
async def get_container_info():
    # containers = client.containers.list(all=True)
    network = client.networks.get('rds-container-pool')
    containers = network.containers
    running_count = 0
    paused_count = 0
    for container in containers:
        if container.name == 'rds-proxy' or container.name == 'rds-tailscale' or container.name == 'rds-wireguard':
            continue
        if container.status == 'running':
            running_count += 1
        elif container.status == 'paused':
            paused_count += 1
    return {"RUNNING_COUNT": running_count, "PAUSED_COUNT": paused_count}
# Docker 容器池資訊，取得容器 id 和 運行狀態
@router.get("/check_container")
async def check_container():
    network = client.networks.get('rds-container-pool')
    containers = network.containers
    container_list = []
    for container in containers:
        if container.name == 'rds-proxy' or container.name == 'rds-tailscale' or container.name == 'rds-wireguard':
            continue
        container_list.append({"id": container.id, "status": container.status})
    return JSONResponse(content=container_list, status_code=200)
