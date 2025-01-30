#!/bin/bash

## Remove VPN Container
cd ./rds-vpn
docker-compose -f docker-compose-tailscale.yml down
docker-compose -f docker-compose-docker-compose-wireguard.yml down
cd ..

docker network remove rds-vpn