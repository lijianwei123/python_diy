# -*- coding: utf-8 -*-


import os, sys
from Queue import Empty

'''
ftp_dir = "lijianwei"
list = [ftp_dir]
[list.append(os.linesep) for i in range(11)]


ftp_user_config_str = "local_root={0}{1}\
    anonymous_enable=NO{2}\
    write_enable=YES{3}\
    local_umask=022{4}\
    anon_upload_enable=NO{5}\
    anon_mkdir_write_enable=NO{6}\
idle_session_timeout=600{7}\
data_connection_timeout=120{8}\
max_clients=10{9}\
max_per_ip=5{10}\
local_max_rate=50000{11}".format(*list)
               
print ftp_user_config_str
'''

'''
ftp_dir = "lijianwei"
list = [ftp_dir]
[list.append(os.linesep) for i in range(11)]
print list;
'''

 
# import commands
# 
# 
# (status, output) = commands.getstatusoutput("ipconfig")
# 
# print status
# print output

# import threading
# 
# def test():
#     basename = os.path.basename("/home/data/wwwroot/.py")
#     if basename.startswith('.'):
#         print "test"
# t = threading.Thread(target=test)
# t.start()


# def test(name = None, sex = None):
#     print name
#     print sex
#     
# test(sex="male")
# 
# class A:
#     def func(self, a, b):
#         return a + b
# 
# a = A()
# print getattr(a, 'func')(2, 3)


# print os.getpid()
#     


# class A(object):
#     def __init__(self):
#         print "Inside class A init"
#  
# class B(A):
#     def __init__(self):
#         A.__init__(self)
#         print "Inside class B init"
#          
# B()

# 
# def fun1():
# 
#     gl.gl_1 = 'Hello'
# 
#     gl.gl_2 = 'World'
# 
# def modifyConstant() :  
# 
#     global CONSTANT  
# 
#     print CONSTANT  
# 
#     CONSTANT += 1  
# 
#     return  
# 
# 
# 
# if __name__ =='__main__' :  
#     
#     CONSTANT = 10
#     
#     modifyConstant()  
# 
#     print CONSTANT  


# import test2
# 
# 
# test2.map['name'] = "lijianwei"
# 
# import test3
# 
# print test2.map

# def test(name):
#     print name
#     
# test("lijianwei", '123')

# import socket
# 
# print socket.INADDR_ANY

# import inspect
# 
# def compact(*names):
#     print names
#     caller = inspect.stack()[1][0] # caller of compact()
#     vars = {}
#     for n in names:
#         if n in caller.f_locals:
#             vars[n] = caller.f_locals[n]
#         elif n in caller.f_globals:
#             vars[n] = caller.f_globals[n]
#     return vars
# 
# li = "123"
# jianwei = "456"
# 
# print compact("li", "jianwei")

# def test(*args):
#     print args
#     
# list = (1, 2, 3)
# test(*list)

# print 1111111111111111111111111111111111111111 + 1

# print 0 < 0 == 0

# import Queue
# 
# q = Queue.Queue()
# print id(q)

# print not bool(0)

# import os
# 
# os.unlink("123")


# class test():
#     def __init__(self):
#         pass
#     
#     @classmethod
#     def a():
#         print "a"
#         
#   
#     def __del__(self):
#         print "del"


# import collections
# 
# q = collections.deque()
# q.append("123")
# q.append("3234")
# print len(q)

# print len({"command": "", "filePath": ""})

# import collections
# 
# d = {"name": 'lijianwei', 'sex': 'male'}
# 
# print d.pop(0)

# first, second, third = (1, 2, 3)
# 
# print second

# a = (1, 2, 3)
# print "command:%s, extraInfo: %s, pos: %d" %a

# try:
#     raise IndexError
# except:
#     raise
#     print "123"
# else:
#     print "312"

import errno
from errno import EALREADY, EINPROGRESS, EWOULDBLOCK, ECONNRESET, EINVAL, \
     ENOTCONN, ESHUTDOWN, EINTR, EISCONN, EBADF, ECONNABORTED, EPIPE, EAGAIN, \
     errorcode
  
_DISCONNECTED = frozenset((ECONNRESET, ENOTCONN, ESHUTDOWN, ECONNABORTED, EPIPE,
                           EBADF))
  
print _DISCONNECTED


# class Test(object):
#  
#     def InstanceFun(self):
#         print("InstanceFun");
#         print(self);
#  
#     @classmethod
#     def ClassFun(cls):
#         print("ClassFun");
#         print(cls);
#  
#     @staticmethod
#     def StaticFun():
#         print("StaticFun");
#  
# 
#  
#  
# t = Test();
# t.InstanceFun();
# 
# Test.ClassFun();
# 
# Test.StaticFun();
# t.StaticFun();
# 
# t.ClassFun();
# Test.InstanceFun(t);
# Test.InstanceFun(Test);

# print os.name


# print EINPROGRESS, EALREADY, EWOULDBLOCK


# def test():
#     pass
#     print "123"
#     
# test()


watchPath = {}
watchPath['test'] = '/data/test/f3.v.veimg.cn/'

for i in watchPath:
    print i, watchPath[i]