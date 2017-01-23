"""
The Scrapers Module is used for getting a list of articles to download, downloading, sending to the parser, and then
saving the data to a database

:Last Modified: 2017-01-18
:Author: Michael Dombrowski
"""

import datetime as dt
import json
import sqlite3
import time
import requests
from Article import Article
from Parsers import Parsers
from textstat import textstat


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

	@staticmethod
	def normalize_url(url):
		"""
		Parses a given url and normalizes it to be all lowercase, be http, and have "www.".

		This is used to prevent duplication of articles due to non-unique URLs.

		:param url: unnormalized url
		:return: normalized url
		"""
		from urlparse import urlparse
		u = urlparse(url)
		url = u.hostname.lower()+u.path.lower()
		if not url.find("www.") == 0:
			url = "www."+url
		url = "http://"+url
		return url

	def get_article_data(self, webpage=None):
		# Get the webpage
		"""
		- Uses class `url` variable to download the webpage
		- Parses the webpage using `my_parser`
		- Saves parsed data into `current_article`
		"""
		if webpage is None:
			response = requests.get(self.url, headers=self.headers)
			while not response.ok:
				print("Sleeping 10 seconds and retrying " + self.url)
				time.sleep(10)
				response = requests.get(self.url, headers=self.headers)
			# Get HTML from response object
			response = response.text
		else:
			response = webpage

		# Parse the webpage and save the data
		self.current_article.url = self.normalize_url(self.url)
		self.current_article.fetch_date = dt.datetime.now()
		self.current_article.section = self.my_parser.get_article_section(response, self.url)
		self.current_article.title = self.my_parser.get_article_title(response)
		self.current_article.subtitle = self.my_parser.get_article_subtitle(response)
		self.current_article.author = self.my_parser.get_article_author(response)
		self.current_article.publisher = self.my_parser.get_article_publisher(response, self.url)
		self.current_article.publish_date = self.my_parser.get_article_publish_date(response)
		self.current_article.sources = self.my_parser.get_article_sources(response)
		self.current_article.full_html = response
		self.current_article.article_text = self.my_parser.get_article_text(response)

		text_stats = textstat.textstatistics()
		self.current_article.grade_level = text_stats.flesch_kincaid_grade(self.current_article.article_text)

	@staticmethod
	def get_article_html_from_db(url, database_filename):
		"""
		Returns only the HTML of the selected URL if it is in the database

		:param database_filename:
		:return:
		"""
		conn = sqlite3.connect(database_filename)
		c = conn.cursor()
		c.execute('SELECT `ArticleURL`, `ArticleHTML` FROM `Articles` WHERE `ArticleURL` = ?', [url])
		ret = c.fetchone()
		conn.close()
		# Return the HTML of the selected webpage
		return ret[1]

	@staticmethod
	def get_article_list(date):
		"""
		Returns list of article URLs from a given scraper subclass

		:param date: date of articles to be enumerated or None
		:type date: DateTime
		:return: list of URLs of articles to be analyzed
		:rtype: list
		"""
		pass

	def queue_article_list(self, article_list):
		"""
		Adds each URL in the given article_list to the Queue table of the database

		:param article_list: List of article URLs to be inserted into the DB
		:return: Void
		"""
		conn = sqlite3.connect(self.database_filename)
		c = conn.cursor()
		for a in article_list:
			c.execute('INSERT OR IGNORE INTO `Queue` (url, dateAdded) VALUES (?,?)', [self.normalize_url(a), dt.datetime.now().__str__()])
		conn.commit()
		conn.close()

	def save_data_to_db(self):
		"""
		Saves current article to the connected database

		:return: Void
		"""
		ca = self.current_article
		conn = sqlite3.connect(self.database_filename)
		conn.text_factory = str
		c = conn.cursor()
		c.execute('''REPLACE INTO `Articles` (ArticleURL, Headline, Subtitle, Author, Publisher, PublishDate, ArticleText,
				  ArticleHTML, ArticleSources, RetrievalDate, ArticleSection, GradeLevel, HasUpdates, HasNotes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
				  [self.url, ca.title, ca.subtitle, ca.author, ca.publisher,
				   ca.publish_date, ca.article_text, ca.full_html, json.dumps(ca.sources), ca.fetch_date,
				   json.dumps(ca.section), ca.grade_level, ca.updates, ca.editor_notes])
		conn.commit()
		conn.close()

	@staticmethod
	def read_article_queue(database_filename):
		"""
		Reads database Queue table and returns the whole table as a list

		:return: list of URLs to be downloaded and parsed
		"""
		conn = sqlite3.connect(database_filename)
		c = conn.cursor()
		c.execute('SELECT * FROM `Queue`')
		ret = c.fetchall()
		conn.close()
		return ret

	def is_already_analyzed(self):
		"""
		Checks if the current URL is in the Articles table

		:rtype: Boolean
		:return: True if the set URL is already in the Articles table of the database
		"""
		conn = sqlite3.connect(self.database_filename)
		c = conn.cursor()
		c.execute('SELECT * FROM `Articles` WHERE `ArticleURL` = ?', [self.url])
		return c.fetchone() is not None

	def __init__(self, db):
		self.current_article = Article()
		self.my_parser = Parsers()
		self.database_filename = db
