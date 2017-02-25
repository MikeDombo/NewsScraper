<?php if(isset($_GET["answer"])){
	try{
		$pdo = new PDO('mysql:host=localhost;dbname=newsscraper;charset=utf8', "root", "");
		$pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
	}
	catch(PDOException $p){
		print 'Exception : '.$p->getMessage();
		return;
	}
	if($_GET["answer"] > -1 && isset($_GET["ID"])){
		$q = $pdo->exec("UPDATE `Article-Fragments` SET `IsSource`=".$_GET["answer"]." WHERE `ID` =".$_GET["ID"]);
	}
	$q = $pdo->query("SELECT `ID`, `Fragment`, `IsSource` FROM `Article-Fragments` WHERE `IsSource` = -1 ORDER BY RAND() LIMIT 0,1");
	$new_fragment = $q->fetchAll()[0];
	$prediction = exec('python ../Auto_Classifier/app.py -p "'.$new_fragment["Fragment"].'"');
	echo json_encode(["ID"=>$new_fragment["ID"], "Fragment"=>$new_fragment["Fragment"], "Prediction"=>intval($prediction)]);
}
if(!isset($_GET["answer"])){
?>
<html>
<head>
	<title>Classify These Fragments</title>
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.1.0/jquery.min.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/tether/1.4.0/js/tether.min.js" integrity="sha384-DztdAPBWPRXSA/3eYEEUWrWCy7G5KFbe8fFjk5JAIxUYHKkDx6Qin1DkWx51bBrb" crossorigin="anonymous"></script>
	<link rel="stylesheet" href="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/css/bootstrap.min.css" crossorigin="anonymous">
	<script src="https://maxcdn.bootstrapcdn.com/bootstrap/4.0.0-alpha.6/js/bootstrap.min.js" crossorigin="anonymous"></script>
	<style>
	</style>
</head>
<body>
	<div class="container-fluid">
		<div class="row mt-5">
			<div class="offset-2 col-8 d-flex justify-content-center">
				<h4 id="fragment"></h4>
			</div>
			<div class="offset-2 col-8 d-flex justify-content-center mt-2">
				<h5><em id="prediction"></em></h5>
			</div>
		</div>
		<div class="row m-5">
			<div class="col-12 d-flex justify-content-center">
				<button class="btn btn-outline-success original-rep m-1"><u>O</u>riginal Reporting</button>
				<button class="btn btn-outline-primary primary-src m-1"><u>P</u>rimary Source</button>
				<button class="btn btn-outline-primary sec-src m-1"><u>S</u>econdary Source</button>
				<button class="btn btn-outline-primary quote-src m-1"><u>Q</u>uote</button>
				<button class="btn btn-outline-primary not-src m-1"><u>N</u>ot a Source</button>
				<button class="btn btn-outline-primary should-src m-1">Should <u>B</u>e Sourced</button>
				<button class="btn btn-outline-danger skip-src m-1">S<u>k</u>ip</button>
			</div>
		</div>
	</div>
	<script>
		function intToText(p){
			switch(p){
				case 0:
					return "Not a Source";
				case 1:
					return "Original Reporting";
				case 2:
					return "Primary Source";
				case 3:
					return "Secondary Source";
				case 4:
					return "Quote";
				case 5:
					return "Should Source"
			}
		}
		var ID = -1;
		$(document).ready(function(){
			$.get("?answer=-1", function(data){
				data = JSON.parse(data);
				$("#fragment").text(data["Fragment"]);
				console.log(intToText(data["Prediction"]));
				ID = data["ID"];
				$("#prediction").text(intToText(data["Prediction"]));
				}
			);
		});

		function saveResult(id, result){
			$.get("?answer="+result+"&ID="+id, function(data){
					data = JSON.parse(data);
					console.log(intToText(data["Prediction"]));
					$("#fragment").text(data["Fragment"]);
					ID = data["ID"];
					$("#prediction").text(intToText(data["Prediction"]));
				}
			);
		}

		$(".original-rep").on("click", function(){saveResult(ID, 1)});
		$(".primary-src").on("click", function(){saveResult(ID, 2)});
		$(".sec-src").on("click", function(){saveResult(ID, 3)});
		$(".quote-src").on("click", function(){saveResult(ID, 4)});
		$(".should-src").on("click", function(){saveResult(ID, 5)});
		$(".not-src").on("click", function(){saveResult(ID, 0)});
		$(".skip-src").on("click", function(){saveResult(ID, -1)});
		$(document).on('keyup', function(event){
			var k = event.key.toLowerCase();
			switch(k){
				case 'b':
					saveResult(ID, 5);
					break;
				case 'o':
					saveResult(ID, 1);
					break;
				case 'p':
					saveResult(ID, 2);
					break;
				case 's':
					saveResult(ID, 3);
					break;
				case 'q':
					saveResult(ID, 4);
					break;
				case 'n':
					saveResult(ID, 0);
					break;
				case 'k':
					saveResult(ID, -1);
					break;
			}
		});
	</script>
</body>
</html>
<?php }?>