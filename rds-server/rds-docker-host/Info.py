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
router = APIRouter()
client = docker.from_env()

@router.get("/system-info")
async def get_system_info():
    # 取得 CPU 核心數量
    cpu_count = os.cpu_count()

    # 取得 RAM 大小
    with open("/proc/meminfo") as f:
        mem_info = f.readlines()
    mem_total = int([line for line in mem_info if line.startswith("MemTotal")][0].split(":")[1].strip().split()[0]) // 1024  # 轉換為 MB

    # 取得 GPU 數量(NVIDIA)
    try:
        gpu_count = int(subprocess.check_output("nvidia-smi -L | wc -l", shell=True).strip())
    except subprocess.CalledProcessError:
        gpu_count = 0
    
    # 取得硬碟使用量
    container = client.containers.run(
        "busybox:latest",
        "df -h /",
        remove=True
    )
    pattern = r"(\d+\.\d+G)\s+(\d+\.\d+G)\s+\d+\.\d+G\s+(\d+)%"
    disk_usage = container.decode("utf-8")
    match = re.search(pattern, disk_usage)
    if match:
        total_size = match.group(1)
        used_size = match.group(2)
        usage_percent = match.group(3)
    else:
        total_size = "Error"
        used_size = "Error"
        usage_percent = "Error"
    
    return {
        "CPU_COUNT": cpu_count,
        "RAM_SIZE(MB)": mem_total,
        "GPU_COUNT": gpu_count,
        "DISK_SIZE": total_size,
        "DISK_USED": used_size,
        "DISK_USAGE_PERCENT": usage_percent,
    }

@router.get("/network-info")
async def get_network_info():
    network_name = 'rds-vpn'
    try:
        # 獲取名為 'rds-vpn' 的網路
        network = client.networks.get(network_name)
        # 取得子網路資訊
        subnet = network.attrs['IPAM']['Config'][0]['Subnet']
        return {"GATEWAY": subnet}
    except docker.errors.NotFound:
        return {"error": f"Network '{network_name}' not found"}
    except KeyError:
        return {"error": "Subnet information not available"}