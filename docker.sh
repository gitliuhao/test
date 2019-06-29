 docker run --privileged --name=test1 --restart=always -dv \
    /d:/d \
    -p 2000:22 -p 8000:8000 -p 80:80 -p 8001:8001 \
    registry.cn-hangzhou.aliyuncs.com/lch_docker_k/aaaaaaaa:1111