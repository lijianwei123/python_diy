#!/usr/bin/python
# -*- coding: utf-8 -*-

http://www.dengdeng.name/u/deng/archives/2011/108.html

import socket
import traceback

HOST = ''
PORT = 8001

def main():
  s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  s.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
  s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
  s.bind((HOST,PORT))

  while True:
      try:
          msg,addr = s.recvfrom(1024)
          print "Received message from %s: %s"%(addr,msg)
          s.sendto("Welcome",addr)
      except (KeyboardInterrupt,SystemExit):
          raise
      except:
          traceback.print_exc()
   
if __name__ == '__main__':
  main()       


client


#!/usr/bin/python
# -*- coding: utf-8 -*-

import socket
import sys


def main():
  desc = ('<broadcast>',8001)
  s = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
  s.setsockopt(socket.SOL_SOCKET,socket.SO_BROADCAST,1)
  s.sendto("Hello,server",desc)
  while True:
      msg,addr = s.recvfrom(1024)
      if not len(msg):
          break
      print "Received message from %s: %s"%(addr,msg)
   
if __name__ == '__main__':
  main()
