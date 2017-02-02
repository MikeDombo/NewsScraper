from bs4 import BeautifulSoup
from Scrapers import Scrapers
import requests
from urlparse import urlparse
import datetime as dt


class TheGuardian(Scrapers):
	"""sections = ["uk-news", "world/europe-news", "world/americas", "world/asia", "world/middleeast",
				"world/africa", "australian-news", "cities", "global-development", "us-news", "us-news/us-politics",
				"politics", "uk/commentisfree", "us/commentisfree", "lifeandstyle/food-and-drink",
				"lifeandstyle/health-and-wellbeing", "lifeandstyle/love-and-sex", "lifeandstyle/family",
				"lifeandstyle/women", "lifeandstyle/home-and-garden", "fashion", "environment/climate-change",
				"environment/wildlife", "environment/energy", "environment/pollution", "uk/technology",
				"us/technology", "travel/uk", "travel/europe", "travel/us", "travel/skiing", "money/property",
				"money/savings", "money/pensions", "money/debt", "money/work-and-careers", "science"]
	"""

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
			dateurl = dt.datetime.now().strftime("%Y/%b/%d")
		elif isinstance(date, dt.datetime):
			dateurl = date.strftime("%Y/%b/%d")
		else:
			dateurl = dt.datetime.fromtimestamp(date).strftime("%Y/%b/%d")
		url = 'https://www.theguardian.com/theguardian/'+dateurl
		response = requests.get(url).text
		page = BeautifulSoup(response, 'html.parser')
		for articles in page.findAll("section"):
			for links in articles.findAll("a", {"class": "js-headline-text"}):
				article_link = links.get('href')
				if article_link is not None:
					href = urlparse(article_link)
					article_link = href.scheme+'://'+href.netloc+href.path
					if article_link not in article_list and "/picture/" not in article_link:
						article_list.append(article_link)
		return article_list

	def __init__(self, db):
		super(TheGuardian, self).__init__(db)
