#!/bin/bash

docker network create rds-vpn
gateway=$(docker network inspect -f '{{range .IPAM.Config}}{{.Subnet}}{{end}}' rds-vpn)

# 預設值
Tailscale="false"
Wireguard="true"

# 解析長選項
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

# 顯示變數值
echo "Tailscale: $Tailscale"
echo "Wireguard: $Wireguard"

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
