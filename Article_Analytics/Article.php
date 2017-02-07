<?php

/**
 * Class to hold all data about individual articles based on the structure of the Articles table of the database
 * @author Michael Dombrowski
 */
class Article{
	private $articleURL;
	private $headline;
	private $subtitle;
	private $author;
	private $publisher;
	private $publishDate;
	private $articleText;
	private $articleHTML;
	private $articleSources;
	private $textSources;
	private $retrievalDate;
	private $articleSection;
	private $gradeLevel;
	private $isPrimarySource;
	private $hasUpdates;
	private $hasNotes;

	public function __construct(){
	}

	/**
	 * @return float
	 */
	public function getGradeLevel(): float{
		return $this->gradeLevel;
	}

	/**
	 * @param float $gradeLevel
	 */
	public function setGradeLevel($gradeLevel){
		if($gradeLevel == null){
			$this->gradeLevel = 0;
		}
		else{
			$this->gradeLevel = $gradeLevel;
		}
	}


	/**
	 * @return mixed
	 */
	public function getArticleURL(){
		return $this->articleURL;
	}

	/**
	 * @param mixed $articleURL
	 */
	public function setArticleURL($articleURL){
		$this->articleURL = $articleURL;
	}

	/**
	 * @return mixed
	 */
	public function getHeadline(){
		return $this->headline;
	}

	/**
	 * @param mixed $headline
	 */
	public function setHeadline($headline){
		$this->headline = $headline;
	}

	/**
	 * @return mixed
	 */
	public function getSubtitle(){
		return $this->subtitle;
	}

	/**
	 * @param mixed $subtitle
	 */
	public function setSubtitle($subtitle){
		$this->subtitle = $subtitle;
	}

	/**
	 * @return mixed
	 */
	public function getAuthor(){
		return $this->author;
	}

	/**
	 * @param mixed $author
	 */
	public function setAuthor($author){
		$this->author = $author;
	}

	/**
	 * @return mixed
	 */
	public function getPublisher(){
		return $this->publisher;
	}

	/**
	 * @param mixed $publisher
	 */
	public function setPublisher($publisher){
		$this->publisher = $publisher;
	}

	/**
	 * @return mixed
	 */
	public function getPublishDate(): \DateTime{
		return $this->publishDate;
	}

	/**
	 * @param mixed $publishDate
	 */
	public function setPublishDate(\DateTime $publishDate){
		$this->publishDate = $publishDate;
	}

	/**
	 * @return mixed
	 */
	public function getArticleText(){
		return $this->articleText;
	}

	/**
	 * @param mixed $articleText
	 */
	public function setArticleText($articleText){
		$this->articleText = $articleText;
	}

	/**
	 * @return mixed
	 */
	public function getArticleHTML(){
		return $this->articleHTML;
	}

	/**
	 * @param mixed $articleHTML
	 */
	public function setArticleHTML($articleHTML){
		$this->articleHTML = $articleHTML;
	}

	/**
	 * @return mixed
	 */
	public function getArticleSources(){
		return $this->articleSources;
	}

	/**
	 * @param mixed $articleSources
	 */
	public function setArticleSources($articleSources){
		$this->articleSources = $articleSources;
	}

	/**
	 * @return mixed
	 */
	public function getRetrievalDate(): \DateTime{
		return $this->retrievalDate;
	}

	/**
	 * @param mixed $retrievalDate
	 */
	public function setRetrievalDate(\DateTime $retrievalDate){
		$this->retrievalDate = $retrievalDate;
	}

	/**
	 * @return mixed
	 */
	public function getArticleSection(){
		return $this->articleSection;
	}

	/**
	 * @param mixed $articleSection
	 */
	public function setArticleSection($articleSection){
		$this->articleSection = $articleSection;
	}

	/**
	 * @return mixed
	 */
	public function getIsPrimarySource(){
		return $this->isPrimarySource;
	}

	/**
	 * @param mixed $isPrimarySource
	 */
	public function setIsPrimarySource($isPrimarySource){
		$this->isPrimarySource = $isPrimarySource;
	}

	/**
	 * @return mixed
	 */
	public function getHasUpdates(){
		return $this->hasUpdates;
	}

	/**
	 * @param mixed $hasUpdates
	 */
	public function setHasUpdates($hasUpdates){
		$this->hasUpdates = $hasUpdates;
	}

	/**
	 * @return mixed
	 */
	public function getHasNotes(){
		return $this->hasNotes;
	}

	/**
	 * @param mixed $hasNotes
	 */
	public function setHasNotes($hasNotes){
		$this->hasNotes = $hasNotes;
	}

	/**
	 * @return mixed
	 */
	public function getTextSources(){
		return $this->textSources;
	}

	/**
	 * @param mixed $textSources
	 */
	public function setTextSources($textSources){
		$this->textSources = $textSources;
	}


}
