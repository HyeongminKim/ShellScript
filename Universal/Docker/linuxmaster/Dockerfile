FROM rockylinux:8

# 패키지 버전 설정
# https://downloads.apache.org//httpd
# https://dlcdn.apache.org//apr
# https://sourceforge.net/projects/pcre/files/pcre
# https://cdn.kernel.org/pub/linux/kernel
# 404 Not Found 오류시 위 링크를 참조하여 버전 수정 후 재시도

ARG httpd_version=2.4.63
ARG apr_version=1.7.5
ARG apr_util_version=1.6.3
ARG pcre_version=8.45
ARG kernel_version=6.13

WORKDIR /root

RUN yum update -y && \
    yum install -y --allowerasing \
        man-db man-pages logrotate rsyslog httpd httpd-* sendmail procps-ng zip \
        net-tools rsync kmod lvm2 openssl-devel bind dhcp-server dhcp-client \
        vim git wget curl sudo make gcc gcc-c++ autoconf automake \
        e2fsprogs util-linux coreutils cronie crontabs squid \
        nfs-utils samba samba-client network-scripts tomcat log4j \
        iproute iputils tar gzip bzip2 xz dump cpio file \
        vsftpd pciutils quota sed iptables firewalld && \
    yum upgrade -y yum autoremove -y && yum clean all && mandb

RUN wget https://downloads.apache.org//httpd/httpd-$httpd_version.tar.gz && \
    tar -xf httpd-$httpd_version.tar.gz && \
    wget https://dlcdn.apache.org//apr/apr-$apr_version.tar.gz && \
    tar -xf apr-$apr_version.tar.gz && \
    wget https://dlcdn.apache.org//apr/apr-util-$apr_util_version.tar.gz && \
    tar -xf apr-util-$apr_util_version.tar.gz && \
    wget https://sourceforge.net/projects/pcre/files/pcre/$pcre_version/pcre-$pcre_version.tar.gz && \
    tar -xf pcre-$pcre_version.tar.gz && \
    wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-$kernel_version.tar.xz && \
    tar -Jxf linux-$kernel_version.tar.xz && \
    mv apr-$apr_version httpd-$httpd_version/srclib/apr && mv apr-util-$apr_util_version httpd-$httpd_version/srclib/apr-util

WORKDIR /root/pcre-$pcre_version
RUN ./configure --prefix=/usr/local/apache && \
    make && make install && \
    ln -s /etc/httpd/conf /usr/local/apache && \
    ln -s /etc/httpd/conf.d /usr/local/apache && \
    ln -s /etc/httpd/conf.modules.d /usr/local/apache && \
    ln -s /etc/httpd/modules /usr/local/apache && \
    ln -s /usr/sbin/apachectl /usr/local/apache/bin

WORKDIR /root
RUN rm -rf *.tar.* httpd-$httpd_version pcre-$pcre_version

