#!/usr/bin/env bash
docker-machine ssh default "sudo mkdir /sys/fs/cgroup/systemd"
docker-machine ssh default "sudo mount -t cgroup -o none,name=systemd cgroup /sys/fs/cgroup/systemd"
workpace=/d/HashiCorp

docker run --privileged --name=test1 --restart=always -d \
    -v $workpace:$workpace \
    -v $workpace/root/.jenkins/:/root/.jenkins/ \
    -p 2000:22 \
    -p 8000:8000 \
    -p 80:80 \
    -p 8001:8001 \
    -p 8080:8080 \
    registry.cn-hangzhou.aliyuncs.com/lch_docker_k/test:latest

docker run --name=jenkins --restart=always -d \
  -u root \
  -p 9090:8080 \
  -v $workpace/var/jenkins_home:/var/jenkins_home \
  jenkins/jenkins

docker run --privileged --name=bluepaas --restart=always -d \
  -u root \
  -p 2001:22 \
  -v $workpace:$workpace \
  registry.cn-hangzhou.aliyuncs.com/lch_docker_k/test:latest