from bs4 import BeautifulSoup
from Scrapers import Scrapers
import requests
from urlparse import urlparse, urljoin
import datetime as dt
import httplib


class TheIndependent(Scrapers):
	@staticmethod
	def get_article_list(date=None):
		"""
		Returns list of article URLs from a given scraper subclass

		:param date: date of articles to be enumerated or None
		:type date: DateTime
		:return: list of URLs of articles to be analyzed
		:rtype: list
		"""
		article_list = []
		if date is None:
			dateurl = dt.datetime.now().strftime("%Y-%m-%d")
		elif isinstance(date, dt.datetime):
			dateurl = date.strftime("%Y-%m-%d")
		else:
			dateurl = dt.datetime.fromtimestamp(date).strftime("%Y-%m-%d")
		url = "http://www.independent.co.uk/archive/" + dateurl
		response = requests.get(url).text
		page = BeautifulSoup(response, 'html.parser')
		for articles in page.findAll("ol", {"class": "archive-news-list"}):
			for links in articles.findAll("a"):
				article_link = links.get('href')
				if article_link is not None:
					article_link = urljoin(url, article_link)
					href = urlparse(article_link)
					article_link = href.scheme + '://' + href.netloc + href.path
					if "/competitions/" not in article_link:
						conn = httplib.HTTPConnection(href.netloc)
						conn.request("HEAD", href.path)
						if conn.getresponse().status == 200:
							article_list.append(article_link)
		return article_list

	def __init__(self, db):
		super(TheIndependent, self).__init__(db)
