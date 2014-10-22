#encoding: utf8
'''
Created on 2013-5-12

@author: Administrator
'''
import socket, os, sys,json

import argv_opt

import const

import util

import location_track_system
import multiprocessing

#端口
const.bindPort = 8888
#recv, send 包大小  1KB
const.packSize = 1024
#数据分隔符
const.dataSep = chr(0x2c)
#bus socket超时时间
const.busSocketTimeOut = 10

from  multiprocessing.connection import listener

connFd = None

def client():
    
    global run_thread, connFd
    
    run_thread.join()
    
    try:
        connFd = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
    except socket.error,msg:
        connFd = None
        sys.exit(msg)
    
    try:
        connFd.connect(("192.168.106.130", 8888))
    except socket.error, msg:
        connFd.close()
        connFd = None
        sys.exit(msg)

    sendData = {"command": "updateLocation", "data": {"uid": 1, "long": "1.0", "lat": "2.0"}}
    sendData = json.dumps(sendData)
    sendData = str(len(sendData)) + "," + sendData
    
    connFd.sendall(sendData)

    print connFd.recv(1024)
    
    connFd.shutdown(socket.SHUT_RDWR)
    connFd.close() 
    
    
if __name__ == "__main__":
    import timeit
    import thread
    import threading
    import time
    import signal
    
    r = 1
    n = 1
    opt = argv_opt.argv_opt('r:n:')
    opt.analysis()
    if opt.getOptValue('r') != None:
        r = opt.getOptValue('r')
    if opt.getOptValue('n') != None:
        n = opt.getOptValue('n')
   
    def handler(signum, frame):
        global connFd
        
        connFd.close()
        print 'quit'
        sys.exit()
    
    #响应ctrl + c
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)

    #timeit.timeit("client()", "from __main__ import client", timeit.default_timer, 2)
    def test():
        print timeit.repeat("client()", "from __main__ import client", timeit.default_timer, int(r), int(n))
        
    flag = 0
    
    def t_start():
        global flag
        flag  = 1
    
    def t_stop():
        global flag
        while not flag:
            time.sleep(1)
    
    #===========================================================================
    # thread.start_new_thread(t_stop, ())
    # time.sleep(30)
    #===========================================================================
    
    run_thread = threading.Thread(target = t_stop, args = ())
    #主线程结束时会kill子线程
    run_thread.setDaemon(True)
    run_thread.start()
   
    for i in range(1, 2):
        test_t = threading.Thread(target=test, args = ())
        test_t.setDaemon(True)
        test_t.start()
    
    #开启   
    t_start()
    
    connFds = {}; onlineUsers = {}; curUser = ''; pushClient_uuid = util.getUUid()
    def createSocket(type):
        '''创建sock
        
        '''
        global connFds
        
        if (type not in connFds) or (not connFds[type]):
            try:
                connFds[type] = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
                #connFd.setsockopt(level, option, value)
            except socket.error,msg:
                connFds[type] = None
                sys.exit(msg)
            
            try:
                connFds[type].connect(("192.168.106.130", 8888))
            except socket.error, msg:
                connFds[type].close()
                connFds[type] = None
                sys.exit()
    
  
    def sendMessage(msg = '', type = 'mainChat', onFinishClose = False):
        '''发送信息, 返回回应.
        
        '''
        global connFds
         
        createSocket(type)
        
        connFd = connFds[type]
        
        #转成json字符串
        sendData = json.dumps(msg)
        sendData = str(len(sendData)) + "," + sendData
        #发到服务端
        connFd.sendall(sendData)
        #解析服务端返回的数据
        
        firstBuf = connFd.recv(const.packSize)
        firstCommaPos = firstBuf.find(const.dataSep)  
            
        if firstCommaPos != -1:
            dataLen = firstBuf[0:firstCommaPos]
            recvMsg = firstBuf[firstCommaPos+1:]
            
            while (len(recvMsg) < int(dataLen)):
                recvMsg = recvMsg + connFd.recv(const.packSize)
                
        if onFinishClose:
            connFd.shutdown(socket.SHUT_RDWR)
            connFd.close()
            connFd = None
            del connFds[type]
        
        if recvMsg and recvMsg.find('{'):
            recvMsg = json.loads(recvMsg)
            return recvMsg
        elif recvMsg:
            return recvMsg
        return None
            
        #connFd.shutdown(socket.SHUT_RDWR)
        #connFd.close() 
        
    #长连接recv信息  
    def recvMessage(type = 'mainChat'):
        global connFds
         
        createSocket(type)
        
        connFd = connFds[type]
        
        firstBuf = connFd.recv(const.packSize)
        firstCommaPos = firstBuf.find(const.dataSep)  
            
        if firstCommaPos != -1:
            dataLen = firstBuf[0:firstCommaPos]
            recvMsg = firstBuf[firstCommaPos+1:]
            
            while (len(recvMsg) < int(dataLen)):
                recvMsg = recvMsg + connFd.recv(const.packSize)
            
            if recvMsg and recvMsg.find('{'):
                recvMsg = json.loads(recvMsg)
                return recvMsg
            elif recvMsg:
                return recvMsg
        return None
        
                
    
    #注册会员
    def reg():
        userName = raw_input("请输入要注册的用户名:")
        if userName:
            msg = {"command": "reg", "data": {"username": userName}}
            recvData = sendMessage(msg = msg, type = 'reg', onFinishClose = True)
            if recvData:
                print recvData
                return True
        return None
            
            
    #登陆
    def login():
        global pushClient_uuid
        userName = raw_input("请输入要登陆的用户名:")
        if userName:
            msg = {"command": "login", "data": {"username": userName, "pushClient_uuid": pushClient_uuid}}
            recvData = sendMessage(msg = msg, type = 'mainChat')
            if type(recvData)== 'str':
                print recvData
                return False
            else:
                global onlineUsers, curUser
                onlineUsers = recvData
                #当前用户
                curUser = userName    
                return True
        return None
            
    #获取在线用户
    def getOnlineUsers():
        global onlineUsers
        
        print "online users:"
        i = 1
        for name in onlineUsers:
            print str(i) + ". " + name
    
    #新的在线用户       
    def addOnlineUsers(users):
        global onlineUsers
        
        if users:
            for newName in users:
                if newName not in onlineUsers:
                    onlineUsers[newName] = users[newName]
        
        print "新增上线的用户:"
        for newName in users:
            print newName
        getOnlineUsers()
   
    #推送客户端
    def pushClient():
        global curUser, pushClient_uuid
        msg = {"command": "pushClient_reg", "data": {"pushClient_uuid": pushClient_uuid}}
        recvData = sendMessage(msg = msg, type = 'pushClient')
        if recvData:
            print recvData
        while True:
            print recvMessage(type = 'pushClient')
            time.sleep(5)
            
                   
    #聊天
    def chat():
        #开启子线程，获取服务端推送的信息
        pushClient_t = threading.thread(target = pushClient, args = {})
        pushClient_t.setDaemon(True)
        pushClient_t.start()
        pushClient_t.join()
        
        #登录
        if login():
            #在线用户
            getOnlineUsers           
            
            toChatUserName = raw_input("请输入你要聊天的用户名:")
            
            if toChatUserName:
                toContent = raw_input("请输入聊天内容:")
                if toContent:
                    msg = {"command": "IMByServer", "data": {"tochatusername": toChatUserName, 'tocontent': toContent}}
                    recvData = sendMessage(msg = msg, type = 'mainChat')
                    
                
        else:
            help()
    
    #获取nat 类型
    def getNatType(other_client_ip, other_client_port):
        #尝试三次，如果不通就认为非clone nat
        
        clientSock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, 0)
        clientSock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        
        clientSock.connect(other_client_ip, other_client_port);
        
        
        
        
        
        
    
    #帮助
    def help():
        print "r: test()\n\
               reg: reg()\n\
               chat:chat()" 
        
        
        
    while True:
        help()
        s = raw_input("请选择命令:")
        if s == 'r':
            test()
        elif s == 'reg':
            reg()
        elif s == 'chat':
            chat()