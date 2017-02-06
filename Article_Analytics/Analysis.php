<?php

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
			<a href='sources?url=".rawurlencode($a->getArticleURL())."'>".$analytics["numSources"]
		."</a></td>";
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
	$numSources = count($article->getArticleSources());
	$numWords = str_word_count($article->getArticleText());
	$sourcesPerMWords = $numSources/($numWords/1000);

	return ["numSources"=>$numSources, "numWords"=>$numWords, "sourcesPerMWords"=>$sourcesPerMWords];
}

/**
 * Generates average analytics for a given list of articles
 * Prints these analytics in h1.lead format
 * @param array|\Article $articles
 */
function overallAnalytics(array $articles){
	$numSources = 0;
	$numWords = 0;
	$numArticles = count($articles);
	$cumulativeGradeLevel= 0;

	foreach($articles as $a){
		/* @var $a \Article */
		$numSources += count($a->getArticleSources());
		$numWords += str_word_count($a->getArticleText());
		$cumulativeGradeLevel += $a->getGradeLevel();
	}

	// Ternary operations added to resolve divide by zero errors
	$sourcesPerArticle = $numArticles == 0 ? 0 : $numSources/$numArticles;
	$sourcesPerMWords = $numWords == 0 ? 0 : $numSources/($numWords/1000);
	$wordsPerArticle = $numArticles == 0 ? 0 : $numWords/$numArticles;
	$avgGradeLevel = $numArticles == 0 ? 0 : $cumulativeGradeLevel/$numArticles;


	if(count($articles) > 1){
		print "<h1 class='lead'>Number of Articles: ".number_format($numArticles)."</h1>";
		print "<h1 class='lead'>Sources per Article: ".number_format($sourcesPerArticle, 2)."</h1>";
		print "<h1 class='lead'>Sources per 1000 Words: ".number_format($sourcesPerMWords, 2)."</h1>";
		print "<h1 class='lead'>Average Word Count: ".number_format($wordsPerArticle, 0)."</h1>";
		print "<h1 class='lead'>Average Flesch-Kincaid Grade Level: ".number_format($avgGradeLevel, 1)."</h1>";
	}
	else if(count($articles) == 1){
		print "<h1 class='lead'>Number of Articles: ".number_format($numArticles)."</h1>";
		print "<h1 class='lead'>Sources: ".number_format($sourcesPerArticle)."</h1>";
		print "<h1 class='lead'>Sources per 1000 words: ".number_format($sourcesPerMWords, 2)."</h1>";
		print "<h1 class='lead'>Word count: ".number_format($wordsPerArticle)."</h1>";
		print "<h1 class='lead'>Flesch-Kincaid Grade Level: ".number_format($avgGradeLevel, 1)."</h1>";
	}
	else if(count($articles) ==  0){
		print "<h1 class='lead'>No Articles to Analyze</h1>";
	}
}