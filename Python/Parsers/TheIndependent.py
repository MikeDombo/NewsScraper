from Parsers import Parsers
from bs4 import BeautifulSoup
import re


class TheIndependent(Parsers):
	def __init__(self):
		super(TheIndependent, self).__init__()
		self._recognized_urls = ["independent.co.uk", "theindependent.co.uk"]

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
		for text in bw.find("div", {'itemprop':'articleBody'}).find_all("p", {'class':None}):
			for br in text.find_all("br"):
				br.replace_with("\r\n")
			if not text.text == "":
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
		for text in bw.find("div", {'itemprop': 'articleBody'}).find_all("p", {'class': None}):
			for link in text.find_all("a"):
				if link.get('class') is None:
					l = link.get('href')
					if l.find("mailto:") == -1:
						my_sources.append(l)
		return my_sources

	@staticmethod
	def get_article_subtitle(webpage):
		"""
		Parses webpage to return the subtitle of an article

		:param webpage:
		:return: Article subtitle
		:rtype: str
		"""
		subtitle = ""
		bw = BeautifulSoup(webpage, 'html.parser')
		try:
			for text in bw.find("div", {'class': 'intro'}).find_all("p"):
				subtitle += text.text + "\r\n"
		except AttributeError:
			subtitle = ""
		return subtitle.strip()

	@staticmethod
	def get_article_author(webpage):
		"""
		Parses webpage to return the author of the article

		:param webpage:
		:return: Author of the article
		:rtype: str
		"""
		bw = BeautifulSoup(webpage, 'html.parser')
		return bw.find("meta", {"name": "article:author_name"})['content']

	@staticmethod
	def get_article_publish_date(webpage):
		"""
		Parses webpage to return the date the article was published

		:param webpage:
		:return: Article publish date
		:rtype: DateTime object
		"""
		bw = BeautifulSoup(webpage, 'html.parser')
		pdate = bw.find("meta", {"property": "article:published_time"})['content']
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

		section = re.findall(".*independent\.co\.uk/(.*)\.html$", url)[0]
		section = section.split("/")
		del[section[len(section)-1]]
		section.reverse()
		return section
