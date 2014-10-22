<?php
/**
 * @desc	自定义linux服务调用  PHP端
 * @author	lijianwei	2013-7-23
 */

//常量
define("DS", DIRECTORY_SEPARATOR);
define("EXTPHPDIR", __DIR__. DS. 'extphp');
define("EXTPYTHONDIR", __DIR__. DS. 'extpython');
define("PHPVIEWDIR", __DIR__. DS. 'phpviews');

//获取参数
$init_params = array(
	'c' => 'index',
	'm' => 'index',
);
parse_str($_SERVER['QUERY_STRING'], $params);
$params = array_merge($init_params, $params);

if($params['c'] != 'index') {
	if(!file_exists(EXTPHPDIR. DS. $params['c']. '.php')) {
		$params['c'] = 'index';
	}
}

//验证
if($params['c'] == 'index') {
	$obj = new extLinuxOp;
} else {
	include(EXTPHPDIR. DS. $params['c']. '.php');
	$obj = new $params['c'];
}

if(!method_exists($obj, $params['m'])) {
	$params['m'] = $init_params['m'];
}
//加载配置
$config_arr = extLinuxOp::loadAllConfig();

call_user_func_array(array($obj, $params['m']), array_slice($params, 2));


class extLinuxOp
{
	public function __construct()
	{
		header('content-type:text/html;charset=utf-8');
		set_time_limit(0);
		date_default_timezone_set('Asia/Shanghai');
		die('123');
	}
	
	//显示所有扩展功能
	public function index()
	{
		$data =	$this->getAllPluginInfo();
		include('phpviews/showallfunc.php');
	}
	//添加插件
	public function addPlugin()
	{
			
		
	}
	//启用插件
	public function enablePlugin()
	{
		
	}
	//停用插件
	public function disablePlugin()
	{
		
	}
	public static function loadAllConfig()
	{
		return parse_ini_file(EXTPHPDIR. DS. 'config.ini', TRUE);
	}
	
	//获取所有插件信息
	protected function getAllPluginInfo()
	{
		global $config_arr;
		return array_slice($config_arr, 1);
	}
	//组装url
	protected function createUrl(array $query_arr = array())
	{
		global $init_params;
		
		$query_arr = array_merge($init_params, $query_arr);
		
		return 'index.php?'. http_build_query($query_arr);
	}
}

class renderHelper
{
	public static function tableTpl(array $data = array())
	{
		ob_start();
		include(PHPVIEWDIR. DS. 'table.php');
		$contents = ob_get_contents();
		ob_end_clean();
		return $contents;
	}
}


