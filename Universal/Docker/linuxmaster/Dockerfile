FROM rockylinux:8

RUN yum update -y && \
    yum install -y --allowerasing \
        man-db man-pages logrotate rsyslog httpd sendmail procps-ng zip \
        net-tools rsync kmod \
        vim git wget curl sudo make gcc autoconf automake \
        e2fsprogs util-linux coreutils cronie crontabs squid \
        nfs-utils samba samba-client network-scripts \
        iproute iputils tar gzip bzip2 xz dump cpio \
        vsftpd pciutils quota sed iptables && \
    yum upgrade -y yum autoremove -y && yum clean all && \
    mandb

