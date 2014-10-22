#encoding: utf8
'''
Created on 2013-5-30

@author: Administrator
'''

import location_track_system 

import location_track_user

import time

import const

import json

class PushServer:
    
    #客户端id
    clientIds = {}
    
    #待推送的消息
    toBePushs = {}
    
    
    
    @staticmethod
    def push2Client():
        '''推送给客户端.
        
        '''
        global location_track_system.condLock
        global location_track_system.serv_obj
        
        __conn = None
        __sucMsg = None
        
        while True:
            if condLock.acquire():
                if PushServer.toBePushs:
                    for clientId in PushServer.toBePushs:
                        for userName in location_track_user.location_track_user.onlineUsers:
                            __conn = location_track_system.serv_obj.connections[PushServer.__getFileNoByUserName(userName)]
                            __sucMsg = {"command": "online_notify", "data": {"username": userName}}
                            
                            #转成json字符串
                            sucMsg = json.dumps(__sucMsg)
                            
                            PushServer.successReturn(sucMsg, __conn)
                        
                else:
                    condLock.wait()
                condLock.release()
                time.sleep(5)
                
    @staticmethod
    def __getClientIdByUserName(userName = ''):
        '''.
        
        '''
        if PushServer.clientIds:
            for clientId in PushServer.clientIds:
                if PushServer.clientIds[clientId]['username'] == userName:
                    return clientId
        return None
    
    @staticmethod
    def __getFileNoByUserName(userName = ''):
        '''.
        
        '''
        clientId = PushServer.__getClientIdByUserName(userName)
        if clientId:
            return PushServer.clientIds[clientId]['fileno']
        return None
    
    @staticmethod
    def successReturn(conn, sucMsg):
        sucMsg = str(len(sucMsg)) + const.dataSep + sucMsg
        
        while True:
            sendLen = 0
            sendLen += conn.send(sucMsg[sendLen:const.packSize])
            if sendLen == len(sucMsg):
                break
    
        