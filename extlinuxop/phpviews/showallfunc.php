<table border="1" cellspacing="3" cellpadding="3" width="500" align="center">
<tr><th>名称</th><th>操作</th></tr>
<?php foreach($data as $k => $v):?>
<tr><td><?php echo $v['description'];?></td><td><a href="<?php echo $this->createUrl(array('c' => basename($v['php_file'], '.php')));?>">显示</a></td></tr>
<?php endforeach;?>
</table>