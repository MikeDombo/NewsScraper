from Parsers import Parsers
from bs4 import BeautifulSoup
import re
import urlparse


class WashingtonPost(object, Parsers):
	def __init__(self):
		super(WashingtonPost, self).__init__()

	__recognizedURLs = ["washingtonpost.com", "thewashingtonpost.com"]

	def url_recognized(self, url):
		return any(u in urlparse.urlparse(url).netloc for u in self.__recognizedURLs)

	def get_article_publisher(self, webpage):
		property = "this.props.source"
		return self.__read_property(webpage, property)

	def get_article_text(self, webpage):
		beautifulWebpage = BeautifulSoup(webpage, 'html.parser')
		returnText = ""
		for text in beautifulWebpage.find("article", {'itemprop':'articleBody'}).find_all("p", {'class':None}):
			for br in text.find_all("br"):
				br.replace_with("\r\n")
			returnText += text.text + "\r\n\r\n"
		returnText = returnText.strip()
		return returnText

	def get_article_sources(self, webpage):
		mySources = []
		beautifulWebpage = BeautifulSoup(webpage, 'html.parser')
		for text in beautifulWebpage.find("article", {'itemprop': 'articleBody'}).find_all("p", {'class': None}):
			for link in text.find_all("a"):
				if link.get('class') is None:
					l = link.get('href')
					if l.find("mailto:") == -1:
						mySources.append(l)
		return mySources

	def get_article_title(self, webpage):
		property = "this.props.headline"
		return self.__read_property(webpage, property).decode('unicode-escape')

	def get_article_author(self, webpage):
		property = "this.props.author"
		return self.__read_property(webpage, property)

	def get_article_publish_date(self, webpage):
		beautifulWebpage = BeautifulSoup(webpage, 'html.parser')
		url = beautifulWebpage.find("meta", {"property": "og:url"})['content']
		from dateutil.parser import parse
		return parse(re.findall(".*/(\d{4}/\d{2}/\d{2})/.*", url)[0])

	def get_article_section(self, webpage, url):
		property = "this.props.hierarchy"
		section = self.__read_property(webpage, property).split("|")
		if "article" in section:
			section.remove("article")

		section.reverse()
		return section

	@staticmethod
	def __read_property(webpage, property):
		webpage = webpage.replace('\n', '').replace('\r', '')
		result = webpage[webpage.find(property) + len(property) + 2:]
		result = result[:result.find(";") - 1]
		return result
