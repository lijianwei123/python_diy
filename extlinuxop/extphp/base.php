<?php
/**
 * @desc	接口
 * @author	lijianwei	2013-7-23
 */
abstract  class  base
{
	//code map
	const codeMap = array(
		'0000' => 'success',
		'9999' => 'error',
	);
	//显示所有
	abstract public function listAll();
	//添加
	abstract public function addItem();
	//删除
	abstract public function delItem();
	//修改
	abstract public function editItem();
	//保存
	abstract public function saveItem();
	
	//调用python
	public function sendCommand($command_str = '')
	{
		$base_config = $this->getBaseConfig();
		extract($base_config, EXTR_OVERWRITE);
		$sock = fsockopen(python_ip, $python_port, $errno, $errstr, 5); //5s 连接超时
		if(!$sock) {
			die('sock occur error: '. $errno. ' '. $errstr);
		}
		fwrite($sock, $command_str);
		$resp_str = fread($sock, 4096); //4KB
		fclose($sock);
		
		$this->commandRespCallBack($resp_str);
	}
	
	//json_encode command
	protected function encodeCommand($pathinfo = '', array $params = array())
	{
		return json_encode(array('pathinfo' => $pathinfo, 'params' => $params));
	}
	//json_decode command
	protected function decodeCommand($command_str = '')
	{
		return json_decode($command_str, TRUE);
	}
		
	//获取基础配置
	protected function getBaseConfig()
	{
		global $config_arr;
		return array_slice($config_arr, 0, 1);
	}
	//命令回调
	protected function commandRespCallBack($resp_str = '')
	{
		$resp_arr = $this->decodeCommand($resp_str);
		if(!empty($resp_arr['code'])) {
			$this->showMsg($resp_arr['code'], $resp_arr['msg']);
		}
	}
	protected function showMsg($code, $msg)
	{
		$codemsg = '';
		if(in_array($code, array_keys(self::codeMap))) {
			$codemsg = self::codeMap[$code]; 
		}
		$echo_str = "执行结果: {$codemsg}  {$msg} <br><a href='javascript:history.go(-1);'>点击返回</a>";
		exit;
	}
	protected function safeData($str = '')
	{

		$safe_str = $str;
		if(!get_magic_quotes_gpc()) {
			$safe_str = addslashes($safe_str);
		}

		return $safe_str;
	}
}
