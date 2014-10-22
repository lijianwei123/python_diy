<!DOCTYPE html>
<html>
  <head>
  <meta http-equiv="content-type" content="text/html; charset=utf-8"/>
  <title>添加分词</title>
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
	
	$content = trim($_POST['content']);
	if(empty($content)) {
		echo "请输入内容";
	}else{
		try{
			//连接超时
			$sock = fsockopen("unix:///tmp/addWord", NULL, $errno, $errstr, 10);
			
			if(!$sock) {
				echo "无法连接服务器!";
			}else {
				//读写超时
				//stream_set_timeout($sock, 10);
				
				$data = array(
					"command" => "addWord",
					"wordContent" => base64_encode($content)
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
  <form method="post" action="addWord.php">
	<textarea name="content" id="content" rows="10" cols="30">新百	1
x:1
建湖	1
x:1</textarea>

	<input type="button" value="提交" onclick="this.form.submit();this.disabled = true;">
	<a href="new.txt" target="_blank">查看已有词库</a>
  </form>
  <span style="color:red">建议在前台业务不太繁忙时执行此脚本，页面执行时请不要关闭！</span>
  </body>
  </html>
