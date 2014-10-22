#encoding: utf-8
'''自动添加ftp账号.

write by lijianwei 2013-10-23
'''
import sys, signal, socket, os, select, stat
import json
import traceback
import time
import subprocess

################################

ftp_user_path = "/etc/vsftpd/vir_user"
ftp_conf_path = "/etc/vsftpd/vconf";

################################

#关闭server socket
def handler(signum = None, frame = None):
    global sock
    if sock:
        sock.close()
    sys.exit("quit")

     
#信号处理
signal.signal(signal.SIGTERM, handler)
signal.signal(signal.SIGINT, handler)

#本地 unix socket
sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM, 0)
sock_path = "/tmp/addFtp"
if os.path.exists(sock_path):
    os.unlink(sock_path)
sock.bind(sock_path)
sock.listen(5)

#修改所有者为www
id_p = subprocess.Popen('id -u www', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
www_uid = int(id_p.stdout.readline())
id_p = subprocess.Popen('id -g www', stdin=subprocess.PIPE, stdout=subprocess.PIPE, shell=True)
www_gid = int(id_p.stdout.readline())
os.chown(sock_path, www_uid, www_gid)


#具体处理
while True:
    try:
            con, addr = sock.accept()
           
            recvData = con.recv(1024 * 100)
            if recvData.find('}'):
                data = json.loads(recvData)
             
                if ('command in data') and (data['command'] == 'addFtp'):
                    ftp_path = data['ftp_path'];
                    ftp_user = data['ftp_user'];
                    ftp_pwd = data['ftp_pwd'];
                
                    if not os.path.exists(ftp_path):
                       con.sendall("ftp path " + ftp_path + "don't exist!");
                       con.close()
                       continue
                    else:
                        os.system("echo " + ftp_user + "\n >> " + ftp_user_path)
                        os.system("echo " + ftp_pwd + " >> " + ftp_user_path)
                        os.system("touch " + ftp_conf_path + os.sep + ftp_user);
                        list = [ftp_path]
                        ftp_user_config_str = "local_root={0}\
anonymous_enable=NO\
write_enable=YES\
local_umask=022\
anon_upload_enable=NO\
anon_mkdir_write_enable=NO\
idle_session_timeout=600\
data_connection_timeout=120\
max_clients=10\
max_per_ip=5\
local_max_rate=50000".format(*list)
                        os.system("echo " + ftp_user_config_str + " >> " + ftp_conf_path + os.sep + ftp_user)
                        os.system("service vsftpd db-load && service vsftpd restart")
                        con.sendall("success")
        
    except Exception, e:
        print traceback.format_stack();
        if con:
            con.sendall("fail")
            if con:
                con.close()
handler()
