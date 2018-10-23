#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
import requests



g_adsl_account = {"name": "�������",
                "username": "test9421",
                "password": "1578"}

class Adsl(object):
    #==============================================================================
    # __init__ : name: adsl����
    #==============================================================================
    def __init__(self):
        self.name = g_adsl_account["name"]
        self.username = g_adsl_account["username"]
        self.password = g_adsl_account["password"]

    #==============================================================================
    # set_adsl : �޸�adsl����
    #==============================================================================
    def set_adsl(self, account):
        self.name = account["name"]
        self.username = account["username"]
        self.password = account["password"]

    #==============================================================================
    # connect : �������
    #==============================================================================
    def connect(self):
        cmd_str = "rasdial %s %s %s" % (self.name, self.username, self.password)
        os.system(cmd_str)
        time.sleep(5)

    #==============================================================================
    # disconnect : �Ͽ��������
    #==============================================================================
    def disconnect(self):
        cmd_str = "rasdial %s /disconnect" % self.name
        os.system(cmd_str)
        time.sleep(5)

    #==============================================================================
    # reconnect : ���½��в���
    #==============================================================================
    def reconnect(self):
        self.disconnect()
        self.connect()





url = 'https://api.ipify.org?format=json'


def getip_requests(url):
    print "(+) Sending request with plain requests..."
    r = requests.get(url)
    ip=r.text.replace("\n", "")
    print "(+) IP is: " + ip
    return ip



def main():
    print "Running tests..."
    ip = getip_requests(url)
    saveip(ip)
    print "save successful..."

#����ip
def saveip(ip):
    f = open('ips.txt','a+')
    f.write(ip+'\n')
    f.close()

if __name__ == "__main__":
    while True:
        aa=Adsl()
        aa.reconnect()
        main()
