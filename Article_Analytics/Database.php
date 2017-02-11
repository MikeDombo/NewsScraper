<?php

require_once "Article.php";

/**
 * @author Michael Dombrowski
 */
class Database{
	private $columns = "`ArticleURL`, `Headline`, `Subtitle`, `Author`, `Publisher`, `PublishDate`, `ArticleSources`,
		`TextSources`, `RetrievalDate`, `ArticleSection`, `GradeLevel`, `IsPrimarySource`, `HasUpdates`, `HasNotes`,
		`ArticleText`";

	/** @var  \PDO */
	private $pdo;

	/** @var  \Article */
	private $articles;

	/**
	 * @param \PDO $pdo
	 */
	public function __construct(\PDO $pdo){
		$this->pdo = $pdo;
		$this->articles = [];
	}

	/**
	 * @return array|Article
	 */
	public function getArticles(): array {
		return $this->articles;
	}

	/**
	 * Returns \Article object with the given URL
	 * @param string $url
	 * @return \Article
	 */
	public function getArticleByURL(string $url): \Article {
		$q = $this->pdo->prepare("SELECT * from `articles` WHERE `ArticleURL`=:url");
		$q->bindValue(":url", $url, PDO::PARAM_STR);
		$q->execute();
		return $this->makeArticleFromDB($q->fetch(PDO::FETCH_ASSOC));
	}

	/**
	 * Returns array of \Article objects that have the same publisher as the given $publisher
	 * @param string $publisher
	 * @return array|Article
	 */
	public function getArticlesByPublisher(string $publisher): array {
		$selected = [];
		$q = $this->pdo->prepare("SELECT ".$this->columns." from `articles` WHERE `Publisher`=:publisher");
		$q->bindValue(":publisher", $publisher, PDO::PARAM_STR);
		$q->execute();
		foreach($q->fetchAll(PDO::FETCH_ASSOC) as $a){
			$selected[] = $this->makeArticleFromDB($a);
		}
		return $selected;
	}

	/**
	 * Returns array of \Article objects that have the same author as the given $author
	 * @param string $author
	 * @return array|Article
	 */
	public function getArticlesByAuthor(string $author): array {
		$selected = [];
		$q = $this->pdo->prepare("SELECT ".$this->columns." from `articles` WHERE `Author`=:author");
		$q->bindValue(":author", $author, PDO::PARAM_STR);
		$q->execute();
		foreach($q->fetchAll(PDO::FETCH_ASSOC) as $a){
			$selected[] = $this->makeArticleFromDB($a);
		}
		return $selected;
	}

	/**
	 * Returns array of \Article objects that have the same section as the given $section
	 * @param string $section
	 * @return array|Article
	 */
	public function getArticlesBySection(string $section): array {
		$selected = [];
		$q = $this->pdo->prepare("SELECT ".$this->columns." from `articles` WHERE `ArticleSection` LIKE :section");
		$q->bindValue(":section", "%\"".$section."\"%", PDO::PARAM_STR);
		$q->execute();
		foreach($q->fetchAll(PDO::FETCH_ASSOC) as $a){
			$sections = json_decode($a["ArticleSection"], true);
			foreach($sections as $s){
				$article = $this->makeArticleFromDB($a);
				if(mb_strtolower($section) == mb_strtolower($s) && !in_array($article, $selected, true)){
					$selected[] = $article;
				}
			}
		}
		return $selected;
	}

	/**
	 * Returns array of \Article objects that were published on a given day of the week
	 * @param string $day Day of the week
	 * @return array|Article
	 */
	public function getArticlesByDayOfWeek(string $day): array {
		$selected = [];
		foreach($this->articles as $a){
			/* @var $a \Article */
			if(date_format($a->getPublishDate(), "l") == $day){
				$selected[] = $a;
			}
		}
		return $selected;
	}

	/**
	 * Returns a list of all the sections any article in the database was published in
	 * @return array|string
	 */
	public function listAllSections(): array {
		$sections = [];
		$q = $this->pdo->query("SELECT `ArticleSection` from `articles` GROUP BY `ArticleSection`");
		foreach($q->fetchAll(PDO::FETCH_ASSOC) as $a){
			$section = json_decode($a["ArticleSection"], true);
			foreach($section as $s){
				/* @var $s string */
				if(!in_array(mb_strtolower($s), $sections, true)){
					$sections[] = mb_strtolower($s);
				}
			}
		}
		sort($sections);
		return $sections;
	}

	/**
	 * Returns a list of all the authors any article in the database wrote
	 * @return array|string
	 */
	public function listAllAuthors(): array {
		$authors = [];
		$q = $this->pdo->query("SELECT `Author` from `articles` GROUP BY `Author`");
		foreach($q->fetchAll(PDO::FETCH_ASSOC) as $a){
			if(!in_array($a["Author"], $authors, true)){
				$authors[] = $a["Author"];
			}
		}
		sort($authors);
		return $authors;
	}

	/**
	 * Returns a list of all the publishers in the database
	 * @return array|string
	 */
	public function listAllPublishers(): array {
		$publishers = [];
		$q = $this->pdo->query("SELECT `Publisher` from `articles` GROUP BY `Publisher`");
		foreach($q->fetchAll(PDO::FETCH_ASSOC) as $a){
			if(!in_array($a["Publisher"], $publishers, true)){
				$publishers[] = $a["Publisher"];
			}
		}
		sort($publishers);
		return $publishers;
	}

	/**
	 * Reads database of given \PDO and creates \Article objects for each row
	 */
	public function readDatabase() {
		$q = $this->pdo->query("SELECT count(*) FROM `Articles`");
		$count = $q->fetch(PDO::FETCH_ASSOC)["count(*)"];
		$numFetched = 0;
		$start = 0;
		// Fetch only 50 articles at a time to limit the memory impact
		while($numFetched < $count){
			$q = $this->pdo->query("SELECT ".$this->columns." FROM `Articles` LIMIT $start,100");
			foreach($q->fetchAll(PDO::FETCH_ASSOC) as $a){
				$this->articles[] = $this->makeArticleFromDB($a);
				$numFetched += 1;
			}
			$start += 100;
		}
	}

	private function makeArticleFromDB($a){
		$article = new Article();

		$pDate = new DateTime();
		$pDate->setTimestamp(strtotime($a["PublishDate"]));
		$fDate = new DateTime();
		$fDate->setTimestamp(strtotime($a["RetrievalDate"]));

		$article->setArticleURL($a["ArticleURL"]);
		$article->setHeadline($a["Headline"]);
		$article->setSubtitle($a["Subtitle"]);
		$article->setAuthor($a["Author"]);
		$article->setPublisher($a["Publisher"]);
		$article->setPublishDate($pDate);
		if(isset($a["ArticleText"])){
			$article->setArticleText($a["ArticleText"]);
		}
		if(isset($a["ArticleHTML"])){
			$article->setArticleHTML($a["ArticleHTML"]);
		}
		$article->setArticleSources(json_decode($a["ArticleSources"], true));
		$article->setTextSources(json_decode($a["TextSources"], true));
		$article->setRetrievalDate($fDate);
		$article->setArticleSection(json_decode($a["ArticleSection"], true));
		$article->setGradeLevel($a["GradeLevel"]);
		$article->setIsPrimarySource($a["IsPrimarySource"]);
		$article->setHasUpdates($a["HasUpdates"]);
		$article->setHasNotes($a["HasNotes"]);

		return $article;
	}
}
