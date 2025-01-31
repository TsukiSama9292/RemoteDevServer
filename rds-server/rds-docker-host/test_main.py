from fastapi.testclient import TestClient
from main import app
import os
import subprocess
import docker
import re

client = TestClient(app)

def test_system_info():
    print("\n\nTesting /system-info")
    response = client.get("/info/system-info")
    # 取得 RAM 大小
    with open("/proc/meminfo") as f:
        mem_info = f.readlines()
    mem_total = int([line for line in mem_info if line.startswith("MemTotal")][0].split(":")[1].strip().split()[0]) // 1024  # 轉換為 MB
    # 取得 GPU 數量(NVIDIA)
    try:
        gpu_count = int(subprocess.check_output("nvidia-smi -L | wc -l", shell=True).strip())
    except subprocess.CalledProcessError:
        gpu_count = 0
    # 解析回應狀態
    assert response.status_code == 200, f"Status Code: {response.status_code}"
    # 解析內容
    response_json = response.json()
    if response_json["DISK_SIZE"] == "Error" or response_json["DISK_USED"] == "Error" or response_json["DISK_USAGE_PERCENT"] == "Error":
        print(f"JSON Content: {response.json()}")
        assert False
    if response_json["CPU_COUNT"] != os.cpu_count() or response_json["RAM_SIZE(MB)"] != mem_total or response_json["GPU_COUNT"] != gpu_count:
        print(f"JSON Content: {response.json()}")
        assert False
    
    

def test_network_info():
    print("\n\nTesting /network-info")
    response = client.get("/info/network-info")
    # 解析回應狀態
    assert response.status_code == 200, f"Status Code: {response.status_code}"
    # 解析內容
    assert response.json() == {'GATEWAY': '10.100.0.0/16'}, f"JSON Content: {response.json()}"