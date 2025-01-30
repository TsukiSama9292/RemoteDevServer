#!/bin/bash

# 讀取 JSON 文件並拉取 Docker 映像
jq -c '.images[]' docker-images.json | while read -r image; do
    name=$(echo "$image" | jq -r '.name')
    tag=$(echo "$image" | jq -r '.tag')
    docker pull "$name:$tag"
done
