from Parsers import Parsers
from bs4 import BeautifulSoup


class NYTimes(Parsers):
	def __init__(self):
		super(NYTimes, self).__init__()
		self._recognized_urls = ["nytimes.com", "nyt.com", "nyti.ms", "newyorktimes.com", "thenewyorktimes.com"]

	@staticmethod
	def get_article_publisher(webpage, url):
		"""
		Parses webpage and/or url to return the publisher of an article

		:param webpage:
		:param url:
		:return: Article publisher, ex: "The New York Times"
		:rtype: str
		"""
		return "The New York Times"

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
	def get_article_section(webpage, url):
		"""
		Parses webpage and/or url to return a list of sections/subsections that the article is in

		:param webpage:
		:param url:
		:return: list of section names in order from most narrow to biggest section
		:rtype: list
		"""
		from urlparse import urlparse
		import re
		u = urlparse(url).path
		a = re.match(".*/\d{4}/\d{2}/\d{2}/(?P<after_date>.*)", u)
		sections = a.group("after_date").split("/")
		# Remove article reference from matched URL
		del sections[len(sections) - 1]
		# Put sections in ascending order
		sections.reverse()
		return sections

	@staticmethod
	def get_article_text(webpage):
		"""
		Parses webpage to return the full plaintext of the article

		:param webpage:
		:return: Plaintext of article
		:rtype: str
		"""
		bw = BeautifulSoup(webpage, 'html.parser')
		return_text = ""
		for text in bw.find_all("p", {"class": ['story-body-text', 'g-p', 'paragraph--story']}):
			for br in text.find_all("br"):
				br.replace_with("\r\n")
			return_text += text.text + "\r\n\r\n"
		return_text = return_text.strip()
		return return_text

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
		for text in bw.find_all("p", {"class": ['story-body-text', 'g-p', 'paragraph--story']}):
			for link in text.find_all("a"):
				if link.get('class') is None:
					l = link.get('href')
					if l.find("mailto:") == -1:
						my_sources.append(l)
		return my_sources

	@staticmethod
	def get_article_title(webpage):
		"""
		Parses webpage to return the title/headline of an article

		:param webpage:
		:return: Article headline
		:rtype: str
		"""
		bw = BeautifulSoup(webpage, 'html.parser')
		return bw.find("meta", {"name": "hdl"})['content']
