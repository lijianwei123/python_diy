'''
Created on 2013-4-12

@author: Administrator
'''

import subprocess
cmd = "cmd.exe"
begin = 190
end = 200
while begin < end:
    p = subprocess.Popen(cmd, shell = True, stdout = subprocess.PIPE, 
                         stdin = subprocess.PIPE, 
                         stderr = subprocess.PIPE)
    p.stdin.write("ping 168.192.122." + str(begin) + "\n")
    p.stdin.close()
    p.wait()
    print("execution result: %s" %p.stdout.read())
    begin = begin + 1
    
