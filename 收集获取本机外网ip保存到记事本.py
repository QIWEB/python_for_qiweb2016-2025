#!/usr/bin/env python
# -*- coding:utf-8 -*-

import os
import time
import requests


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
    main()
