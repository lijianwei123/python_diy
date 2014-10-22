#encoding: utf8
import getopt
import sys

def usage():
    print '''Help Information:
    -h: Show help information
    -xValue:
    ...'''

if __name__=='__main__':
    #set default values
    x=1
    y='y'

    try:
        #print sys.argv[1:]
        opts,args=getopt.getopt(sys.argv[1:],'hx:y:d')
        #opts 是带-选项的参数
        #args 是没有选项的参数
        print opts
        print args
        #h表示使用-h,h选项没有对应的值
        #x:表示你要使用-xValue,x选项必须有对应的值.
    except getopt.GetoptError:
        #打印帮助信息并退出
        usage()
        sys.exit(2)
    #处理命令行参数
    for o,a in opts:
        if o=='-h':
            usage()
            sys.exit()
        if o=='-x':
            try:
                x=x+int(a) #注意默认a为字符串
            except ValueError:
                print 'Invalid Value'
            print x
        if o=='-d':
            print 'use -d'
        if o=='-y':
            y=y+a