# -*- coding: utf-8 -*-


import Queue

import os 

import time

# 
# def call(func):
#     def call_fn(fn):
#         return fn
#     return call_fn
# 
# @call
# def a(n):
#     value = []
#     for i in range(n):
#         value.append(i*i)
#     return value
# 
# print a(5)
# 
# 
# 
# 
# def p_decorate(func):
#    def func_wrapper(*args, **kwargs):
#        return "<p>{0}</p>".format(func(*args, **kwargs))
#    return func_wrapper
# 
# class Person(object):
#     def __init__(self):
#         self.name = "John"
#         self.family = "Doe"
# 
#     @p_decorate
#     def get_fullname(self):
#         return self.name+" "+self.family
# 
# my_person = Person()
# 
# print my_person.get_fullname()


# print os.getcwd()

# try:
#     raise IOError
# except IOError,e:
#     print "3231"
#     raise
# except:
#     print "123"

# watchPath = {}
# watchPath['test'] = '/data/test/f3.v.veimg.cn/'
# watchPath['test2'] = '/data/test2/f3.v.veimg.cn/' 

# print os.listdir('.')
# 
# def listDir(path = None):
#     l= os.listdir(path)
#     
#     dirs = []
#     files = []
#     
#     for file in l:
#         if not file.startswith('.'):
#             if os.path.isdir(file):
#                 dirs.append(file)
#             else:
#                 files.append(file)
#     return [dirs, files]
# 
# print listDir(".")

# print os.path.dirname('')


# import psutil
# 
# print psutil.virtual_memory().total / 1024 / 1024

# 
# s = 's'
# print type(s)

# import signal
# 
# def getNowTime():
#     return time.strftime('%Y-%m-%d %H-%M-%S', time.localtime(time.time()))
# 
# def handleAlarm(self, signum, frame):
#      print getNowTime()
# 
# 
# signal.signal(signal.SIGVTALRM, handleAlarm)
# signal.setitimer(signal.ITIMER_VIRTUAL, 1, 0.5)

# print not bool("lijianwie")

print range(2)