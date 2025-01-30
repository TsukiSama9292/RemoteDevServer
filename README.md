```bash
docker-compose -f docker-compose-tailscale.yml down
docker-compose -f docker-compose-tailscale.yml build --no-cache
docker-compose -f docker-compose-tailscale.yml up -d
```
```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ssh-tailscale
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ssh-server-ssh-1
```

docker run -t -d --network=ssh-server alpine:latest
```
```bash
docker run -d -t --network ssh-server --name dev-ssh tsukisama9292/dev:ssh-rolling
```
```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' dev-ssh
```
```bash
for i in $(seq 1 255); do
    docker run -d -t --name "container$i" --network ssh-server alpine:latest
done
```
```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' container255
```
```bash
chmod +x setup.sh
./setup.sh --Tailscale true --Wireguard false
```
```bash
chmod +x remove.sh
./remove.sh
```
```bash
docker network inspect -f '{{range .IPAM.Config}}{{.Subnet}}{{end}}' rds-vpn
```