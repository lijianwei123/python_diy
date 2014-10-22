#encoding: utf-8
'''自动添加分词.

write by lijianwei 2013-5-24
'''
import sys, signal, socket, os, select, stat
import json
import traceback
import time
import subprocess

################################

oldWordFile = 'efon.txt'
newWordFile = 'new.txt'

#分词编译命令
wordCompileCommand = "/usr/local/mmseg3/bin/mmseg"

#文件锁
lock_file = "addWord.lock"

################################

#关闭server socket
def handler(signum = None, frame = None):
	global sock
	if sock:
		sock.close()
	sys.exit("quit")

#去重	
def delDuplicate():
	global oldWordFile, newWordFile
	f = open(oldWordFile)
	f2 = open(newWordFile,"w")
	all_line = set()
	for line in f:
	        if line != '' and line.find('\t') > 3:
	                all_line.add(line)
	for line in all_line:
	        f2.write(line)
	        f2.write('x:1')
	        f2.write('\n')
	 

#信号处理
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)
#signal.signal(signal.SIGCHLD, signal.SIG_IGN)

#本地 unix socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
sock_path = "/tmp/addWord"
if os.path.exists(sock_path):
    os.unlink(sock_path)
sock.bind(sock_path)
sock.listen(5)

#修改所有者为nobody
id_p = subprocess.Popen('id -u www', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
id_p.wait()
nobody_uid = int(id_p.stdout.readline())
id_p = subprocess.Popen('id -g www', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
id_p.wait()
nobody_gid = int(id_p.stdout.readline())
os.chown(sock_path, nobody_uid, nobody_gid)

#修改权限 777
#os.chmod(sock_path, stat.S_IRWXU|stat.S_IRWXG|stat.S_IRWXO);  

#具体处理
while True:
	try:
   		con,addr = sock.accept()
   		
   		if os.path.exists(lock_file):
   			recvData = con.recv(1)
   		 	con.sendall("addWord is already running!")
   		 	con.close()
   		 	continue
   		else:
   			os.system('touch ' + lock_file)
   		

	 	recvData = con.recv(1024*100)
	 	
	 	if recvData.find('}'):
	 		data = json.loads(recvData)
	 		
		  	if ('command' in data) and (data['command'] == 'addWord'):
				wordContent = data['wordContent'].decode("base64")
				os.system("echo '" + wordContent + "' >> " +  oldWordFile)
				delDuplicate()
					
				#生成字典
				
				#删除之前的new.txt.uni
				dict_uni = newWordFile + ".uni"
				if os.path.exists(dict_uni):
					os.unlink(dict_uni) 
				os.system(wordCompileCommand + " -u "\
						+ newWordFile);
						
				#备份之前uni.lib
				os.system("cd " + os.path.dirname(os.path.dirname(wordCompileCommand)) + os.sep + "etc;mv -f uni.lib uni.lib.bak")
				
				#拷贝到etc中
				os.system("cp -f " + dict_uni + " " + os.path.dirname(os.path.dirname(wordCompileCommand)) + os.sep + "etc" + os.sep + "uni.lib")
				
				#time.sleep(5)
				
				# 重建索引
				os.system("/usr/local/coreseek/bin/indexer -c /usr/local/coreseek/etc/csft_mysql_job_search.conf --all --rotate >/dev/null")
				# 重启服务
				#os.system("/usr/local/coreseek/bin/searchd -c /usr/local/coreseek/etc/csft_mysql_job_search.conf --stop >/dev/null")
				#time.sleep(2)
				#os.system("/usr/local/coreseek/bin/searchd -c /usr/local/coreseek/etc/csft_mysql_job_search.conf >/dev/null")
				
				con.sendall("success")
			elif ('command' in data) and (data['command'] == 'addLmsDiyHost'):
				diy_host = data['diy_host']
				
				x_lms_nginx_conf = "/usr/local/nginx/conf/virtual_host/x.lms.9first.com.conf"
				command = "/usr/local/nginx/sbin/nginx -s reload >/dev/null"
				
				# 查询已有的域名字符串
				grab_diy_host_command = "/bin/awk -F '^' '/\(\$host/{print $2}' " + x_lms_nginx_conf + " | /bin/awk -F ')' '{print $1}' | /bin/awk '{print substr($0, 2)}'"
				# 添加
				add_diy_host = "/bin/sed -i 's/\^(/&" + diy_host + "|/' " + x_lms_nginx_conf + " 2>&1"
				
				# 先读取已有的host
				diy_hosts_p = subprocess.Popen(grab_diy_host_command, stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
				diy_hosts_p.wait()
				diy_hosts_p = diy_hosts_p.stdout.readline()
				diy_hosts_list = diy_hosts_p.split('|')
				
				# 已经添加过的
				if diy_host in diy_hosts_list:
					con.sendall('exist')
				else:
					# 添加
					if os.system(add_diy_host) == 0 :
						con.sendall("success")
						os.system(command)
					else:
						con.sendall("fail")
				
		
		os.system("rm -rf " + lock_file)
   		con.close()
   	except Exception,e:
   		print traceback.format_stack();
   		#print sys.exc_info()[1]
   		if con:
   			con.sendall("fail:" + sys.exc_info()[1])
   		os.system("rm -rf " + lock_file)
   		if con:
   		 	con.close()
   		#handler()

def readFileContent(filename = None):
	fp = open(filename)
	cotent = fp.read()
	fp.close()
	return content

handler()   		

		





