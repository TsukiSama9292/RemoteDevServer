# 筆記區
## Docker 獲取容器 IP CLI
```bash
docker inspect -f '{{range.NetworkSettings.Networks}}{{.IPAddress}}{{end}}' ssh-tailscale
```