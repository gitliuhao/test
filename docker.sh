#!/usr/bin/env bash
docker-machine ssh default "sudo mkdir /sys/fs/cgroup/systemd"
docker-machine ssh default "sudo mount -t cgroup -o none,name=systemd cgroup /sys/fs/cgroup/systemd"
docker-machine ssh default "docker network create --driver bridge --subnet=10.10.10.0/24 --gateway=10.10.10.1 mynet"

workpace=/d/HashiCorp
db_name=o39
# 开发环境容器启动
docker run --privileged --name=test1 --restart=always -d \
    --network=mynet --ip 10.10.10.10 \
    -v $workpace:$workpace \
    -v $workpace/root/.jenkins/:/root/.jenkins/ \
    -p 2000:22 \
    -p 8000:8000 \
    -p 80:80 \
    -p 8001:8001 \
    -p 8006:8006 \
    -p 8007:8007 \
    -p 8008:8008 \
    -p 8009:8009 \
    -p 8080:8080 \
    registry.cn-hangzhou.aliyuncs.com/lch_docker_k/test:latest

## mysql数据库容器启动
#docker run --privileged --name=mymysql --restart=always -d \
#    -p 3306:3306 \
#    --network=mynet --ip 10.10.10.24 \
#    -v $workpace/mymysql/conf:/etc/mysql/conf.d \
#    -v $workpace/mymysql/logs:/logs \
#    -e MYSQL_ROOT_PASSWORD=123456 \STATIC_ROOT
#    mysql:latest
#
##docker run --privileged --name=mymysql --restart=always -it \
##    -p 3306:3306 \
##    -u root \
##    --network=mynet --ip 10.10.10.24 \
##    -e MYSQL_ROOT_PASSWORD=123456 \
##    mysql:5.6
#
##docker run --name=jenkins --restart=always -d \
##  -u root \
##  -p 9090:8080 \
##  -v $workpace/var/jenkins_home:/var/jenkins_home \
##  jenkins/jenkins
#
## jenkins容器启动
#docker run --privileged --name=jenkins_1 --restart=always -d \
#    --network=mynet --ip 10.10.10.1 \
#    -u root \
#    -p 2001:22 \
#    -p 8081:8080 \
#    -v $workpace/root/.jenkins_1/:/root/.jenkins/ \
#    registry.cn-hangzhou.aliyuncs.com/lch_docker_k/test:latest
#
#
#docker run --privileged --name=jenkins_2 --restart=always -d \
#    --network=mynet --ip 10.10.10.2 \
#    -u root \
#    -p 2002:22 \
#    -p 8082:8080 \
#    -v $workpace/root/.jenkins_2/:/root/.jenkins/ \
#    registry.cn-hangzhou.aliyuncs.com/lch_docker_k/test:latest
#
#docker run --privileged --name=jenkins_3 --restart=always -d \
#    --network=mynet --ip 10.10.10.3 \
#    -u root \
#    -p 2003:22 \
#    -p 8083:8080 \
#    -v $workpace/root/.jenkins_3/:/root/.jenkins/ \
#    registry.cn-hangzhou.aliyuncs.com/lch_docker_k/test:latest
#
##mysql允许远程连接
#docker-machine ssh default \
#    "docker exec -d mymysql " \
#    "mysql -uroot -p123456 -e\"" \
#    "CREATE DATABASE $db_name CHARACTER SET utf8 COLLATE utf8_general_ci;" \
#    "ALTER USER 'root'@'%' IDENTIFIED WITH mysql_native_password BY '123456';" \
#    "FLUSH PRIVILEGES;\""
#
## 启动三个jenkins服务
#docker-machine ssh default "sudo rm -rf /root/.ssh/known_hosts"
#docker-machine ssh default "docker exec -d jenkins_1 java -jar /root/jenkins.war"
#docker-machine ssh default "docker exec -d jenkins_1 \cp -r  ~/.ssh/id_rsa ~/.jenkins/"
#docker-machine ssh default "docker exec -d jenkins_2 java -jar /root/jenkins.war"
#docker-machine ssh default "docker exec -d jenkins_2 \cp -r  ~/.ssh/id_rsa ~/.jenkins/"
#docker-machine ssh default "docker exec -d jenkins_3 java -jar /root/jenkins.war"
#docker-machine ssh default "docker exec -d jenkins_3 \cp -r  ~/.ssh/id_rsa ~/.jenkins/"
