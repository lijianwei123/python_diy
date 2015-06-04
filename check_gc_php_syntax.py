#/usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2015年6月4日

检测git commit php 语法正确
@author: lijianwei
'''

import os
import sys
import subprocess

#获取要commit的文件
def getGitCommitFiles():
    shell ='''git status -s|awk -F" " '{print $2}'
    '''
    
    gc = subprocess.Popen(shell, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
    gc.wait()
    
    gcFiles = gc.stdout.read()
    if gcFiles == "":
        return None
    else:
        return filter(None, str(gcFiles).split("\n"))
    
def getExtension(file):
    absolute_path = os.path.abspath(file)
    return os.path.splitext(absolute_path)[-1]
    
if __name__ == '__main__':
    gcFiles = getGitCommitFiles()

    if gcFiles != None:
        for file in gcFiles:
            if getExtension(file) == '.php':
                os.system("php -l " + file)
                
    sys.exit()