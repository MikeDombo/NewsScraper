<?php
require_once "Article.php";
require_once "Analysis.php";

require "DBConnection.php";

$singleAuthor = false;
if(isset($_GET["author"])){
	$authors = [rawurldecode($_GET["author"])];
	$singleAuthor = true;
}
else{
	$authors = $dbo->listAllAuthors();
}
?>

<html>
<head>
	<meta charset="utf-8">
	<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no">
	<meta http-equiv="X-UA-Compatible" content="IE=10; IE=9; IE=8; IE=7; IE=EDGE" />

	<title>NewsScraper Phase II: Analysis</title>

	<style>
		#maincontent{padding-top:1rem;}
		thead {
			background-color: #f7f7f7;
		}
	</style>

	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" crossorigin="anonymous">
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" crossorigin="anonymous"></script>
	<script src="js/jquery.floatThead.min.js"></script>
</head>
<body>
<?php include "makeNav.php";?>
<div class="container-fluid" id="maincontent">
	<div class="col-lg-12 pb-5">
		<?php
		foreach($authors as $currentAuthor){
			print "<hr/><h2>Analytics For Author <a href='author?author=".rawurlencode($currentAuthor)."'>"
				.htmlspecialchars($currentAuthor)."</a>:</h2>";
			$p = $dbo->getArticlesByAuthor($currentAuthor);
			overallAnalytics($p);
			?>
			<div>
				<?php if(!$singleAuthor){
					print "<button class=\"btn btn-outline-primary individualArticle\">Individual Article Analytics</button>
				<div class=\"collapse mt-2\">";
				}?>
				<?php require_once "tableTemplate.php"; makeTable($p);?>
				<?php if(!$singleAuthor){
					print "</div>";
				}?>
			</div>
			<?php
			}
			?>
	</div>
	<script>
		$("table.analytics-table").floatThead({
			responsiveContainer: function($table){
				return $table.closest('.table-responsive');
			},
			position:'absolute'
		});
		$(".individualArticle").on('click', function(){
			$(this).parent().find(".collapse").toggle();
		});
	</script>
</div>
</body>
</html>
