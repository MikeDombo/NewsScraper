<?php
$db = "../news.db";
try{
	$pdo = new PDO('sqlite:'.$db);
}
catch(PDOException $p){
	print 'Exception : '.$p->getMessage();
}

print "HI"
?>
