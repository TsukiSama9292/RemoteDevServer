#!/bin/bash

## Remove VPN Container
cd ./rds-vpn
docker-compose -f docker-compose-tailscale.yml down
docker-compose -f docker-compose-wireguard.yml down
cd ..

## Remove Server Container
cd ./rds-server
docker-compose down

## Remove Docker Host Container
cd ./rds-docker-host
docker-compose down
cd ../..

docker network remove rds-container-pool
docker network remove rds-server
docker network remove rds-docker-host

docker volume remove rds-vpn_tailscale
docker volume remove rds-vpn_wireguard-config
docker volume remove rds-vpn_wireguard-modules
docker volume remove rds-server_db
docker volume remove rds-server_static
docker volume remove rds-server_redis