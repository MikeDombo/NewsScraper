<?php

/**
 * Prints into a table the article headline (linked to URL) and statistics
 * @param array|\Article $articles
 */
function analyticsByHeadline(array $articles){
	foreach($articles as $a){
		$analytics = articleAnalytics($a);
		print "<tr>";
		print "<td><a target='_blank' href='".$a->getArticleURL()."'>".$a->getHeadline()."</a></td>";
		print "<td>".$analytics["numSources"]."</td>";
		print "<td>".number_format($analytics["sourcesPerMWords"], 2)."</td>";
		print "<td>".$analytics["numWords"]."</td>";
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
		$numArticles++;
		$numSources += count(array_unique($a->getArticleSources()));
		$numWords += str_word_count($a->getArticleText());
	}

	print "<h1 class='lead'>Sources per article: ".number_format($numSources/$numArticles, 2)."</h1>";
	print "<h1 class='lead'>Sources per 1000 words: ".number_format($numSources/($numWords/1000), 2)."</h1>";
	print "<h1 class='lead'>Average word count: ".number_format($numWords/$numArticles, 0)."</h1>";
}