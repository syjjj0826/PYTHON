import socket
import socks
from urllib import request
import os

# socks.set_default_proxy(socks.SOCKS5, '127.0.0.1', 7890)
# socket.socket = socks.socksocket

btih = input()[-40:].upper().replace('L', '1')
# print('magnet:?xt=urn:btih:' + btih)

name = btih + '.torrent'
url = 'https://itorrents.org/torrent/' + name

headers = {
    'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36'
}

req = request.Request(url, headers=headers)
resp = request.urlopen(req)

path = 'D:\\ut\\' + name
with open(path, 'wb') as f:
    f.write(resp.read())

os.startfile(path)