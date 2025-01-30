```bash
docker-compose -f docker-compose-tailscale.yml down
docker-compose -f docker-compose-tailscale.yml build --no-cache
docker-compose -f docker-compose-tailscale.yml up -d
```
```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ssh-tailscale
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ssh-server-ssh-1
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