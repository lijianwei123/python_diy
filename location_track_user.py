#encoding: utf8

from  location_track_system import rLock

class location_track_user:
    '''定位系统会员.
    
    '''
    #临时保存用户  集合
    users = set()
    
    #临时保存在线用户
    onlineUsers = {}
    
    def __init__(self):
        pass
    
    #静态方法
    @staticmethod
    def reg(self, username):
        '''注册.
        
        @param username: string 用户名 
        @return: boolean
        '''
        
        #已经注册了
        if username in location_track_user.users:
            return False   
        else:
            location_track_user.users.add(username)
            return True
    
    @staticmethod
    def login(self, username, addr):
        '''登陆.
        
        @param username: string 用户名
        @return: boolean 
        '''
        
        #已经登陆了
        if username in location_track_user.onlineUsers:
            return False
        else:
            if username in location_track_user.users: 
                if rLock.acquire():
                    location_track_user.onlineUsers.setdefault(username, addr)
                    rLock.release()
                    return True
            else:
                return False
    @staticmethod
    def checkLogin(self, username):
        '''验证是否登录.
        
        '''
        if username in location_track_user.onlineUsers:
            return True
        else:
            return False
           
    #类方法 
    @classmethod
    def getUserFriends(self):
       pass 