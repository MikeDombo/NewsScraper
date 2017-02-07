import sqlite3
import MySQLdb
import json
import datetime as dt
from warnings import filterwarnings


class DBConnection(object):
	conn = None
	db_name = None
	db_type = None

	def __init__(self, options=False):
		if options is not False:
			filterwarnings('ignore', category=MySQLdb.Warning)
			if options["db"] == "sqlite":
				self.conn = sqlite3.connect(options["file"])
				self.db_name = options["file"]
				self.conn.text_factory = str
				self.verify_sqlite_db()
			elif options["db"] == "mysql":
				self.conn = MySQLdb.connect(host=options["host"],user=options["user"],passwd=options["password"],
											db=options["file"],charset="utf8")
				self.verify_mysql_db()
			self.db_type = options["db"]

	def get_article_html_from_db(self, url):
		"""
		Returns only the HTML of the selected URL if it is in the database

		:param url:
		:return:
		"""
		c = self.conn.cursor()
		if self.db_type == "mysql":
			c.execute('SELECT `ArticleURL`, `ArticleHTML` FROM `Articles` WHERE `ArticleURL` = %s', (url))
		elif self.db_type == "sqlite":
			c.execute('SELECT `ArticleURL`, `ArticleHTML` FROM `Articles` WHERE `ArticleURL` = ?', [url])
		ret = c.fetchone()
		# Return the HTML of the selected webpage
		return ret[1]

	def queue_article_list(self, article_list):
		"""
		Adds each URL in the given article_list to the Queue table of the database

		:param article_list: List of article URLs to be inserted into the DB
		:return: Void
		"""
		c = self.conn.cursor()
		from Scrapers import Scrapers
		for a in article_list:
			parameters = (Scrapers.normalize_url(a), dt.datetime.now().__str__())
			if self.db_type == "mysql":
				c.execute('INSERT IGNORE INTO `Queue` (url, dateAdded) VALUES (%s,%s)', parameters)
			elif self.db_type == "sqlite":
				c.execute('INSERT OR IGNORE INTO `Queue` (url, dateAdded) VALUES (?,?)', parameters)
		self.conn.commit()

	def save_data_to_db(self, sc):
		"""
		Saves current article to the connected database

		:return: Void
		"""
		ca = sc.current_article
		parameters = (sc.url, ca.title, ca.subtitle, ca.author, ca.publisher,
					ca.publish_date, ca.article_text, ca.full_html, json.dumps(ca.sources),
					json.dumps(ca.text_sources), ca.fetch_date, json.dumps(ca.section),
					ca.grade_level, ca.updates, ca.editor_notes)
		c = self.conn.cursor()
		if self.db_type == "mysql":
			c.execute('''REPLACE INTO `Articles` (ArticleURL, Headline, Subtitle, Author, Publisher, PublishDate, ArticleText,
							  ArticleHTML, ArticleSources, TextSources, RetrievalDate, ArticleSection, GradeLevel, HasUpdates, HasNotes) VALUES
							  (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)''', parameters)
		elif self.db_type == "sqlite":
			c.execute('''REPLACE INTO `Articles` (ArticleURL, Headline, Subtitle, Author, Publisher, PublishDate, ArticleText,
				  ArticleHTML, ArticleSources, TextSources, RetrievalDate, ArticleSection, GradeLevel, HasUpdates, HasNotes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)''',
					  parameters)
		self.conn.commit()

	def read_article_queue(self):
		"""
		Reads database Queue table and returns the whole table as a list

		:return: list of URLs to be downloaded and parsed
		"""
		c = self.conn.cursor()
		c.execute('SELECT * FROM `Queue`')
		return c.fetchall()

	def is_already_analyzed(self, url):
		"""
		Checks if the current URL is in the Articles table

		:rtype: Boolean
		:return: True if the set URL is already in the Articles table of the database
		"""
		c = self.conn.cursor()
		if self.db_type == "mysql":
			c.execute('SELECT * FROM `Articles` WHERE `ArticleURL` = %s', (url))
		elif self.db_type == "sqlite":
			c.execute('SELECT * FROM `Articles` WHERE `ArticleURL` = ?', [url])
		return c.fetchone() is not None

	def verify_mysql_db(self):
		# Create Article Table
		self.conn.query('''CREATE TABLE IF NOT EXISTS `Articles` (
			`ID` INT NOT NULL AUTO_INCREMENT ,
			`ArticleURL` TEXT NOT NULL ,
			`Headline` TEXT NOT NULL ,
			`Subtitle` TEXT NULL ,
			`Author` TEXT NOT NULL ,
			`Publisher` TEXT NOT NULL ,
			`PublishDate` TEXT NOT NULL ,
			`ArticleText` LONGTEXT NOT NULL ,
			`ArticleHTML` LONGTEXT NOT NULL ,
			`ArticleSources` TEXT NOT NULL ,
			`TextSources` TEXT NOT NULL ,
			`RetrievalDate` TEXT NOT NULL ,
			`ArticleSection` TEXT NOT NULL ,
			`GradeLevel` DOUBLE NOT NULL ,
			`IsPrimarySource` INT NULL ,
			`HasUpdates` INT NULL ,
			`HasNotes` INT NULL ,
			PRIMARY KEY (`ID`),
			UNIQUE (`ArticleURL` (150))
			) ENGINE = InnoDB;''')
		# Create Queue Table
		self.conn.query('''CREATE TABLE IF NOT EXISTS `Queue` (
				`ID` INT NOT NULL AUTO_INCREMENT ,
				`url` TEXT NOT NULL ,
				`dateAdded` TEXT NOT NULL ,
				PRIMARY KEY (`ID`),
				UNIQUE (`url` (150))
				) ENGINE = InnoDB;''')

	@staticmethod
	def __is_sqlite3(filename):
		from os.path import isfile, getsize
		if not isfile(filename):
			return False
		if getsize(filename) < 100:  # SQLite database file header is 100 bytes
			return False
		with open(filename, 'rb') as fd:
			header = fd.read(100)
		return header[:16] == 'SQLite format 3\x00'

	def verify_sqlite_db(self):
		# Verify the database
		if not self.__is_sqlite3(self.db_name):
			c = self.conn.cursor()
			# Create Article Table
			c.execute('''CREATE TABLE `Articles` (
							`ID` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
							`ArticleURL` TEXT UNIQUE,
							`Headline` TEXT,
							`Subtitle` TEXT,
							`Author` TEXT,
							`Publisher` TEXT,
							`PublishDate` TEXT,
							`ArticleText` TEXT,
							`ArticleHTML` TEXT,
							`ArticleSources` TEXT,
							`TextSources` TEXT,
							`RetrievalDate` TEXT,
							`ArticleSection` TEXT,
							`GradeLevel` REAL,
							`IsPrimarySource` INTEGER,
							`HasUpdates` INTEGER,
							`HasNotes` INTEGER
						);''')
			# Create Queue Table
			c.execute('''CREATE TABLE `Queue` (
							`ID` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
							`url` TEXT UNIQUE,
							`dateAdded` TEXT
						);''')
			self.conn.commit()
