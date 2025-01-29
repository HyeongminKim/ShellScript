FROM rockylinux:8

# 패키지 버전 설정
# https://dlcdn.apache.org//httpd
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
        man-db man-pages logrotate rsyslog sendmail procps-ng zip \
        net-tools rsync kmod lvm2 openssl-devel bind dhcp-server dhcp-client \
        vim git wget curl sudo make gcc gcc-c++ autoconf automake flex \
        e2fsprogs util-linux coreutils cronie crontabs squid mdadm telnet \
        nfs-utils samba samba-client network-scripts bison nmap traceroute \
        iproute iputils tar gzip bzip2 xz dump cpio file passwd ncurses ncurses-devel \
        vsftpd pciutils quota sed iptables firewalld bind-utils expat expat-devel \
        ypbind ypserv yp-tools rpcbind xinetd

RUN curl -fSL https://dlcdn.apache.org//httpd/httpd-$httpd_version.tar.gz > httpd-$httpd_version.tar.gz && \
    tar -xf httpd-$httpd_version.tar.gz && \
    curl -fSL https://dlcdn.apache.org//apr/apr-$apr_version.tar.gz > apr-$apr_version.tar.gz && \
    tar -xf apr-$apr_version.tar.gz && \
    curl -fSL https://dlcdn.apache.org//apr/apr-util-$apr_util_version.tar.gz > apr-util-$apr_util_version.tar.gz && \
    tar -xf apr-util-$apr_util_version.tar.gz && \
    curl -fSL https://sourceforge.net/projects/pcre/files/pcre/$pcre_version/pcre-$pcre_version.tar.gz > pcre-$pcre_version.tar.gz && \
    tar -xf pcre-$pcre_version.tar.gz && \
    curl -fSL https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-$kernel_version.tar.xz > linux-$kernel_version.tar.xz && \
    tar -Jxf linux-$kernel_version.tar.xz && \
    mv apr-$apr_version apr-util-$apr_util_version httpd-$httpd_version pcre-$pcre_version /usr/local/src && \
    rm -rf *.tar.*

WORKDIR /usr/local/src
RUN apr-$apr_version/configure \
        --prefix=/usr/local/src/apr-$apr_version && \
        make && make install && \
    apr-util-$apr_util_version/configure \
        --prefix=/usr/local/src/apr-util-$apr_util_version \
        --with-apr=/usr/local/src/apr-$apr_version && \
        make && make install && \
    pcre-$pcre_version/configure \
        --prefix=/usr/local/src/pcre-$pcre_version \
        --with-apr=/usr/local/src/apr-$apr_version \
        --with-apr-util=/usr/local/src/apr-util-$apr_util_version && \
        make && make install

WORKDIR /usr/local/src/httpd-$httpd_version
RUN ./configure \
    --prefix=/usr/local/apache \
    --enable-modules=most \
    --enable-mods-shared=all \
    --enable-so \
    --with-apr=/usr/local/src/apr-$apr_version \
    --with-apr-util=/usr/local/src/apr-util-$apr_util_version \
    --with-pcre=/usr/local/src/pcre-$pcre_version/bin/pcre-config && \
    make && make install && \
    /usr/local/apache/bin/httpd -V

# RUN ln -s /etc/httpd/conf /usr/local/apache && \
#     ln -s /etc/httpd/conf.d /usr/local/apache && \
#     ln -s /etc/httpd/conf.modules.d /usr/local/apache && \
#     ln -s /etc/httpd/modules /usr/local/apache && \
#     ln -s /usr/sbin/apachectl /usr/local/apache/bin && \

WORKDIR /root
RUN yum upgrade -y yum autoremove -y && yum clean all && \
    mandb

