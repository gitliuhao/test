#!/usr/bin/env bash
docker-machine ssh default "sudo mkdir /sys/fs/cgroup/systemd"
docker-machine ssh default "sudo mount -t cgroup -o none,name=systemd cgroup /sys/fs/cgroup/systemd"

docker run --privileged --name=test1 --restart=always -d \
    -v /d/HashiCorp:/d/HashiCorp \
    -v /d/HashiCorp/root/.jenkins/:/root/.jenkins/ \
    -p 2000:22 \
    -p 8000:8000 \
    -p 80:80 \
    -p 8001:8001 \
    -p 8080:8080 \
    registry.cn-hangzhou.aliyuncs.com/lch_docker_k/aaaaaaaa:1111
