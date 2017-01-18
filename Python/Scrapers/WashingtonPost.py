from bs4 import BeautifulSoup
from Scrapers import Scrapers
import requests
from urlparse import urlparse


class WashingtonPost(Scrapers):
	@staticmethod
	def get_article_list(date=None):
		article_list = []
		if date is not None:
			raise ValueError("This scraper does not accept differing dates, it can only show the latest articles")

		url = "https://www.washingtonpost.com/todays_paper/updates/"
		response = requests.get(url).text
		page = BeautifulSoup(response, 'html.parser')
		for articles in page.findAll("ul", {"class": "without-subsection-header"}):
			for links in articles.findAll("a", {"class": "headline"}):
				article_link = links.get('href')
				if article_link is not None:
					href = urlparse(article_link)
					article_link = href.scheme + '://' + href.netloc + href.path
					if "_story.html" in article_link:
						article_list.append(article_link)
		return article_list

	def __init__(self, db):
		super(WashingtonPost, self).__init__(db)
