<?php

/**
 * Read request url path and split it into subdirectories to redirect the request
 */
$url = explode("/", parse_url($_SERVER['REQUEST_URI'])["path"]);
foreach($url as $k=>$u){
	if($u == "author"){
		include "authorAnalytics.php";
		exit;
	}
	else if($u == "publisher"){
		include "index.php";
		exit;
	}
	else if($u == "day"){
		include "dailyAnalytics.php";
		exit;
	}
	else if($u == "sources" && isset($_GET["url"])){
		include "sourcesListing.php";
		exit;
	}
	else if($u == "section"){
		include "sectionAnalytics.php";
		exit;
	}
}
make404();

/**
 * Send a 404 error and show "Page not found"
 */
function make404(){
	header("HTTP/1.0 404 Not Found");
	echo "404: Page Not Found!";
	exit(0);
}