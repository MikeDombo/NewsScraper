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
		print "<td>".number_format($analytics["originalReportingPercent"], 2)."%</td>";
		print "<td onclick='return navigate(event, \"sources?url=".rawurlencode($a->getArticleURL())."\");'>
			<a href='sources?url=".rawurlencode($a->getArticleURL())."'>".$analytics["numLinks"]
		."</a></td>";
		print "<td>".number_format($analytics["linksPerMWords"], 2)."</td>";
		print "<td>".number_format($analytics["averageLinkQuality"], 2)."</td>";
		print "<td>".number_format($analytics["numSources"])."</td>";
		print "<td>".number_format($analytics["sourcesPerMWords"], 2)."</td>";
		print "<td>".number_format($analytics["numWords"])."</td>";
		print "<td>".number_format($analytics["numSentences"])."</td>";
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
	$numSentences = $article->getNumSentences();
	$unsourced = $article->getNumNotSourced();
	$originalReporting = $article->getNumOriginalReporting();
	$primarySource = $article->getNumPrimarySource();
	$secondarySource = $article->getNumSecondarySource();
	$quote = $article->getNumQuote();
	$needsSource = $article->getNumNeedsSource();

	foreach($article->getArticleSources() as $t){
		$numLinks += 1;
		$cumulativeLinkQuality += $t["Quality"];
	}

	$linksPerMWords = $numLinks/($numWords/1000);
	$linkQualityAverage = $numLinks == 0 ? -1 : $cumulativeLinkQuality/$numLinks;
	$avgUnsourced = $numSentences == 0 ? 0 : $unsourced/$numSentences;
	$avgOriginalReporting = $numSentences == 0 ? 0 : $originalReporting/$numSentences;
	$avgPrimarySource = $numSentences == 0 ? 0 : $primarySource/$numSentences;
	$avgSecondarySource = $numSentences == 0 ? 0 : $secondarySource/$numSentences;
	$avgQuote = $numSentences == 0 ? 0 : $quote/$numSentences;
	$avgNeedsSource = $numSentences == 0 ? 0 : $needsSource/$numSentences;

	return ["numLinks"=>$numLinks, "numWords"=>$numWords, "linksPerMWords"=>$linksPerMWords,
		"numSources"=>$numSources, "sourcesPerMWords"=>$sourcesPerMWords, "numSentences"=>$numSentences,
		"averageLinkQuality"=>$linkQualityAverage, "unsource"=>$unsourced, "originalReporting"=>$originalReporting,
		"primarySource"=>$primarySource, "secondarySource"=>$secondarySource, "quote"=>$quote,
		"needsSource"=>$needsSource, "originalReportingPercent"=>$avgOriginalReporting*100,
		"unsourcedPercent"=>$avgUnsourced*100, "primarySourcePercent"=>$avgPrimarySource*100,
		"secondarySourcePercent"=>$avgSecondarySource*100, "quotePercent"=>$avgQuote*100,
		"needsSourcePercent"=>$avgNeedsSource*100
	];
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

	$cumulativeUnsourced = 0;
	$cumulativeOriginalReporting = 0;
	$cumulativePrimarySource = 0;
	$cumulativeSecondarySource = 0;
	$cumulativeQuote = 0;
	$cumulativeNeedsSource = 0;
	$cumulativeSentenceCount = 0;

	foreach($articles as $a){
		/* @var $a \Article */
		$numSources += count($a->getTextSources());
		$numWords += str_word_count($a->getArticleText());
		$cumulativeGradeLevel += $a->getGradeLevel();
		foreach($a->getArticleSources() as $t){
			$numLinks += 1;
			$cumulativeLinkQuality += $t["Quality"];
		}

		$cumulativeSentenceCount += $a->getNumSentences();
		$cumulativeUnsourced += $a->getNumNotSourced();
		$cumulativeOriginalReporting += $a->getNumOriginalReporting();
		$cumulativePrimarySource += $a->getNumPrimarySource();
		$cumulativeSecondarySource += $a->getNumSecondarySource();
		$cumulativeQuote += $a->getNumQuote();
		$cumulativeNeedsSource += $a->getNumNeedsSource();
	}

	// Ternary operations added to resolve divide by zero errors
	$linksPerArticle = $numArticles == 0 ? 0 : $numLinks/$numArticles;
	$linksPerMWords = $numWords == 0 ? 0 : $numLinks/($numWords/1000);
	$sourcesPerArticle = $numArticles == 0 ? 0 : $numSources/$numArticles;
	$sourcesPerMWords = $numWords == 0 ? 0 : $numSources/($numWords/1000);
	$wordsPerArticle = $numArticles == 0 ? 0 : $numWords/$numArticles;
	$sentencesPerArticle = $numArticles == 0 ? 0 : $cumulativeSentenceCount/$numArticles;
	$avgGradeLevel = $numArticles == 0 ? 0 : $cumulativeGradeLevel/$numArticles;
	$avgUnsourced = $cumulativeSentenceCount == 0 ? 0 : $cumulativeUnsourced/$cumulativeSentenceCount;
	$avgOriginalReporting = $cumulativeSentenceCount == 0 ? 0 : $cumulativeOriginalReporting/$cumulativeSentenceCount;
	$avgPrimarySource = $cumulativeSentenceCount == 0 ? 0 : $cumulativePrimarySource/$cumulativeSentenceCount;
	$avgSecondarySource = $cumulativeSentenceCount == 0 ? 0 : $cumulativeSecondarySource/$cumulativeSentenceCount;
	$avgQuote = $cumulativeSentenceCount == 0 ? 0 : $cumulativeQuote/$cumulativeSentenceCount;
	$avgNeedsSource = $cumulativeSentenceCount == 0 ? 0 : $cumulativeNeedsSource/$cumulativeSentenceCount;
	$linkQualityAverage = $numLinks == 0 ? -1 : $cumulativeLinkQuality/$numLinks;

	global $qualityDefinition;
	$quality = $qualityDefinition[intval($linkQualityAverage)];


	if(count($articles) > 1){
		print "<p>Number of Articles: ".number_format($numArticles)."<br/>";
		print "Average Percent Unsourced: ".number_format($avgUnsourced*100, 2)."%<br/>";
		print "Average Percent Original Reporting: ".number_format($avgOriginalReporting*100, 2)."%<br/>";
		print "Average Percent Primary Source: ".number_format($avgPrimarySource*100, 2)."%<br/>";
		print "Average Percent Secondary Source: ".number_format($avgSecondarySource*100, 2)."%<br/>";
		print "Average Percent Quote: ".number_format($avgQuote*100, 2)."%<br/>";
		print "Average Percent That Needs A Source: ".number_format($avgNeedsSource*100, 2)."%<br/>";
		print "Links per Article: ".number_format($linksPerArticle, 2)."<br/>";
		print "Links per 1000 Words: ".number_format($linksPerMWords, 2)."<br/>";
		print "Link Quality: ".number_format($linkQualityAverage, 2)." ($quality)<br/>";
		print "Sources in Text per Article: ".number_format($sourcesPerArticle, 2)."<br/>";
		print "Sources in Text per 1000 Words: ".number_format($sourcesPerMWords, 2)."<br/>";
		print "Average Word Count: ".number_format($wordsPerArticle, 0)."<br/>";
		print "Average Sentence Count: ".number_format($sentencesPerArticle, 0)."<br/>";
		print "Average Flesch-Kincaid Grade Level: ".number_format($avgGradeLevel, 1)."</p>";
	}
	else if(count($articles) == 1){
		print "<h1 class='lead'>Number of Articles: ".number_format($numArticles)."</h1>";
		print "<h1 class='lead'>Percent Unsourced: ".number_format($avgUnsourced*100, 2)."%</h1>";
		print "<h1 class='lead'>Percent Original Reporting: ".number_format($avgOriginalReporting*100, 2)."%</h1>";
		print "<h1 class='lead'>Percent Primary Source: ".number_format($avgPrimarySource*100, 2)."%</h1>";
		print "<h1 class='lead'>Percent Secondary Source: ".number_format($avgSecondarySource*100, 2)."%</h1>";
		print "<h1 class='lead'>Percent Quote: ".number_format($avgQuote*100, 2)."%</h1>";
		print "<h1 class='lead'>Percent That Needs A Source: ".number_format($avgNeedsSource*100, 2)."%</h1>";
		print "<h1 class='lead'>Links: ".number_format($linksPerArticle)."</h1>";
		print "<h1 class='lead'>Links per 1000 words: ".number_format($linksPerMWords, 2)."</h1>";
		print "<h1 class='lead'>Link Quality: ".number_format($linkQualityAverage, 2)." ($quality)</h1>";
		print "<h1 class='lead'>Sources in Text per Article: ".number_format($sourcesPerArticle)."</h1>";
		print "<h1 class='lead'>Sources in Text per 1000 Words: ".number_format($sourcesPerMWords)."</h1>";
		print "<h1 class='lead'>Word count: ".number_format($wordsPerArticle)."</h1>";
		print "<h1 class='lead'>Sentence Count: ".number_format($sentencesPerArticle)."</h1>";
		print "<h1 class='lead'>Flesch-Kincaid Grade Level: ".number_format($avgGradeLevel, 1)."</h1>";
	}
	else if(count($articles) ==  0){
		print "<h1 class='lead'>No Articles to Analyze</h1>";
	}
}