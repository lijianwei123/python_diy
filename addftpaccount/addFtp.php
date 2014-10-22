<!DOCTYPE html>
<html>
  <head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
  <title>添加ftp账号</title>
  </head>
  <body>  
<?php
set_time_limit(0);

header("content-type:text/html;charset=utf-8");
$user = "lijianwei";
$pwd = "lijianwei";

if(!isset($_SERVER['PHP_AUTH_USER'])){
	header("WWW-Authenticate: Basic realm='access'");
	header("HTTP/1.0 401 unauthorized");
	echo  "你点击了取消按钮!";
	exit;
}else{
	if(!($_SERVER['PHP_AUTH_PW'] == $pwd) || !($_SERVER['PHP_AUTH_USER'] == $user)){
		header("WWW-Authenticate: Basic realm='access'");
		header("HTTP/1.0 401 unauthorized");
		echo "帐号密码错误!";
		exit;
	}
}

if($_SERVER['REQUEST_METHOD'] == 'POST') {
	
	$ftp_path = trim($_POST['ftp_path']);
	$ftp_user = trim($_POST['ftp_user']);
	$ftp_pwd  = trim($_POST['ftp_pwd']);
	
	
	
	if(empty($ftp_path) || empty($ftp_user) || empty($ftp_pwd)) {
		echo "有些东西你忘记填写了";
	}else{
		try{
			//连接超时
			$sock = fsockopen("unix:///tmp/addFtp", NULL, $errno, $errstr, 10);
			
			if(!$sock) {
				echo "无法连接服务器!";
			}else {
				//读写超时
				//stream_set_timeout($sock, 10);
				
				$data = array(
					"command" => "addFtp",
					"ftp_path" => $ftp_path,
				    "ftp_user" => $ftp_user,
				    "ftp_pwd"  => $ftp_pwd,
				);
				
				$json_data = json_encode($data);
				
				fwrite($sock, $json_data);
				
				echo $ret_str = fread($sock, 4096);
				
				fclose($sock);	
				
			}
		}catch(Exception $e){
			echo "出现异常：". $e->getMessage();
		}
		
	}
}
?>
  <form method="post" action="addFtp.php">
	ftp路径:<input type="input" name="ftp_path" value=""/>
	ftp账号:<input type="input" name="ftp_user" value=""/>
	ftp密码:<input type="input" name="ftp_pwd"  value=""/>
	<input type="button" value="提交" onclick="this.form.submit();this.disabled = true;">
  </form>
  <span style="color:red">建议在前台业务不太繁忙时执行此脚本，页面执行时请不要关闭！</span>
  </body>
  </html>
