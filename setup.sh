#!/bin/bash

# 錯誤檢查
set -e

error_handler() {
    echo "發生錯誤，請根據錯誤修正..."
    exit 1
    ./remove.sh
}

trap error_handler ERR

# 執行初始化腳本
cd ./script
chmod +x ./*
./ubuntu.sh
./docker-pull.sh
cd ..

# 建立 Docker 網路
source .env
SUBNET="10.$((HOST_COUNT + 100)).0.0/16"
docker network create --driver bridge --subnet=$SUBNET rds-vpn
GATEWAY=$(docker network inspect -f '{{range .IPAM.Config}}{{.Subnet}}{{end}}' rds-vpn)
echo "SERVER_IP=$SERVER_IP" > ./rds-vpn/.env
echo "GATEWAY=$GATEWAY" >> ./rds-vpn/.env

# 預設值
Tailscale="false"
Wireguard="false"
# 解析命令列參數
PARSED_OPTS=$(getopt -o "" --long Tailscale:,Wireguard: -- "$@")
eval set -- "$PARSED_OPTS"
while true; do
  case "$1" in
    --Tailscale) Tailscale="$2"; shift 2 ;;
    --Wireguard) Wireguard="$2"; shift 2 ;;
    --) shift; break ;;
    *) break ;;
  esac
done

# 啟動 VPN 容器
if [ "$Tailscale" = "true" ]; then
  echo "Setup Tailscale Container..."
  cd ./rds-vpn
  docker-compose -f docker-compose-tailscale.yml up -d
  cd ..
fi
if [ "$Wireguard" = "true" ]; then
  echo "Setup Wireguard Container..."
  cd ./rds-vpn
  docker-compose -f docker-compose-wireguard.yml up -d
  cd ..
fi
# 啟動 Docker Host 容器
echo "Setup Docker Host Container..."
cd ./rds-server/rds-docker-host
docker-compose build --no-cache
docker-compose up -d
cd ../..

# 啟動 Server 容器
cd ./rds-server
# docker-compose build --no-cache
docker-compose up -d
cd ..