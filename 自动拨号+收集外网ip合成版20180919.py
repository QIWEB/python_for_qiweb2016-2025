#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
import requests



g_adsl_account = {"name": "宽带连接",
                "username": "test9421",
                "password": "1578"}

class Adsl(object):
    #==============================================================================
    # __init__ : name: adsl名称
    #==============================================================================
    def __init__(self):
        self.name = g_adsl_account["name"]
        self.username = g_adsl_account["username"]
        self.password = g_adsl_account["password"]

    #==============================================================================
    # set_adsl : 修改adsl设置
    #==============================================================================
    def set_adsl(self, account):
        self.name = account["name"]
        self.username = account["username"]
        self.password = account["password"]

    #==============================================================================
    # connect : 宽带拨号
    #==============================================================================
    def connect(self):
        cmd_str = "rasdial %s %s %s" % (self.name, self.username, self.password)
        os.system(cmd_str)
        time.sleep(5)

    #==============================================================================
    # disconnect : 断开宽带连接
    #==============================================================================
    def disconnect(self):
        cmd_str = "rasdial %s /disconnect" % self.name
        os.system(cmd_str)
        time.sleep(5)

    #==============================================================================
    # reconnect : 重新进行拨号
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

#保存ip
def saveip(ip):
    f = open('ips.txt','a+')
    f.write(ip+'\n')
    f.close()

if __name__ == "__main__":
    while True:
        aa=Adsl()
        aa.reconnect()
        main()
