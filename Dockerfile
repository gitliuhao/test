FROM centos:7
#
RUN yum -y  update
RUN yum -y  install gcc automake autoconf libtool make java-1.8.0-openjdk wget gcc-c++ zlib* netstat \
    openssh-server openssh-clients passwd chkconfig lsof
# Install any needed packages specified in requirements.txt
RUN echo "root:root"|chpasswd \
    && sed -i "s/#PubkeyAuthentication yes/PubkeyAuthentication yes/g"  /etc/ssh/sshd_config \
    && sed -i "s/#PermitRootLogin yes/PermitRootLogin yes/g"  /etc/ssh/sshd_config



RUN wget https://www.python.org/ftp/python/3.6.8/Python-3.6.8.tar.xz \
    && mkdir -p /usr/local/python3 \
    && tar xJf Python-3.6.8.tar.xz \
    && Python-3.6.8/configure --with-ssl \
    && make && make install \
    && ln -s /usr/local/python3/bin/python3 /usr/bin/python3 && ln -s /usr/local/python3/bin/pip3 /usr/bin/pip3


#
CMD ["/usr/sbin/init"]
#CMD ["mkdir", "aabb"]
