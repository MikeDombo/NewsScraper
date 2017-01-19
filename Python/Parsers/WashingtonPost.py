from Parsers import Parsers
from bs4 import BeautifulSoup
import re


class WashingtonPost(Parsers):
	def __init__(self):
		super(WashingtonPost, self).__init__()
		self._recognized_urls = ["washingtonpost.com", "thewashingtonpost.com"]

	@staticmethod
	def get_article_publisher(webpage, url):
		"""
		Parses webpage and/or url to return the publisher of an article

		:param webpage:
		:param url:
		:return: Article publisher, ex: "The New York Times"
		:rtype: str
		"""
		property = "this.props.source"
		return WashingtonPost.__read_property(webpage, property)

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
		for text in bw.find("article", {'itemprop':'articleBody'}).find_all("p", {'class':None}):
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
		for text in bw.find("article", {'itemprop': 'articleBody'}).find_all("p", {'class': None}):
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
		property = "this.props.headline"
		return WashingtonPost.__read_property(webpage, property).decode('unicode-escape')

	@staticmethod
	def get_article_author(webpage):
		"""
		Parses webpage to return the author of the article

		:param webpage:
		:return: Author of the article
		:rtype: str
		"""
		property = "this.props.author"
		return WashingtonPost.__read_property(webpage, property)

	@staticmethod
	def get_article_publish_date(webpage):
		"""
		Parses webpage to return the date the article was published

		:param webpage:
		:return: Article publish date
		:rtype: DateTime object
		"""
		bw = BeautifulSoup(webpage, 'html.parser')
		url = bw.find("meta", {"property": "og:url"})['content']
		from dateutil.parser import parse
		return parse(re.findall(".*/(\d{4}/\d{2}/\d{2})/.*", url)[0])

	@staticmethod
	def get_article_section(webpage, url):
		"""
		Parses webpage and/or url to return a list of sections/subsections that the article is in

		:param webpage:
		:param url:
		:return: list of section names in order from most narrow to biggest section
		:rtype: list
		"""
		property = "this.props.hierarchy"
		section = WashingtonPost.__read_property(webpage, property).split("|")
		if "article" in section:
			section.remove("article")

		section.reverse()
		return section

	@staticmethod
	def __read_property(webpage, property):
		"""
		Parses JavaScript on Washington Post pages that contain properties including Author, Headline, etc

		:param webpage:
		:param property:
		:return: property value
		:rtype: str
		"""
		webpage = webpage.replace('\n', '').replace('\r', '')
		result = webpage[webpage.find(property) + len(property) + 2:]
		result = result[:result.find(";") - 1]
		return result
