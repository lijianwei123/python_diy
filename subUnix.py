#encoding: utf8
'''
Created on 2013-5-21

@author: Administrator
'''

import sys, signal, socket, os, select

def handler():
    pass

signal.signal(signal.SIGTERM, handler)

#本地unix socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
sock_path = "/tmp/subUnix"
if os.path.exists(sock_path):
    os.unlink(sock_path)
sock.bind(sock_path)
sock.listen(5)

infds, outfds, errfds = select.select([sock,],[],[],5)  
if len(infds) != 0:  
   con,addr = sock.accept()  
   print con.recv(1024)  
   con.close()  
   sock.close()  
print '5 seconds later no data coming' 


#传过来的数据
data = sys.stdin.read()






