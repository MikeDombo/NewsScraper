from bs4 import BeautifulSoup
from Scrapers import Scrapers
import requests
from urlparse import urlparse
import datetime as dt
import re


class NYTimes(Scrapers):
	def get_article_data(self):
		super(NYTimes, self).get_article_data()

	def get_article_list(self, date=None):
		articleList = []
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
				articleLink = links.get('href')
				if articleLink is not None:
					href = urlparse(articleLink)
					articleLink = href.scheme+'://'+href.netloc+href.path
					hasMatch = re.match('.*/\d{4}/\d{2}/\d{2}/*', articleLink) is not None
					if articleLink not in articleList and hasMatch:
						articleList.append(articleLink)
		return articleList

	def __init__(self, db):
		super(NYTimes, self).__init__(db)
