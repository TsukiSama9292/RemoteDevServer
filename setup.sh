#!/bin/bash

# 執行初始化腳本
cd ./script
chmod +x ./*
./ubuntu.sh
./docker-pull.sh
cd ..

# 建立 Docker 網路
docker network create rds-vpn
gateway=$(docker network inspect -f '{{range .IPAM.Config}}{{.Subnet}}{{end}}' rds-vpn)
echo "gateway=$gateway" > ./rds-server/docker-host/rds-vpn.env

# 預設值
Tailscale="false"
Wireguard="true"
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
docker-compose build --no-cache
docker-compose up -d
cd ..