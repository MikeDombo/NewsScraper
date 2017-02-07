<?php
require_once "Database.php";

try{
	$pdo = new PDO('mysql:host=localhost;dbname=newsscraper;charset=utf8', "root", "");
	$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
}
catch(PDOException $p){
	print 'Exception : '.$p->getMessage();
	return;
}
$dbo = new Database($pdo);