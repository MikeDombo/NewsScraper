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
		<div class="container-fluid" id="maincontent">
			<h1 class="display-3 d-flex justify-content-center">NewsScraper Analysis</h1>
			<div class="col-lg-12">
				<?php
					print "<h1>Average Analytics:</h1>";
					overallAnalytics($dbo->getArticles());
					print "<hr/><h1>Analytics By Publisher:</h1>";

					foreach($dbo->listAllPublishers() as $p){
						print "<h3>".$p."</h3>";
						$p = $dbo->getArticlesByPublisher($p);
						overallAnalytics($p);
				?>
				<div>
				<button class="btn btn-outline-primary individualArticle">Individual Article Analytics</button>
				<div class="collapse mt-2">
					<table class="table table-responsive analytics-table">
						<thead>
							<tr>
								<th>Headline</th>
								<th>Sources in Article</th>
								<th>Sources per 1000 Words</th>
								<th>Word Count</th>
							</tr>
						</thead>
						<tbody>
						<?php
							analyticsByHeadline($p);
						?>
						</tbody>
					</table>
				</div>
				</div>
				<?php
						print "<hr/>";
					}
				?>
				<script>
					$("table.analytics-table").floatThead({
						responsiveContainer: function($table){
								return $table.closest('.table-responsive');
						},
						position:'fixed'
					});
				</script>
			</div>
		</div>
		<script>
			$(".individualArticle").on('click', function(){
				$(this).parent().find(".collapse").toggle();
			});
		</script>
	</body>
</html>
