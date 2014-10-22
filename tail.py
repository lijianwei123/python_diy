#encoding: utf8
'''类linux tail 支持大文件
Created on 2013-5-9

@author: lijianwei
'''


import sys, os
import util
import argv_opt
import time

# argv = sys.argv
# os_type = util.getOsType

def usage():
    print '''
        py price.py [option][value]...
        -h or --help
        -f or --file 文件路径
    '''

opt_obj = argv_opt.argv_opt('hf:', ['help', 'file='])

line_num = 10

# 如果没有任何选项
if not opt_obj.analysis():
    usage()
    sys.exit(1)

is_help = (opt_obj.getOptValue('h') != None) or (opt_obj.getOptValue('help') != None)


if is_help:
    usage()
    sys.exit(0)

# 获取文件路径
filepath = opt_obj.getOptValue('f') or opt_obj.getOptValue('file')

# 文件路径不能是目录
if os.path.isdir(filepath):
    print filepath + " can't be dir!"
    sys.exit(1)

# 文件路径必须存在
if not os.path.exists(filepath):
    print filepath + " don't exist!"
    sys.exit(1)
    

def litterRowsTail():
    # 文件行数
    fileRowNums = util.countFileRows(filepath)
    
    # 开始行数
    start = max(fileRowNums - 10, 0) + 1
    
    while True:
        try:
            import linecache, time
            line_str = linecache.getline(filepath, start)
            if line_str:
                print line_str,
                start = start + 1
                time.sleep(0.01)
            else:
                linecache.clearcache()
            
        except ImportError:
            print ''
            print 'error!'
            sys.exit(1)
        except KeyboardInterrupt:
            print ''
            print 'quit!'
            sys.exit(1)

def largeRowsTail():
    try:
        '''
        \r\n windows 换行
        \n 类unix 换行
        \r 其他
        '''
        line_breaks = ['\r', '\n', '\r\n']
        #检测换行符
        fp = open(filepath, 'rb')
        first_line = fp.readline()
        
        if not first_line[-2:].rstrip(line_breaks[2]):
            break_flag = 2
        elif first_line[-2:].find(line_breaks[0]) != -1:
            break_flag = 0
        else:
            break_flag = 1
            
        #初始化位置
        fp.seek(0)
        read_byte = 1
        step = 1

        
        read_str = ""
        
        #计算开始位置
        while True:
            fp.seek(-(read_byte), os.SEEK_END)
            read_str = fp.read(step) + read_str
            if util.countOccurSubstrNum(read_str, line_breaks[break_flag]) < line_num:
                read_byte = read_byte + step
                continue
            else:
                break
            
        start = read_byte - len(line_breaks[break_flag])
        
        fp.seek(-start, os.SEEK_END)
        
        while True:
            line_str = fp.readline()
            if line_str:
                print line_str,
                time.sleep(0.01)
            else:
                time.sleep(0.01)
            
    except KeyboardInterrupt:
            print ''
            print 'quit!'
            sys.exit(1)
        
    
    
    
if __name__ == '__main__':
    #1M左右
    if os.path.getsize(filepath) < 1024*1024:
        litterRowsTail()
    else:
        largeRowsTail()
