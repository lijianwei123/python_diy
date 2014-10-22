#encoding: utf8
'''位置跟踪系统服务端.

类似公交车控制台  显示  
网页版   用php  ppython  node.js 
手机版  andorid
Created on 2013-5-10

@author: Administrator
'''

import os,sys,socket,select,threading,json,logging,logging.handlers,traceback

import signal, subprocess

import const

import location_track_user

import push_server

import p2p_chat


#端口
const.bindPort = 8888
#处理队列长度
const.listenNum = 20
#recv, send 包大小  1KB
const.packSize = 1024
#数据分隔符
const.dataSep = chr(0x2c)
#bus socket超时时间
const.busSocketTimeOut = 10
#调试
const.debug = True

const.commands = ['updateLocation', 'readLocation', 'reg', 'login', 'getUsers', 'IMByServer']


#子进程
g_subUnix = None

#线程可重用锁
rLock = threading.RLock()

#线程条件锁
condLock = threading.Condition()

#服务端obj
serv_obj = None

#服务端
class server:
    def __init__(self):
        self.epoll = None
        self.serversocket = None
        self.subUnix = None
        
        self.connections = {}
        self.addresses = {}
        self.threads = {}
        
        #主线程响应ctrl + c
        signal.signal(signal.SIGINT, self.handler)
        signal.signal(signal.SIGTERM, self.handler)
    
    def handler(self, signum, frame):
        self.finish()
        pass
    
    def __del__(self):
        #self.finish()
        #del self.connections
        #del self.addresses
        #del self.threads
        pass
        
        
    def start(self):
        try:
            logger.info("start location_track_system")
            
            self.serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0)
            #设置端口重用    修正  Address Already In Use 错误   参考http://www.2cto.com/kf/201208/150347.html
            self.serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.serversocket.setblocking(False)
            self.serversocket.bind(('0.0.0.0', const.bindPort))
            self.serversocket.listen(const.listenNum)
            
            #开启子进程
            global g_subUnix
            g_subUnix = self.subUnix = subprocess.Popen('python subUnix.py', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
            
            #开启子线程 推送消息  tcp
            pushServer_t = threading.thread(target = push_server.PushServer.push2Client, args = {})
            pushSerer_t.setDaemon(True)
            pushServer_t.start()
            #开启子线程  p2p  chat udp
            p2pChat_t = threading.thread(target = p2p_chat.P2pChat.start, args = {})
            p2pChat_t.setDaemon(True)
            p2pChat_t.start()
            
            
            self.epoll = select.epoll()
            
            self.epoll.register(self.serversocket.fileno(), select.EPOLLIN)
            
           
            while True:
                #epoll监听事件， 1秒没有事件退出
                self.epoll_list = self.epoll.poll(1)
                
                for fd,events in self.epoll_list:
                    if fd == self.serversocket.fileno():
                        conn,addr = self.serversocket.accept()
                        logger.info("客户端请求:fileno " + str(conn.fileno()) + ", address " + addr[0] + ":" + str(addr[1]))
                        self.connections[conn.fileno()] = conn
                        self.addresses[conn.fileno()] = addr
                        self.threads[conn.fileno()] = busProcess(self, conn, addr)
                        #true 主线程关闭时，会kill子线程   false等子线程关闭时，才关闭  就算按ctrl + c 也不能关闭主线程
                        self.threads[conn.fileno()].setDaemon(True)
                        self.threads[conn.fileno()].start()
                    #长连接  读    
                    elif select.EPOLLIN & events:
                        self.threads[fd] = busProcess(self, self.connections[fd], self.addresses[fd])
                        self.threads[fd].setDaemon(True)
                        self.threads[fd].start()
                    #有中断时    
                    elif select.EPOLLHUP & events:
                        fd.unregister(fd)
                        self.connections[fd].close()
                        
                        del self.connections[fd]
                        del self.addresses[fd]
                        del self.threads[fd]
                        
                        
                        
                    
                
        except KeyboardInterrupt:
            print sys.exc_info()[:1]
        except Exception,e:
            print traceback.format_exc()
            #pass
        finally:
            self.finish()
    
    def finish(self):
            try:
                if self.epoll:
                    self.epoll.unregister(self.serversocket.fileno())
                    self.epoll.close()
                    self.epoll = None
                    
                if self.serversocket:
                    self.serversocket.shutdown(socket.SHUT_RDWR)
                    self.serversocket.close()
                    self.serversocket = None
                
                for fileno in self.connections:
                    self.connections[fileno].close()
                
                #self.subUnix.poll None表示子进程未终止
                if self.subUnix and (not self.subUnix.poll):
                    #关闭子进程
                    self.subUnix.terminate() #发送SIGTERM信号
                    #等待子进程结束
                    self.subUnix.wait()
                 
                sys.exit('quit')
            except Exception, e:
                print traceback.format_exc()
                #pass
                                          
#业务处理
class busProcess(threading.Thread):
    def __init__(self, parent, socket, addr):
        threading.Thread.__init__(self)
        self._socket = socket
        self._addr = addr
        self.parent = parent
        self.onFinishClose = True
        
        self._socket.settimeout(const.busSocketTimeOut)
        
    def __del__(self):
        #self.finish()
        pass
        
    def run(self):
        '''数据包格式   数据包大小,真正的数据   中间以逗号隔开.
        
        '''
        try:
            firstBuf = self._socket.recv(const.packSize)
            firstCommaPos = firstBuf.find(const.dataSep)  
            
            if firstCommaPos != -1:
                dataLen = firstBuf[0:firstCommaPos]
                recvMsg = firstBuf[firstCommaPos+1:]
                
                while (len(recvMsg) < int(dataLen)):
                    recvMsg = recvMsg + self._socket.recv(const.packSize)
                
                #具体业务处理
                recvMsgPy = json.loads(recvMsg) #json_decode
                self.process(recvMsgPy)
                
                #self.successReturn('操作成功')
                
            else:
                self.errReturn("数据包格式不正确:")
        except Exception, e:
            self.errReturn("业务处理出现异常:" + traceback.format_exc())
        
        finally:
            self.finish()
            
    def process(self, recvMsgPy):
        '''数据格式
        
        {"command": "updateLocation", "data": {"uid": 1, "long": "1.0", "lat": "2.0"}}.
        '''
        try:   
            if ('command' in recvMsgPy) and (recvMsgPy['command'] in const.commands):
                command = recvMsgPy['command']
                data = recvMsgPy['data']
                
                #更新位置
                if command == 'updateLocation':
                    if data:
                        loc_obj.updateLocation(**data)
                        self.successReturn('操作成功')
                #读取位置
                elif command == 'readLocation':
                    pass
                #注册
                elif command == 'reg':
                    if location_track_user.reg(data.username):
                        self.successReturn('注册成功')
                    else:
                        self.errReturn('用户名:' + data.username + '已经注册')
                #推送客户端id注册
                elif command == 'pushClient_reg':
                    if (pushClient_uuid in data) and data['pushClient_uuid']:                    
                        #长连接
                        self.onFinishClose = False
                        self._socket.settimeout(None)
                        
                        push_server.clientIds[pushClient_uuid] = {'fileno': self._socket.fileno(), 'username': ''}
                        self.successReturn('pushClient_reg success')
                              
                #登陆
                elif command == 'login':
                    if location_track_user.login(data['username'], self._addr):
                        
                        #长连接
                        self.onFinishClose = False
                        self._socket.settimeout(None)
                        
                        #更新push_server中clientIds
                        push_server.clientIds[data['pushClient_uuid']]['username'] = data['username']
                        
                        #告诉其他在线用户我上线了
                        if condLock.acquire():
                            push_server.PushServer.toBePushs[data['pushClient_uuid']] = {'username': data['username']}
                            condLock.notify(1)#唤醒一个线程
                            condLock.release()
                        
                        #获取在线用户列表
                        self.successReturn(location_track_user.onlineUsers)
                        
                        #注册到epoll列表
                        self.parent.epoll.register(self._socket.fileno(), select.EPOLLIN|select.EPOLLET) #读数据
                        
                    else:
                        self.errReturn('用户名:' + data.username + '登陆失败')
                #通过服务器聊天
                elif command == 'IMByServer':
                    toChatUserName = data.tochatusername
                    toContent = data.tocontent
                    
                    toConn = push_server.PushServer.__getFileNoByUserName(toChatUserName)
                    msg = {'command': 'chatFromServer', "data": {"tocontent": toContent}}
                    sendMsg = json.dumps(msg)
                    toConn.sendall(sendMsg)
                
            else:
                self.errReturn("数据包格式不正确:")
        except Exception, e:
            print traceback.format_exc()
            #self.errReturn("业务处理出现异常:")
        
   
    def errReturn(self, errMsg):
        if not const.debug:
            errMsg = '操作失败'
        
        errMsg = str(len(errMsg)) + const.dataSep + errMsg
        
        while True:
            sendLen = 0
            sendLen += self._socket.send(errMsg[sendLen:const.packSize])
            if sendLen == len(errMsg):
                break
            
    #成功返回
    #sucMsg string 
    def successReturn(self, sucMsg):
        sucMsg = str(len(sucMsg)) + const.dataSep + sucMsg
        
        while True:
            sendLen = 0
            sendLen += self._socket.send(sucMsg[sendLen:const.packSize])
            if sendLen == len(sucMsg):
                break
     
    def finish(self):
        try:
            if self._socket and self.onFinishClose:
                logger.info("客户端请求:fileno " + str(self._socket.fileno()) + "正在关闭")
                del self.parent.connections[self._socket.fileno()]
                del self.parent.addresses[self._socket.fileno()]
                del self.parent.threads[self._socket.fileno()]
                
                self._socket.shutdown(socket.SHUT_RDWR)
                self._socket.close()
                self._socket = None
                logger.info("客户端请求 关闭")
            elif self._socket:
                del self.parent.threads[self._socket.fileno()]
                
        except Exception:
             self.errReturn("finish:" + traceback.format_exc())
        
           

#位置类
class location:
    def __init__(self):
        pass
    
    def updateLocation(self, **kwargs):
        logger.info('更新位置: ' + str(kwargs))
        global g_subUnix
        output, err = g_subUnix.communicate(str(kwargs))
        
    
    def readLocation(self):
        pass
    
if __name__ == '__main__':
    logger = logging.Logger("location_track_system")
    logger.setLevel(logging.DEBUG)
    
    #最多备份5个日志文件，每个日志文件最大10M
    rtHandler = logging.handlers.RotatingFileHandler("location_track_system.log", maxBytes = 10*1024*1024, backupCount=5)
    rtHandler.setLevel(logging.DEBUG)
    formatter = logging.Formatter("%(asctime)s-%(name)s-%(levelname)s-%(filename)s[line:%(lineno)d]-%(message)s")
    rtHandler.setFormatter(formatter)
    
    console = logging.StreamHandler()
    console.setLevel(logging.DEBUG)
    console.setFormatter(formatter)
    
    logger.addHandler(rtHandler)
    logger.addHandler(console)
    
    loc_obj = location()
    
    serv_obj = server()
    serv_obj.start()