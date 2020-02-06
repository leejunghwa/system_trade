############################################################
# LeeJungHwa's Crawler Ubuntu 19.04 base image
############################################################

FROM ubuntu:19.04

MAINTAINER Lee JungHwa <junghwa.lee@piolink.com>

ENV DEBIAN_FRONTEND noninteractive
RUN cd /etc/apt && \
    sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' sources.list
    # sed -i 's/archive.ubuntu.com/mirror.kakao.com/g' sources.list.d/proposed.list

RUN apt-get update

# Install Linux command line tools
############################################################
RUN apt-get update && apt-get -y dist-upgrade && \
    apt-get install -y sudo openssh-server dnsutils \
    net-tools nmap ack-grep telnet traceroute iputils-ping
RUN apt-get install -y netstat-nat vim bash-completion \
    apt-utils wget curl git-core locate man rsync make \
    gcc keychain dialog locales iproute2
RUN apt-get install -y tcpdump tzdata vsftpd
RUN apt-get install -y bsdtar
RUN apt-get install -y ftp netcat iptables xinetd telnetd git tree \
    dosfstools
RUN apt-get install -y python
RUN apt-get install -y python-pip  python-matplotlib
RUN python -m pip install schedule requests bs4 feedparser slacker
############################################################

# for Time zone
RUN ln -sf /usr/share/zoneinfo/Asia/Seoul /etc/localtime

# tcpdump binary move for https://github.com/dotcloud/docker/issues/5490
RUN mv /usr/sbin/tcpdump /usr/bin/tcpdump

# for docker container ssh login
RUN mkdir -p -m 0755 /var/run/sshd
RUN sed -i 's/#PermitRootLogin prohibit-password/PermitRootLogin yes/' /etc/ssh/sshd_config
RUN echo 'root:admin' | chpasswd

# for docker container ftp service
COPY env_conf/vsftpd.conf /etc/vsftpd.conf

# for docker container telnet service
COPY env_conf/telnet /etc/xinetd.d/telnet
COPY env_conf/securetty /etc/securetty

# for entry point
COPY script/* /root/
RUN chmod +x /root/entrypoint.sh

# for docker container crawler
COPY code/Crawler /root/Crawler
COPY code/trader_main.py /root/crawler_main.py

EXPOSE 20 21 22 23

ENTRYPOINT ["/root/entrypoint.sh"]