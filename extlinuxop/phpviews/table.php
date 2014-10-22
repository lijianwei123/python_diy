<table border="1" cellspacing="3" cellpadding="3" width="500" align="center">
<tr><th>名称</th><th>操作</th></tr>
<?php foreach($data as $k => $v):?>
<tr><td><?php echo $v['description'];?></td><td>操作</td></tr>
<?php endforeach;?>
</table>