from bs4 import BeautifulSoup
import urlparse


class Parsers(object):
	def __init__(self):
		pass

	__recognized_urls = []

	@classmethod
	def url_recognized(cls, url):
		"""
		Checks if this parser can parse a given URL

		:param url: URL to check if this parser can recognize it
		:return: True if this parser can parse the given URL
		:rtype: Boolean
		"""
		return any(u in urlparse.urlparse(url).netloc for u in cls.__recognized_urls)

	@staticmethod
	def get_article_text(webpage):
		return webpage

	@staticmethod
	def get_article_section(webpage, url):
		return []

	@staticmethod
	def get_article_title(webpage):
		bw = BeautifulSoup(webpage, 'html.parser')
		return bw.title.string

	@staticmethod
	def get_article_author(webpage):
		bw = BeautifulSoup(webpage, 'html.parser')
		return bw.find("meta", {"name": "author"})['content']

	@staticmethod
	def get_article_publish_date(webpage):
		bw = BeautifulSoup(webpage, 'html.parser')
		pdate = bw.find("meta", {"name": "pdate"})['content']
		from dateutil.parser import parse
		return parse(pdate)

	@staticmethod
	def get_article_publisher(webpage, url):
		from urlparse import urlparse
		o = urlparse(url)
		return o.hostname

	@staticmethod
	def get_article_sources(webpage):
		my_sources = []
		bw = BeautifulSoup(webpage, 'html.parser')
		for link in bw.find_all('a'):
			l = link.get('href')
			if l.find("mailto:") == -1:
				my_sources.append(l)
		return my_sources
