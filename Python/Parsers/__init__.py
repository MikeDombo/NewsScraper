from bs4 import BeautifulSoup


class Parsers:
	def __init__(self):
		pass

	def url_recognized(self, url):
		return False

	def get_article_text(self, webpage):
		return webpage

	def get_article_section(self, webpage, url):
		pass

	def get_article_title(self, webpage):
		beautifulWebpage = BeautifulSoup(webpage, 'html.parser')
		return beautifulWebpage.title.string

	def get_article_author(self, webpage):
		beautifulWebpage = BeautifulSoup(webpage, 'html.parser')
		return beautifulWebpage.find("meta", {"name": "author"})['content']

	def get_article_publish_date(self, webpage):
		beautifulWebpage = BeautifulSoup(webpage, 'html.parser')
		pdate = beautifulWebpage.find("meta", {"name": "pdate"})['content']
		from dateutil.parser import parse
		return parse(pdate)

	def get_article_publisher(self, webpage):
		from urlparse import urlparse
		o = urlparse(self.url)
		return o.hostname

	def get_article_sources(self, webpage):
		mySources = []
		beautifulWebpage = BeautifulSoup(webpage, 'html.parser')
		for link in beautifulWebpage.find_all('a'):
			l = link.get('href')
			if l.find("mailto:") == -1:
				mySources.append(l)
		return mySources
