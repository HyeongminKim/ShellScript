FROM rockylinux:8

RUN yum update -y && yum upgrade -y && yum autoremove && \
    yum install -y --allowerasing \
        man logrotate rsyslog httpd sendmail procps-ng zip \
        net-tools rsync kmod \
        vim git wget curl sudo make gcc autoconf automake \
        e2fsprogs util-linux coreutils cronie crontabs squid \
        nfs-utils samba samba-client network-scripts \
        iproute iputils tar gzip bzip2 xz dump cpio \
        vsftpd pciutils quota sed iptables && \
    yum clean all && \
    mandb

