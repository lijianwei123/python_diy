'''
Created on 2013-7-23

@author: Administrator
'''
import os,sys
sys.path.append('..')
import util
import json

class MVC:
    def __init__(self):
        pass
    @staticmethod
    def router(conn, pathinfo, params = {}):
        controller, action = pathinfo.split('/')
        if util.checkModule(controller):
            obj = getattr(controller, controller)(conn)
            if util.method_exists(obj, action):
                getattr(obj, action)(**params)
           
