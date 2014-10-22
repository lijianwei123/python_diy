#encoding: utf-8
'''自定义linux服务调用  类似于MVC方式调用
Created on 2013-7-23

@author: lijianwei
'''


import os, sys
import socket
import signal
import json
sys.path.append('..')
sys.path.append('extpython')
import util
from MVC import MVC


PORT = 88888

def handler(signum = None, frame = None):
    global sock
    if sock:
        sock.close()
    sys.exit('quit')
    
#信号处理
signal.signal(signal.SIGINT, handler) #ctrl + c
signal.signal(signal.SIGTERM, handler) #kill pid



sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind(('', PORT))
sock.listen(5)

while(True):
    conn, address = sock.accept()
    recvData = conn.recv(1024 * 100) #100KB
    if '{' in recvData:
        decodeData = json.loads(recvData)
        if ('pathinfo in decodeData') and decodeData['pathinfo']:
            pathinfo = decodeData['pathinfo']
            MVC.router(conn, pathinfo, decodeData['params'])
            conn.close()
    else:
       continue
