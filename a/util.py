'''
Created on 2014-7-19

@author: Administrator
'''


import time

def getNowTime():
    return  time.strftime('%Y-%m-%d %H-%M-%S',time.localtime(time.time()))