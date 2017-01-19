from bs4 import BeautifulSoup
import urlparse


class Parsers(object):
	def __init__(self):
		self._recognized_urls = []

	def url_recognized(self, url):
		"""
		Checks if this parser can parse a given URL

		:param url: URL to check if this parser can recognize it
		:return: True if this parser can parse the given URL
		:rtype: Boolean
		"""
		return any(u in urlparse.urlparse(url).netloc for u in self._recognized_urls)

	@staticmethod
	def get_article_text(webpage):
		"""
		Parses webpage to return the full plaintext of the article

		:param webpage:
		:return: Plaintext of article
		:rtype: str
		"""
		return webpage

	@staticmethod
	def get_article_section(webpage, url):
		"""
		Parses webpage and/or url to return a list of sections/subsections that the article is in

		:param webpage:
		:param url:
		:return: list of section names in order from most narrow to biggest section
		:rtype: list
		"""
		return []

	@staticmethod
	def get_article_title(webpage):
		"""
		Parses webpage to return the title/headline of an article

		:param webpage:
		:return: Article headline
		:rtype: str
		"""
		bw = BeautifulSoup(webpage, 'html.parser')
		return bw.title.string

	@staticmethod
	def get_article_author(webpage):
		"""
		Parses webpage to return the author of the article

		:param webpage:
		:return: Author of the article
		:rtype: str
		"""
		bw = BeautifulSoup(webpage, 'html.parser')
		return bw.find("meta", {"name": "author"})['content']

	@staticmethod
	def get_article_publish_date(webpage):
		"""
		Parses webpage to return the date the article was published

		:param webpage:
		:return: Article publish date
		:rtype: DateTime object
		"""
		bw = BeautifulSoup(webpage, 'html.parser')
		pdate = bw.find("meta", {"name": "pdate"})['content']
		from dateutil.parser import parse
		return parse(pdate)

	@staticmethod
	def get_article_publisher(webpage, url):
		"""
		Parses webpage and/or url to return the publisher of an article

		:param webpage:
		:param url:
		:return: Article publisher, ex: "The New York Times"
		:rtype: str
		"""
		from urlparse import urlparse
		o = urlparse(url)
		return o.hostname

	@staticmethod
	def get_article_sources(webpage):
		"""
		Parses webpage to extract all sources from an article

		:param webpage:
		:return: list of sources, typically URLs of the sources
		:rtype: list
		"""
		my_sources = []
		bw = BeautifulSoup(webpage, 'html.parser')
		for link in bw.find_all('a'):
			l = link.get('href')
			if l.find("mailto:") == -1:
				my_sources.append(l)
		return my_sources
