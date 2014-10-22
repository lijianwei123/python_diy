#encoding: utf8
'''
Created on 2013-4-12

@author: Administrator
'''

def checkModule(module_name):
    '''检测模块是否存在.
    
    @param module_name: 模块名.
    '''
    try:
        __import__(module_name)
        return True
    except ImportError:
        return False


def getOsType():
    '''获取操作系统类型.
             
     1  windows
     2  linux
     3  other
    '''
    import platform
    os = platform.system().upper()
    if os.find('WINDOW') != -1:
        return 1
    elif os.find('LINUX') != -1:
        return 2
    else:
        return 3

def countFileRows(filePath):
    '''统计文件行数.
    '''
    import fileinput
    for line_str in fileinput.input(filePath):
        pass
    return fileinput.lineno()
    
    #===========================================================================
    # count = 0
    # os_type = getOsType()
    # if os_type == 1:
    #     count = -1
    #     for count, line in enumerate(open(filePath, 'rU')):
    #         pass
    #     count += 1
    # else:
    #     import os
    #     count = os.system("wc -l " + filePath)
    # return count
    #===========================================================================
    
 
  
def getdirsize(dir):  
    '''计算目录大小
    
    '''
    import os
    from os.path import join, getsize 
    size = 0
    for root, dirs, files in os.walk(dir):  
       size += sum([getsize(join(root, name)) for name in files])  
    return size

def countOccurSubstrNum(str, substr):
    '''计算子字符串出现的次数
    @param str:  字符串
    @param substr: 子字符串 
    '''
    
    import re
    return len(re.findall(substr, str))

def getUUid():
    import uuid
    return uuid.uuid1()
def method_exists(obj, method_name):
    return hasattr(obj, method_name) and callable(getattr(obj, method_name))
    