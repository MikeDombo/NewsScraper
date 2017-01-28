from Parsers import Parsers
from bs4 import BeautifulSoup
import re


class TheGuardian(Parsers):
	def __init__(self):
		super(TheGuardian, self).__init__()
		self._recognized_urls = ["theguardian.com", "theguardian.co.uk"]

	@staticmethod
	def get_article_publish_date(webpage):
		"""
		Parses webpage to return the date the article was published

		:param webpage:
		:return: Article publish date
		:rtype: DateTime object
		"""
		bw = BeautifulSoup(webpage, 'html.parser')
		pdate = bw.find("time", {"itemprop": "datePublished"})['datetime']
		from dateutil.parser import parse
		return parse(pdate)

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
		for text in bw.find("div", {'itemprop': ['articleBody', 'reviewBody']}).find_all("p"):
			p = text.parent.name
			if not p == "li":
				for br in text.find_all("br"):
					br.replace_with("\r\n")
				if not text.text == "":
					return_text += text.text.encode("UTF-8") + "\r\n\r\n"
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
		for text in bw.find("div", {'itemprop': ['articleBody', 'reviewBody']}).find_all("p"):
			p = text.parent.name
			if not p == "li":
				for link in text.find_all("a"):
					if "auto-linked-tag" not in link['data-link-name']:
						l = link.get('href')
						if l is not None:
							if l.find("mailto:") == -1:
								my_sources.append(l)
		return my_sources

	@staticmethod
	def get_article_section(webpage, url):
		"""
		Parses webpage and/or url to return a list of sections/subsections that the article is in

		:param webpage:
		:param url:
		:return: list of section names in order from most narrow to biggest section
		:rtype: list
		"""

		section = re.findall("theguardian\.com/(.*)/\d{4}/\w{3}/\d{2}", url, re.IGNORECASE)[0]
		section = section.split("/")
		section.reverse()
		return section
