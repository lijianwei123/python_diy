'''
Created on 2013-7-23

@author: Administrator
'''
import os, sys
import json

from base import  base

class addftpconfig(base):
    vsftp_config_file = None
    vsftp_userconfig_dir = None
    def __init__(self, conn = None):
        self.conn = conn
        self.getConfigFile()
        self.getUserConfigDir()
    def addItem(self, **params):
        ftp_dir = params.get('ftp_dir')
        ftp_user = params.get('ftp_user')
        ftp_pwd = params.get('ftp_pwd')
        if self.user_exist(ftp_user):
            self.respStr(base.codeMap.get('error'), 'ftp use yet exist')
        #添加ftp用户
        vir_user_path = os.path.basename(addftpconfig.vsftp_userconfig_dir) + os.sep + 'vir_user' 
        cmd = "echo " + ftp_user + os.linesep + ftp_pwd + ">>" + vir_user_path
        os.system(cmd)
        #添加ftp 用户的对应的配置文件
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
        cmd = "cd " + addftpconfig.vsftp_userconfig_dir + " && cat " + ftp_user + " && echo " + ftp_user_config_str + " > " + ftp_user
        os.system(cmd)
        #重启服务
        cmd = "service vsftpd db-load && service vsftpd restart"
        os.system(cmd)
        #返回结果
        self.respStr(base.codeMap.get('success'))
       
    def user_exist(self, ftp_user = None):
        '''检测ftp用户是否存在.
        
        Args:
            ftp_user: ftp用户名
        Returns:
            True or False.
        
        '''
        return os.path.exists(addftpconfig.vsftp_userconfig_dir + os.sep + ftp_user)
        
    def getConfigFile(self):
        '''获取配置文件位置.
        
        '''
        f = os.popen("ps -ef|grep  [v]sftpd|awk '{print $9}'", 'r') #可读写
        addftpconfig.vsftp_config_file = f.read().strip()
    def getUserConfigDir(self):
        '''获取vsftp配置文件中的user_config_dir.
        
        '''
        f = os.popen("grep -i 'user_config_dir' " + addftpconfig.vsftp_config_file, 'r');
        addftpconfig.vsftp_userconfig_dir = f.read().strip();