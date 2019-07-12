#!/usr/bin/env bash
docker-machine ssh default "sudo mkdir /sys/fs/cgroup/systemd"
docker-machine ssh default "sudo mount -t cgroup -o none,name=systemd cgroup /sys/fs/cgroup/systemd"
docker-machine ssh default "docker network create --driver bridge --subnet=10.10.10.0/24 --gateway=10.10.10.1 mynet"

workpace=/d/HashiCorp

docker run --privileged --name=test1 --restart=always -d \
    --network=mynet --ip 10.10.10.10 \
    -v $workpace:$workpace \
    -v $workpace/root/.jenkins/:/root/.jenkins/ \
    -p 2000:22 \
    -p 8000:8000 \
    -p 80:80 \
    -p 8001:8001 \
    -p 8080:8080 \
    registry.cn-hangzhou.aliyuncs.com/lch_docker_k/test:latest

#docker run --name=jenkins --restart=always -d \
#  -u root \
#  -p 9090:8080 \
#  -v $workpace/var/jenkins_home:/var/jenkins_home \
#  jenkins/jenkins

docker run --privileged --name=jenkins_1 --restart=always -d \
    --network=mynet --ip 10.10.10.1 \
    -u root \
    -p 2001:22 \
    -p 8081:8080 \
    -v $workpace/root/.jenkins_1/:/root/.jenkins/ \
    registry.cn-hangzhou.aliyuncs.com/lch_docker_k/test:latest


docker run --privileged --name=jenkins_2 --restart=always -d \
    --network=mynet --ip 10.10.10.2 \
    -u root \
    -p 2002:22 \
    -p 8082:8080 \
    -v $workpace/root/.jenkins_2/:/root/.jenkins/ \
    registry.cn-hangzhou.aliyuncs.com/lch_docker_k/test:latest

docker run --privileged --name=jenkins_3 --restart=always -d \
    --network=mynet --ip 10.10.10.3 \
    -u root \
    -p 2003:22 \
    -p 8083:8080 \
    -v $workpace/root/.jenkins_3/:/root/.jenkins/ \
    registry.cn-hangzhou.aliyuncs.com/lch_docker_k/test:latest

docker-machine ssh default "docker exec -d jenkins_1 java -jar /root/jenkins.war"
docker-machine ssh default "docker exec -d jenkins_2 java -jar /root/jenkins.war"
docker-machine ssh default "docker exec -d jenkins_3 java -jar /root/jenkins.war"
