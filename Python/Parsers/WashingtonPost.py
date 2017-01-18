from Parsers import Parsers
from bs4 import BeautifulSoup
import re


class WashingtonPost(Parsers):
	def __init__(self):
		super(WashingtonPost, self).__init__()

	__recognized_urls = ["washingtonpost.com", "thewashingtonpost.com"]

	@classmethod
	def get_article_publisher(cls, webpage, url):
		property = "this.props.source"
		return cls.__read_property(webpage, property)

	@staticmethod
	def get_article_text(webpage):
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
		my_sources = []
		bw = BeautifulSoup(webpage, 'html.parser')
		for text in bw.find("article", {'itemprop': 'articleBody'}).find_all("p", {'class': None}):
			for link in text.find_all("a"):
				if link.get('class') is None:
					l = link.get('href')
					if l.find("mailto:") == -1:
						my_sources.append(l)
		return my_sources

	@classmethod
	def get_article_title(cls, webpage):
		property = "this.props.headline"
		return cls.__read_property(webpage, property).decode('unicode-escape')

	@classmethod
	def get_article_author(cls, webpage):
		property = "this.props.author"
		return cls.__read_property(webpage, property)

	@staticmethod
	def get_article_publish_date(webpage):
		bw = BeautifulSoup(webpage, 'html.parser')
		url = bw.find("meta", {"property": "og:url"})['content']
		from dateutil.parser import parse
		return parse(re.findall(".*/(\d{4}/\d{2}/\d{2})/.*", url)[0])

	@classmethod
	def get_article_section(cls, webpage, url):
		property = "this.props.hierarchy"
		section = cls.__read_property(webpage, property).split("|")
		if "article" in section:
			section.remove("article")

		section.reverse()
		return section

	@classmethod
	def __read_property(cls, webpage, property):
		webpage = webpage.replace('\n', '').replace('\r', '')
		result = webpage[webpage.find(property) + len(property) + 2:]
		result = result[:result.find(";") - 1]
		return result
