# API List


## Infomation 
### 主機系統資訊，取得 CPU/RAM/GPU/DISK 資訊
```bash
curl -X GET http://127.0.0.1:52375/info/system
```
### Docker 容器池網路資訊，取得 rds-container-pool Subnet
```bash
curl -X GET http://127.0.0.1:52375/info/network
```
### Docker 容器池資訊，取得容器 運行和停止 數量
```bash
curl -X GET http://127.0.0.1:52375/info/container
```
### Docker 容器池資訊，取得容器 id 和 運行狀態
```bash
curl -X GET http://127.0.0.1:52375/info/check_container
```


## Image
### 拉取鏡像，鏡像已存在不會執行
```bash
curl -X 'POST' \
  'http://localhost:52375/image/pull_image' \
  -H 'Content-Type: application/json' \
  -d '{"image": "alpine:latest"}'
```
### 更新鏡像，鏡像不存在不會執行
```bash
curl -X 'POST' \
  'http://localhost:52375/image/update_image' \
  -H 'Content-Type: application/json' \
  -d '{"image": "alpine:latest"}'
```
### 移除鏡像
```bash
curl -X 'POST' \
  'http://localhost:52375/image/remove_image' \
  -H 'Content-Type: application/json' \
  -d '{"image": "alpine:latest"}'
```


## Container
### 運行容器
```bash
curl -X 'POST' \
  'http://localhost:52375/container/run_container' \
  -H 'Content-Type: application/json' \
  -d '{"image": "busybox:latest", "command": "", "cpus": 20, "mem_limit": "800m", "privileged": true}'
```
### 停止容器
```bash
curl -X 'POST' \
  'http://localhost:52375/container/stop_container' \
  -H 'Content-Type: application/json' \
  -d '{"container_id": "4d965d7527d4cacd8f1ba934aeddad894a9ca269c8edbdc09c4ac31766f85699"}'
```
### 移除容器，強行移除
```bash
curl -X 'POST' \
  'http://localhost:52375/container/remove_container' \
  -H 'Content-Type: application/json' \
  -d '{"container_id": "4d965d7527d4cacd8f1ba934aeddad894a9ca269c8edbdc09c4ac31766f85699"}'
```