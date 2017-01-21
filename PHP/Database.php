<?php

require_once "Article.php";

/**
 * @author Michael Dombrowski
 */
class Database{
	/** @var  \PDO */
	private $pdo;

	/** @var  \Article */
	private $articles;

	/**
	 * @param \PDO $pdo
	 */
	public function __construct(\PDO $pdo){
		$this->pdo = $pdo;
		$this->articles = $this->readDatabase();
	}

	/**
	 * @return array|\Article
	 */
	public function getArticles(): array {
		return $this->articles;
	}

	/**
	 * Returns array of \Article objects that have the same publisher as the given $publisher
	 * @param string $publisher
	 * @return array
	 */
	public function getArticlesByPublisher(string $publisher): array {
		$selected = [];
		foreach($this->articles as $a){
			if($a->getPublisher() == $publisher){
				$selected[] = $a;
			}
		}
		return $selected;
	}

	/**
	 * Returns array of \Article objects that have the same author as the given $author
	 * @param string $author
	 * @return array
	 */
	public function getArticlesByAuthor(string $author): array {
		$selected = [];
		foreach($this->articles as $a){
			if($a->getAuthor() == $author){
				$selected[] = $a;
			}
		}
		return $selected;
	}

	/**
	 * Returns array of \Article objects that have the same section as the given $section
	 * @param string $section
	 * @return array
	 */
	public function getArticlesBySection(string $section): array {
		$selected = [];
		foreach($this->articles as $a){
			if(in_array($section, $a->getArticleSection())){
				$selected[] = $a;
			}
		}
		return $selected;
	}

	/**
	 * Returns array of \Article objects that were published on a given day of the week
	 * @param string $day Day of the week
	 * @return array|\Article
	 */
	public function getArticlesByDayOfWeek(string $day): array {
		$selected = [];
		foreach($this->articles as $a){
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
		foreach($this->articles as $a){
			foreach($a->getArticleSection() as $s){
				if(!in_array($s, $sections, true)){
					$sections[] = $s;
				}
			}
		}
		return $sections;
	}

	/**
	 * Returns a list of all the authors any article in the database wrote
	 * @return array|string
	 */
	public function listAllAuthors(): array {
		$authors = [];
		foreach($this->articles as $a){
			if(!in_array($a->getAuthor(), $authors, true)){
				$authors[] = $a->getAuthor();
			}
		}
		return $authors;
	}

	/**
	 * Returns a list of all the publishers in the database
	 * @return array|string
	 */
	public function listAllPublishers(): array {
		$publishers = [];
		foreach($this->articles as $a){
			if(!in_array($a->getPublisher(), $publishers, true)){
				$publishers[] = $a->getPublisher();
			}
		}
		return $publishers;
	}

	/**
	 * Reads database of given \PDO and creates \Article objects for each row
	 * @return array|\Article Array of article objects from the Articles table of the connected database
	 */
	private function readDatabase(): array {
		$localArticles = [];

		$q = $this->pdo->query("SELECT * FROM `Articles`");
		foreach($q->fetchAll() as $a){
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
			$article->setArticleText($a["ArticleText"]);
			$article->setArticleHTML($a["ArticleHTML"]);
			$article->setArticleSources(json_decode($a["ArticleSources"], true));
			$article->setRetrievalDate($fDate);
			$article->setArticleSection(json_decode($a["ArticleSection"], true));
			$article->setIsPrimarySource($a["IsPrimarySource"]);
			$article->setHasUpdates($a["HasUpdates"]);
			$article->setHasNotes($a["HasNotes"]);

			$localArticles[] = $article;
		}
		return $localArticles;
	}
}
