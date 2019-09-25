import socket
#import socks
import requests
 
#socks.set_default_proxy(socks.SOCKS5, "127.0.0.1", 9050)
#socket.socket = socks.socksocket
print(requests.get('http://api.ipify.org?format=json').text)
import json

json1 = '{"retcode":3,"errmsg":"\u4eca\u65e5\u89c2\u770b\u6b21\u6570\u5df2\u770b\u5b8c\uff0c\u8bf7\u70b9\u51fb\u514d\u8d39\u6ce8\u518c\u4f1a\u5458\u83b7\u53d6\u66f4\u591a\u5f71\u7247\u89c2\u770b\u6b21\u6570\u3002","data":{"xxx_api_auth":"3235346331653035353361343837663033356434346565383564363630303239","isfavorite":0,"httpurl_preview":"https:\/\/v1.xinliangfc.com\/20171206\/tG3xL6Qh\/index.m3u8?300"}}';

text = json.loads(json1)
print(text["retcode"])

from html.parser import HTMLParser
import urllib.parse

escape_str = '%u5728%u7ebf%u64ad%u653e%24https%3A%2F%2Fdadi-bo.com%2Fshare%2FZnvYTXO3rKYBDJUs%24%24%24%u5728%u7ebf%u64ad%u653e%24https%3A%2F%2Fdadi-bo.com%2F20181211%2FNLPhl10R%2Findex.m3u8'
str1 = escape_str.replace('%u', '\\u')
# 得到结果 str1 = '\u4eba\u751f\u82e6\u77ed'
str = str1.encode('utf-8').decode('unicode_escape')
print(str)

print(urllib.parse.unquote(str))


html = escape_str
html_parser = HTMLParser()
txt = html_parser.unescape(html)
print(txt)