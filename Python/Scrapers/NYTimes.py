from bs4 import BeautifulSoup
from Scrapers import Scrapers
import requests
from urlparse import urlparse
import datetime as dt
import re


class NYTimes(Scrapers):
	@staticmethod
	def get_article_list(date=None):
		article_list = []
		if date is None:
			dateurl = dt.datetime.now().strftime("%Y/%m/%d")
		elif isinstance(date, dt.datetime):
			dateurl = date.strftime("%Y/%m/%d")
		else:
			dateurl = dt.datetime.fromtimestamp(date).strftime("%Y/%m/%d")
		url = 'http://www.nytimes.com/indexes/'+dateurl+'/todayspaper/index.html'
		response = requests.get(url).text
		page = BeautifulSoup(response, 'html.parser')
		for articles in page.findAll("div", {"class": "columnGroup"}):
			for links in articles.findAll("a", {"class": None}):
				article_link = links.get('href')
				if article_link is not None:
					href = urlparse(article_link)
					article_link = href.scheme+'://'+href.netloc+href.path
					has_match = re.match('.*/\d{4}/\d{2}/\d{2}/*', article_link) is not None
					if article_link not in article_list and has_match:
						article_list.append(article_link)
		return article_list

	def __init__(self, db):
		super(NYTimes, self).__init__(db)
