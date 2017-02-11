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
		Parses a given url and normalizes it to be all lowercase, be http, and not have "www.".

		This is used to prevent duplication of articles due to non-unique URLs.

		:param url: unnormalized url
		:return: normalized url
		"""
		from urlparse import urlparse
		u = urlparse(url)
		url = u.hostname.lower()+u.path.lower()
		if url.find("www.") == 0:
			url = url.replace("www.", "")
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
			if not response.ok:
				raise RuntimeError("Error with URL "+self.url)
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
		self.current_article.article_text = self.my_parser.get_article_text(response)
		self.current_article.sources = self.my_parser.get_article_sources(response)
		self.current_article.sources = self.parse_sources(self.current_article.sources)
		self.current_article.text_sources = self.parse_text_sources(self.current_article.article_text)
		self.current_article.full_html = response

		text_stats = textstat.textstatistics()
		self.current_article.grade_level = text_stats.flesch_kincaid_grade(self.current_article.article_text)

	def parse_sources(self, sources):
		from Router import Router
		from urlparse import urlparse
		my_r = Router()
		for i,s in enumerate(sources):
			parsed = urlparse(s)
			if parsed.path is None or parsed.path == "" or parsed.path == "/":
				sources[i] = {"URL": s, "Quality": 0}
			elif my_r.get_parsers_by_url(s) is not None:
				sources[i] = {"URL": s, "Quality": 1}
			elif len(parsed.path.split("/")) > 1:
				sources[i] = {"URL": s, "Quality": 2}
			else:
				sources[i] = {"URL": s, "Quality": -1}
				from unidecode import unidecode
				print unidecode(s)+" UNKNOWN QUALITY!!!!!"
		return sources

	def parse_text_sources(self, text):
		text_sources = []
		import re
		sentence_regex = ur'[\.\?!]\s+(\"\'\u2018\u2019\u201c\u201d[A-Z][^\"\u2018\u2019\u201c\u201d]*[\.\?!]+\"\u2018\u2019\u201c\u201d)|[\.\?!][\'\"\\u2018\u2019\u201c\u201d)\]]*\s*(?<!\w\.\w.)(?<![A-Z][a-z][a-z]\.)(?<![A-Z][a-z]\.)(?<![A-Z]\.)\s+'
		source_regex = r'([^,;]*) are reporting.*|.*according to\s+([^,;]*)|.*reported by\s+([^,;]*)'
		fragments = re.split(sentence_regex, text)
		for f in fragments:
			if f is not None:
				f = f.strip()
				if len(f) >= 20:
					matches = re.match(source_regex, f)
					if matches is not None:
						for match in matches.groups():
							if match is not None:
								text_sources.append({"sentence": f, "source": match})
		return text_sources

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

	def __init__(self):
		self.current_article = Article()
		self.my_parser = Parsers()
