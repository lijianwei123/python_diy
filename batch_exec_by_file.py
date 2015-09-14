# /usr/bin/python
# -*- coding: utf-8 -*-

'''
Created on 2015年6月4日

批量执行脚本 参数从文件中获取

sample:
    python batch_exec_by_file.py --file=test.txt  --exec="wc -l %s"

@author: lijianwei
'''

import os
import sys
import subprocess

import argv_opt
from __builtin__ import file

def usage():
    print '''
        python batch_exec_by_file.py [option][value]...
        --file 参数文件  以换行符分割
        --exec 要执行脚本  `ls %s`
    '''

if __name__ == "__main__":
    opt_obj = argv_opt.argv_opt("", ['file=', 'exec='])
    
    if not opt_obj.analysis():
        usage()
        sys.exit(1)
        
    file = opt_obj.getOptValue("file")
    if file == None:
        file = "./sql_filed_search.py"
    
    exec_format = opt_obj.getOptValue('exec')
    
    if exec_format == None:
        print "exec lost"
        sys.exit(-1)
        
    
    if os.path.isfile(file) and os.path.exists(file):
        with open(file) as f:
            lines = [line.strip("\n") for line in f.readlines()]
            f.close()
         
        for arg in lines:
             exec_shell = str(exec_format) %(arg)
             print exec_shell
             gc = subprocess.Popen(exec_shell, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
             gc.wait()
    
             print gc.stdout.read()
           
         
        
            
