import ftplib
import os
import socket
import sys

class ftp:
    def __init__(self, **karg):
        try:
            self.f = ftplib.FTP()
            self.f.connect(karg.get('host', 'localhost'), karg.get('port', 21), karg.get('timeout', 30))
        except socket.timeout:
            print 'connect error'
    def login(self, *arg):
        try:
            self.f.login(arg[0], arg[1])
        except ftplib.error_perm:
            print 'login error'
            self.f.quit()

            
    def upload(self, local_file, remote_file):
        '''Ftp upload.
        
        Args:
            local_file: local file path.
            remote_file: remote file path.
        
        Returns:
            null.
        '''
        try:
            self.f.storbinary('STOR %s' %remote_file, open(local_file, 'rb'))
        except ftplib.error_perm:
            print 'upload error'
            return
        finally:
            self.f.quit()
            
        print 'upload success'

    
    def download(self, local_file, remote_file):
        try:
           self.f.retrbinary('RETR %s' %remote_file, open(local_file, 'wb').write)
        except ftplib.error_perm:
            print 'download error'
            os.unlink(local_file)
            return
        finally:
            self.f.quit()
            
        print 'download success'
        

def dict_merge(dict1, dict2):
    dict_merge = dict1.copy()
    dict_merge.update(dict2)
    return dict_merge
           
if __name__ == '__main__':
    default_setup = {'host': '', 'port': 21, 'timeout': 3}
    setup = {'host': '168.192.122.29'}
    setup = dict_merge(default_setup, setup)
    account = {'username': 'lijianwei', 'password': 'lijianwei'}
    
    f = ftp(**setup)
    f.login(*account.itervalues())
    
    remote_file = 'lijianwei.jpg'
    local_file = "D:\\123.jpg"
    
    f.download(local_file, remote_file)
 


        
