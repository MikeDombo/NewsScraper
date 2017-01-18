import datetime as dt
import json
import sqlite3
import time
import requests
from Article import Article
from Parsers import Parsers


class Scrapers(object):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.87 Safari/537.36',
		'Accept-Encoding': ', '.join(('gzip', 'deflate')),
		'Connection': 'keep-alive',
		'Pragma': 'no-cache',
		'Cache-Control': 'no-cache',
		'Upgrade-Insecure-Requests': '1',
		'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
		'DNT': '1',
		'Referer': 'https://www.google.com/',
		'Accept-Language': 'en-US,en;q = 0.8'
	}
	url = ""

	def get_article_data(self):
		# Get the webpage
		"""
		Uses class url variable to download the webpage
		Parses the webpage using myParser
		Saves parsed data into currentArticle
		"""
		response = requests.get(self.url, headers=self.headers)
		while not response.ok:
			print("Sleeping 10 seconds and retrying " + self.url)
			time.sleep(10)
			response = requests.get(self.url, headers=self.headers)
		# Get HTML from response object
		response = response.text

		# Parse the webpage and save the data
		self.currentArticle.url = self.url
		self.currentArticle.fetchedDate = dt.datetime.now()
		self.currentArticle.articleSection = self.myParser.get_article_section(response, self.url)
		self.currentArticle.articleTitle = self.myParser.get_article_title(response)
		self.currentArticle.articleAuthor = self.myParser.get_article_author(response)
		self.currentArticle.articlePublisher = self.myParser.get_article_publisher(response)
		self.currentArticle.articleDate = self.myParser.get_article_publish_date(response)
		self.currentArticle.sources = self.myParser.get_article_sources(response)
		self.currentArticle.articleHTML = response
		self.currentArticle.articleText = self.myParser.get_article_text(response)

	def get_article_list(self, date):
		"""
		:param date: date of articles to be enumerated or None
		:return list of URLs of articles to be analyzed
		:rtype list
		"""
		pass

	def queue_article_list(self, articleList):
		"""
		:param articleList: List of article URLs to be inserted into the DB
		:return Void
		"""
		conn = sqlite3.connect(self.NewsDatabase)
		c = conn.cursor()
		for a in articleList:
			c.execute('INSERT OR IGNORE INTO `Queue` (url, dateAdded) VALUES (?,?)', [a, dt.datetime.now().__str__()])
		conn.commit()
		conn.close()

	def save_data_to_db(self):
		ca = self.currentArticle
		conn = sqlite3.connect(self.NewsDatabase)
		c = conn.cursor()
		c.execute('''INSERT OR IGNORE INTO `Articles` (ArticleURL, Headline, Subtitle, Author, Publisher, PublishDate, ArticleText,
				  ArticleHTML, ArticleSources, RetrievalDate, ArticleSection, HasUpdates, HasNotes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)''',
				  [self.url, ca.articleTitle, ca.articleSubtitle, ca.articleAuthor, ca.articlePublisher,
				   ca.articleDate, ca.articleText, ca.articleHTML, json.dumps(ca.sources), ca.fetchedDate,
				   json.dumps(ca.articleSection), ca.articleUpdates, ca.articleNotes])
		conn.commit()
		conn.close()

	def read_article_queue(self):
		conn = sqlite3.connect(self.NewsDatabase)
		c = conn.cursor()
		c.execute('SELECT * FROM `Queue`')
		ret = c.fetchall()
		conn.close()
		return ret

	def is_already_analyzed(self):
		conn = sqlite3.connect(self.NewsDatabase)
		c = conn.cursor()
		c.execute('SELECT * FROM `Articles` WHERE `ArticleURL` = ?', [self.url])
		return c.fetchone() is not None

	def __init__(self, db):
		self.currentArticle = Article()
		self.myParser = Parsers()
		self.NewsDatabase = db
