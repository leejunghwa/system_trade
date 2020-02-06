#!/usr/bin/env bash

# for ssh login
/usr/sbin/sshd

# for telnet login
service xinetd restart

# for crawler execute
python /root/crawler_main.py -t xoxb-240213934096-877230619267-RhhlfWgo0n0aGohid9OK8UY6 -c \#play_and_study >> crawler.log

# for bash execute
/bin/bash