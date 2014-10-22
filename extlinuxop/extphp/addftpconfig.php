<?php
/**
 * @desc	添加ftp配置
 * @author	lijianwei	2013-7-23
 */

require('base.php');

class addftpconfig extends base  
{
	public function __construct()
	{
	}
	
	public function index()
	{
		$this->listAll();
	}
	
	//显示所有
	public function listAll()
	{
		$pathinfo = __CLASS__. '/'. __METHOD__;
		$params = array();
		$this->sendCommand($this->encodeCommand($pathinfo, $params));
	}
	//添加
	public function addItem()
	{
		$pathinfo = __CLASS__. '/'. __METHOD__;
		$params = array();
		//参数
		$params['ftp_dir'] = $this->safeData($_POST['ftp_dir']);
		$params['ftp_user'] = $this->safeData($_POST['ftp_user']);
		$params['ftp_pwd'] = $this->safeData($_POST['ftp_pwd']);
		//验证ftp_dir
		global $config_arr;
		$ftp_basedir = $config_arr[__CLASS__]['ftp_basedir'];
		if(false === strpos($params['ftp_dir'], $ftp_basedir)) {
			$this->showMsg('9999', '目录应该设置在'. $ftp_basedir. '目录下');
		}
	
		
		$this->sendCommand($this->encodeCommand($pathinfo, $params));
	}
	//删除
	public function delItem()
	{
		
	}
	//修改
	public function editItem()
	{
		
	}
	//保存
	public function saveItem()
	{
	}
	
	
	
	
}