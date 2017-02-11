<?php

$qualityDefinition = [-1=> "no links", 0=> "link", 1=> "newspaper source", 2=> "assumed primary source"];

/**
 * Prints into a table the article headline (linked to URL) and statistics
 * @param array|\Article $articles
 */
function analyticsByHeadline(array $articles){
	foreach($articles as $a){
		/* @var $a \Article */
		$analytics = articleAnalytics($a);
		print "<tr>";
		print "<td><a target='_blank' href='".$a->getArticleURL()."'>".$a->getHeadline()."</a>";
		print "<br/><a href='author?author=".rawurlencode($a->getAuthor())."'>By: ".$a->getAuthor()."</td>";
		print "<td onclick='return navigate(event, \"sources?url=".rawurlencode($a->getArticleURL())."\");'>
			<a href='sources?url=".rawurlencode($a->getArticleURL())."'>".$analytics["numLinks"]
		."</a></td>";
		print "<td>".number_format($analytics["linksPerMWords"], 2)."</td>";
		print "<td>".number_format($analytics["averageLinkQuality"], 2)."</td>";
		print "<td>".number_format($analytics["numSources"])."</td>";
		print "<td>".number_format($analytics["sourcesPerMWords"], 2)."</td>";
		print "<td>".number_format($analytics["numWords"])."</td>";
		print "</tr>";
	}
}

/**
 * Returns statistics from a given article including number of sources, number of words, and sources
 * per 1000 words.
 * @param \Article $article article you want statistics about
 * @return array
 */
function articleAnalytics(\Article $article): array {
	$numLinks = 0;
	$cumulativeLinkQuality = 0;
	$numWords = str_word_count($article->getArticleText());
	$numSources = count($article->getTextSources());
	$sourcesPerMWords = $numSources/($numWords/1000);
	$linksPerMWords = $numLinks/($numWords/1000);

	foreach($article->getArticleSources() as $t){
		$numLinks += 1;
		$cumulativeLinkQuality += $t["Quality"];
	}

	$linkQualityAverage = $numLinks == 0 ? -1 : $cumulativeLinkQuality/$numLinks;

	return ["numLinks"=>$numLinks, "numWords"=>$numWords, "linksPerMWords"=>$linksPerMWords,
			"numSources"=>$numSources, "sourcesPerMWords"=>$sourcesPerMWords,
			"averageLinkQuality"=>$linkQualityAverage];
}

/**
 * Generates average analytics for a given list of articles
 * Prints these analytics in h1.lead format
 * @param array|\Article $articles
 */
function overallAnalytics(array $articles){
	$numLinks = 0;
	$numSources = 0;
	$numWords = 0;
	$numArticles = count($articles);
	$cumulativeGradeLevel= 0;
	$cumulativeLinkQuality = 0;

	foreach($articles as $a){
		/* @var $a \Article */
		$numSources += count($a->getTextSources());
		$numWords += str_word_count($a->getArticleText());
		$cumulativeGradeLevel += $a->getGradeLevel();
		foreach($a->getArticleSources() as $t){
			$numLinks += 1;
			$cumulativeLinkQuality += $t["Quality"];
		}
	}

	// Ternary operations added to resolve divide by zero errors
	$linksPerArticle = $numArticles == 0 ? 0 : $numLinks/$numArticles;
	$linksPerMWords = $numWords == 0 ? 0 : $numLinks/($numWords/1000);
	$sourcesPerArticle = $numArticles == 0 ? 0 : $numSources/$numArticles;
	$sourcesPerMWords = $numWords == 0 ? 0 : $numSources/($numWords/1000);
	$wordsPerArticle = $numArticles == 0 ? 0 : $numWords/$numArticles;
	$avgGradeLevel = $numArticles == 0 ? 0 : $cumulativeGradeLevel/$numArticles;
	$linkQualityAverage = $numLinks == 0 ? -1 : $cumulativeLinkQuality/$numLinks;

	global $qualityDefinition;
	$quality = $qualityDefinition[intval($linkQualityAverage)];


	if(count($articles) > 1){
		print "<h1 class='lead'>Number of Articles: ".number_format($numArticles)."</h1>";
		print "<h1 class='lead'>Links per Article: ".number_format($linksPerArticle, 2)."</h1>";
		print "<h1 class='lead'>Links per 1000 Words: ".number_format($linksPerMWords, 2)."</h1>";
		print "<h1 class='lead'>Link Quality: ".number_format($linkQualityAverage, 2)." ($quality)</h1>";
		print "<h1 class='lead'>Sources in Text per Article: ".number_format($sourcesPerArticle, 2)."</h1>";
		print "<h1 class='lead'>Sources in Text per 1000 Words: ".number_format($sourcesPerMWords, 2)."</h1>";
		print "<h1 class='lead'>Average Word Count: ".number_format($wordsPerArticle, 0)."</h1>";
		print "<h1 class='lead'>Average Flesch-Kincaid Grade Level: ".number_format($avgGradeLevel, 1)."</h1>";
	}
	else if(count($articles) == 1){
		print "<h1 class='lead'>Number of Articles: ".number_format($numArticles)."</h1>";
		print "<h1 class='lead'>Links: ".number_format($linksPerArticle)."</h1>";
		print "<h1 class='lead'>Links per 1000 words: ".number_format($linksPerMWords, 2)."</h1>";
		print "<h1 class='lead'>Link Quality: ".number_format($linkQualityAverage, 2)." ($quality)</h1>";
		print "<h1 class='lead'>Sources in Text per Article: ".number_format($sourcesPerArticle)."</h1>";
		print "<h1 class='lead'>Sources in Text per 1000 Words: ".number_format($sourcesPerMWords)."</h1>";
		print "<h1 class='lead'>Word count: ".number_format($wordsPerArticle)."</h1>";
		print "<h1 class='lead'>Flesch-Kincaid Grade Level: ".number_format($avgGradeLevel, 1)."</h1>";
	}
	else if(count($articles) ==  0){
		print "<h1 class='lead'>No Articles to Analyze</h1>";
	}
}