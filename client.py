#encoding: utf-8
'''
Created on 2013-4-16

@author: Administrator
'''
import socket
import time
import logging

logger = logging.getLogger("network-client")
logger.setLevel(logging.DEBUG)

fh = logging.FileHandler("network-client.log")
fh.setLevel(logging.DEBUG)

ch = logging.StreamHandler()
ch.setLevel(logging.ERROR)

formatter = logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s")
ch.setFormatter(formatter)
fh.setFormatter(formatter)

logger.addHandler(fh)
logger.addHandler(ch)

if __name__ == "__main__":
    try:
        connFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    except socket.error,msg:
        logger.error(msg)
    
    try:
        connFd.connect(("192.168.106.3", 2003))
        logger.debug("connect to network server success")
    except socket.error, msg:
        logger.error(msg)

    for i in range(1, 11):
        data = "The Number is %d" %i
        if connFd.send(data) != len(data):
            logger.error("send data to network server failed")
            break
        readData = connFd.recv(1024)
        print readData
        time.sleep(1)
    
    #发出关机命令
    command_str = 'reboot';
    if connFd.send(command_str) == len(command_str):
        print connFd.recv(1024)
      
    connFd.close()