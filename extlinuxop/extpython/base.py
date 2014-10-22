'''
Created on 2013-7-23

@author: Administrator
'''
import os,sys
import json

class base:
    codeMap = {'success' : '0000', 'error': '9999'}
    
    def __init__(self):
        pass
    
    def respStr(self, code = '0000', msg = ''):
        '''返回结果.
        
        '''
        if not (code in base.codeMap.items()):
            code = base.codeMap.get('error')
            msg = 'Unknown Error'
        
        resp = {'code': code, 'msg': msg}
        self.conn.sendall(json.dumps(resp))
        self.conn.close()

