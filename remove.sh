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

docker network remove rds-vpn