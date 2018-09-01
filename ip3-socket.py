import socket
import socks
import requests
 
socks.set_default_proxy(socks.SOCKS5, "14.63.226.163", 9999)
socket.socket = socks.socksocket
print(requests.get('http://api.ipify.org?format=json').text)
