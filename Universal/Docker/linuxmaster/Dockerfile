FROM rockylinux:8

WORKDIR /root

RUN yum update -y && \
    yum install -y --allowerasing \
        man-db man-pages logrotate rsyslog httpd sendmail procps-ng zip \
        net-tools rsync kmod lvm2 openssl-devel bind dhcp-server dhcp-client \
        vim git wget curl sudo make gcc gcc-c++ autoconf automake \
        e2fsprogs util-linux coreutils cronie crontabs squid \
        nfs-utils samba samba-client network-scripts \
        iproute iputils tar gzip bzip2 xz dump cpio file \
        vsftpd pciutils quota sed iptables firewalld && \
    yum upgrade -y yum autoremove -y && yum clean all && mandb

RUN wget https://downloads.apache.org//httpd/httpd-2.4.62.tar.gz && \
    tar -xf httpd-2.4.62.tar.gz && \
    wget https://dlcdn.apache.org//apr/apr-1.7.5.tar.gz && \
    tar -xf apr-1.7.5.tar.gz && \
    wget https://dlcdn.apache.org//apr/apr-util-1.6.3.tar.gz && \
    tar -xf apr-util-1.6.3.tar.gz && \
    wget https://sourceforge.net/projects/pcre/files/pcre/8.36/pcre-8.36.tar.gz && \
    tar -xf pcre-8.36.tar.gz && \
    wget https://cdn.kernel.org/pub/linux/kernel/v6.x/linux-6.13.tar.xz && \
    tar -Jxf linux-6.13.tar.xz && \
    mv apr-1.7.5 httpd-2.4.62/srclib/apr && mv apr-util-1.6.3 httpd-2.4.62/srclib/apr-util

WORKDIR /root/pcre-8.36
RUN ./configure --prefix=/usr/local/apache && \
    make && make install

WORKDIR /root
RUN rm -rf *.tar.* httpd-2.4.62 pcre-8.36

