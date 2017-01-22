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
		print "<br/><a target='_self' href='author?author=".rawurlencode($a->getAuthor())."'>By: ".$a->getAuthor()."</td>";
		print "<td><a target='_self' href='sources?url=".rawurlencode($a->getArticleURL())."'>".$analytics["numSources"]
		."</a></td>";
		print "<td>".number_format($analytics["sourcesPerMWords"], 2)."</td>";
		print "<td>".number_format($analytics["numWords"])."</td>";
		print "</tr>";
	}
}

function sectionAnalytics($section, $articles){

}

/**
 * Returns statistics from a given article including number of sources, number of words, and sources
 * per 1000 words.
 * @param \Article $article article you want statistics about
 * @return array
 */
function articleAnalytics(\Article $article): array {
	$numSources = count(array_unique($article->getArticleSources()));
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

	foreach($articles as $a){
		/* @var $a \Article */
		$numSources += count(array_unique($a->getArticleSources()));
		$numWords += str_word_count($a->getArticleText());
	}

	// Ternary operations added to resolve divide by zero errors
	$sourcesPerArticle = $numArticles == 0 ? 0 : $numSources/$numArticles;
	$sourcesPerMWords = $numWords == 0 ? 0 : $numSources/($numWords/1000);
	$wordsPerArticle = $numArticles == 0 ? 0 : $numWords/$numArticles;


	print "<h1 class='lead'>Sources per article: ".number_format($sourcesPerArticle, 2)."</h1>";
	print "<h1 class='lead'>Sources per 1000 words: ".number_format($sourcesPerMWords, 2)."</h1>";
	print "<h1 class='lead'>Average word count: ".number_format($wordsPerArticle, 0)."</h1>";
}