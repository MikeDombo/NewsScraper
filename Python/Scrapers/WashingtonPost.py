from bs4 import BeautifulSoup
from Scrapers import Scrapers
import requests
from urlparse import urlparse


class WashingtonPost(Scrapers):
	def get_article_data(self):
		super(WashingtonPost, self).get_article_data()

	def get_article_list(self, date=None):
		articleList = []
		if date is not None:
			raise ValueError("This scraper does not accept differing dates, it can only show the latest articles")

		url = "https://www.washingtonpost.com/todays_paper/updates/"
		response = requests.get(url).text
		page = BeautifulSoup(response, 'html.parser')
		for articles in page.findAll("ul", {"class": "without-subsection-header"}):
			for links in articles.findAll("a", {"class": "headline"}):
				articleLink = links.get('href')
				if articleLink is not None:
					href = urlparse(articleLink)
					articleLink = href.scheme + '://' + href.netloc + href.path
					if "_story.html" in articleLink:
						articleList.append(articleLink)
		return articleList

	def __init__(self, db):
		super(WashingtonPost, self).__init__(db)
