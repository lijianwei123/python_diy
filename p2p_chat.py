#encoding: utf8
'''
Created on 2013-5-30

@author: Administrator
'''
import os,sys
import socket
import json
import const

const.serverUdpPort = 6666

class P2pChat:
    udp_sock = None
    def __init__(self):
        pass
    
    @classmethod
    def start(self):
        P2pChat.udp_sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        P2pChat.udp_sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        P2pChat.udp_sock.bind(('0.0.0.0', const.serverUdpPort))
        while True:
           recvData, client_addr = P2pChat.udp_sock.recvfrom(8192) 
    
        
        
        