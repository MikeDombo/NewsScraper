<?php
require_once "Article.php";
require_once "Database.php";
require_once "Analysis.php";

$db = "../news.db";
try{
	$pdo = new PDO('sqlite:'.$db);
}
catch(PDOException $p){
	print 'Exception : '.$p->getMessage();
	return;
}

$dbo = new Database($pdo);

$url = rawurldecode($_GET["url"]);
$currentArticle = $dbo->getArticleByURL($url);

?>

<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	<meta http-equiv="X-UA-Compatible" content="IE=10; IE=9; IE=8; IE=7; IE=EDGE" />

	<title>NewsScraper Phase II: Analysis</title>

	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" crossorigin="anonymous">
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" crossorigin="anonymous"></script>

	<style>
		#maincontent{padding-top:1rem;}
		thead {
			background-color: #f7f7f7;
		}
		.card-columns .card{
			display: inline-block;
		}
		@media (min-width: 48em) {
			.card-columns {
				-webkit-column-count: 1;
				-moz-column-count: 1;
				column-count: 1;
			}
		}
		@media (min-width: 62em) {
			.card-columns {
				-webkit-column-count: 2;
				-moz-column-count: 2;
				column-count: 2;
			}
		}
	</style>
</head>
<body>
<?php include "makeNav.php";?>
<div class="container-fluid" id="maincontent">
	<div class="card-columns">
		<div class="card">
			<div class="card-block">
				<h1 class="card-title">Average Analytics</h1>
				<p class="card-text">
					<?php overallAnalytics($dbo->getArticles());?>
				</p>
			</div>
		</div>
		<div class="card">
			<div class="card-block">
				<?php
				print "<h1 class='card-title'>Analytics For <em><a target='_blank' href='".$currentArticle->getArticleURL
					()."'>".$currentArticle->getHeadline()."</em></a></h1>";
				?>
				<p class="card-text">
					<?php
					overallAnalytics([$currentArticle]);
					?>
				</p>
			</div>
		</div>
		<div class="card">
			<div class="card-block">
				<h2 class="card-title">Byline</h2>
				<p class="card-text"><?php print "<a href='author?author=".rawurlencode($currentArticle->getAuthor())."'>"
						.$currentArticle->getAuthor()."</a>"?></p>
			</div>
		</div>
		<div class="card">
			<div class="card-block">
				<h2 class="card-title">Sources</h2>
				<p class="card-text"><?php foreach($currentArticle->getArticleSources() as $s){print "<a href='$s'>$s</a><br/>";}?></p>
			</div>
		</div>
		<div class="card">
			<div class="card-block">
				<h3 class="card-title">Published By <?php print $currentArticle->getPublisher();?> on <?php print
						$currentArticle->getPublishDate()->format("Y/m/d");?></h3>
			</div>
		</div>
		<div class="card">
			<div class="card-block">
				<h3 class="card-title">Section(s) Published in</h3>
				<p class="card-text">
					<?php foreach($currentArticle->getArticleSection() as $i=>$s){
						print "<a href='section?section=".$s."'>";
						print ucwords($s);
						print "</a>";
						if($i != count($currentArticle->getArticleSection()) - 1){
							print "<-";
						}
					}?>
				</p>
			</div>
		</div>
		<div class="card">
			<div class="card-block">
				<h2 class="card-title">Full Text</h2>
				<p class="card-text"><?php print nl2br($currentArticle->getArticleText());?></p>
			</div>
		</div>
	</div>
</div>
</body>
</html>
