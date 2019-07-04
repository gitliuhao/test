FROM centos:7
RUN yum -y  update
RUN yum -y  install gcc automake autoconf libtool make java-1.8.0-openjdk wget gcc-c++ zlib* \
    openssh-server openssh-clients passwd chkconfig lsof vim
# Install any needed packages specified in requirements.txt
RUN echo "root:root"|chpasswd \
    && sed -i "s/#PubkeyAuthentication yes/PubkeyAuthentication yes/g"  /etc/ssh/sshd_config \
    && sed -i "s/#PermitRootLogin yes/PermitRootLogin yes/g"  /etc/ssh/sshd_config

# python环境依赖包
RUN yum -y install openssl-devel bzip2-devel expat-devel gdbm-devel readline-devel sqlite-devel

# 安装python
RUN wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tar.xz \
    && tar xJf Python-3.6.8.tar.xz \
    && /Python-3.6.8/configure --prefix=/usr/local/python3 \
    && make && make install \
    && ln -s /usr/local/python3/bin/python3 /usr/bin/python3 && ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3

# pip换源
RUN mkdir ~/.pip && \
    echo -e "[global]" \
            "\ntimeout = 6000" \
            "\nindex-url = https://mirrors.aliyun.com/pypi/simple/" \
            "\ntrusted-host = pypi.tuna.tsinghua.edu.cn" >  ~/.pip/pip.conf

# yum 换源
RUN yum -y install epel-release && yum clean all && yum makecache


# 系统编码设置utf8

#RUN export LC_ALL=en_US.utf8 && export LANG=en_US.utf8
RUN sed -i '$a export LANG=en_US.utf8' /etc/profile
ENV LANG en_US.utf8


# 安装python环境
COPY requirements.txt /root/requirements.txt
RUN pip3 install -r /root/requirements.txt

#下载Jenkins
RUN wget http://mirrors.jenkins.io/war-stable/latest/jenkins.war -P ~

#
CMD ["/usr/sbin/init"]
#CMD ["mkdir", "aabb"]
