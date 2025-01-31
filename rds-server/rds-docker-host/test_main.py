from fastapi.testclient import TestClient
from main import app
import os
import subprocess
import docker
import re
import psutil
import pyopencl as cl

client = TestClient(app)
docker_client = docker.from_env()
container_id = None


# 測試資訊路由
## 測試主機系統資訊，取得 CPU/RAM/GPU/DISK 資訊
def test_system_info():
    print("\n\nTesting /info/system")
    response = client.get("/info/system")
    # 解析回應狀態
    assert response.status_code == 200, f"Status Code: {response.status_code}"
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

    rj = response.json()
    if rj["CPU_COUNT"] != cpu_count or rj["RAM_TOTAL_MB"] != mem_total or rj["GPU_COUNT"] != gpu_count or rj["DISK_TOTAL_GB"] != disk_total :
        assert False, f"JSON Content: {rj}"
## 測試 Docker 容器池網路資訊，取得 rds-container-pool Subnet
def test_network_info():
    print("\n\nTesting /info/network")
    response = client.get("/info/network")
    # 解析回應狀態
    assert response.status_code == 200, f"Status Code: {response.status_code}"
    # 解析內容
    assert response.json() == {'GATEWAY': '10.100.0.0/16'}, f"JSON Content: {response.json()}"
## 測試 Docker 容器池資訊，取得容器 運行和停止 數量
def test_container_info():
    global docker_client
    container = docker_client.containers.run(
        image="busybox:latest",
        tty=True,
        detach=True,
        stdout=True,
        stderr=True,
        network="rds-container-pool"
    )
    print("\n\nTesting /info/container")
    response = client.get("/info/container")
    # 解析回應狀態
    assert response.status_code == 200, f"Status Code: {response.status_code}"
    container.remove(force=True)
    # 解析內容
    assert response.json() == {"RUNNING_COUNT": 1, "PAUSED_COUNT": 0}
## 測試 Docker 容器池資訊，取得容器 id 和 運行狀態
def test_check_container():
    global docker_client
    container = docker_client.containers.run(
        image="busybox:latest",
        tty=True,
        detach=True,
        stdout=True,
        stderr=True,
        network="rds-container-pool"
    )
    print("\n\nTesting /info/check_container")
    response = client.get("/info/check_container")
    # 解析回應狀態
    assert response.status_code == 200, f"Status Code: {response.status_code}"
    container.remove(force=True)
    # 解析內容
    assert response.json() == [{"id": container.id, "status": "running"}], f"JSON Content: {response.json()}"

# 測試鏡像路由
## 測試拉取鏡像
def test_pull_image():
    print("\n\nTesting /image/pull_image")
    response = client.post("/image/pull_image", json={"image": "alpine:latest"})
    # 解析回應狀態
    assert response.status_code == 200, f"Status Code: {response.status_code}"
    # 解析內容
    if response.json() != {"message": "Image already exists"} and response.json() != {"message": "Image pulled"}:
        assert False, f"JSON Content: {response.json()}"
## 測試更新鏡像
def test_update_image():
    print("\n\nTesting /image/update_image")
    response = client.post("/image/update_image", json={"image": "alpine:latest"})
    # 解析回應狀態
    assert response.status_code == 200, f"Status Code: {response.status_code}"
    # 解析內容
    assert response.json() == {"message": "Image updated"}, f"JSON Content: {response.json()}"
## 測試移除鏡像
def test_remove_image():
    print("\n\nTesting /image/remove_image")
    response = client.post("/image/remove_image", json={"image": "alpine:latest"})
    # 解析回應狀態
    assert response.status_code == 200, f"Status Code: {response.status_code}"
    # 解析內容
    assert response.json() == {"message": "Image removed"}, f"JSON Content: {response.json()}"


# 測試容器路由
## 測試運行容器
def test_run_container():
    global container_id
    print("\n\nTesting /container/run_container")
    response = client.post("/container/run_container", json={"image": "busybox:latest", "command": "", "cpus": 20, "mem_limit": "800m", "privileged": True})
    # 解析回應狀態
    assert response.status_code == 200, f"Status Code: {response.status_code}"
    container_id = response.json()["container_id"]
    # 解析內容
    assert re.match(r'^[0-9a-f]{64}$', container_id), f"JSON Content: {response.json()}"
## 測試停止容器
def test_stop_container():
    global container_id
    print("\n\nTesting /container/stop_container")
    response = client.post("/container/stop_container", json={"container_id": container_id})
    # 解析回應狀態
    assert response.status_code == 200, f"Status Code: {response.status_code}"
    # 解析內容
    assert response.json() == {"message": "Container stopped"}, f"JSON Content: {response.json()}"
## 測試移除容器
def test_remove_container():
    global container_id
    print("\n\nTesting /container/remove_container")
    response = client.post("/container/remove_container", json={"container_id": container_id})
    # 解析回應狀態
    assert response.status_code == 200, f"Status Code: {response.status_code}"
    # 解析內容
    assert response.json() == {"message": "Container removed"}, f"JSON Content: {response.json()}"
