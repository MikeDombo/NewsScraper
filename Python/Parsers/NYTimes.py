from Parsers import Parsers
from bs4 import BeautifulSoup
import urlparse


class NYTimes(object, Parsers):
	def __init__(self):
		super(NYTimes, self).__init__()

	__recognizedURLs = ["nytimes.com", "nyt.com", "nyti.ms", "newyorktimes.com", "thenewyorktimes.com"]

	def url_recognized(self, url):
		return any(u in urlparse.urlparse(url).netloc for u in self.__recognizedURLs)

	def get_article_publisher(self, webpage):
		return "The New York Times"

	def get_article_section(self, webpage, url):
		pass

	def get_article_text(self, webpage):
		beautifulWebpage = BeautifulSoup(webpage, 'html.parser')
		returnText = ""
		for text in beautifulWebpage.find_all("p", {"class": 'story-body-text'}):
			for br in text.find_all("br"):
				br.replace_with("\r\n")
			returnText += text.text + "\r\n\r\n"
		returnText = returnText.strip()
		return returnText

	def get_article_sources(self, webpage):
		mySources = []
		beautifulWebpage = BeautifulSoup(webpage, 'html.parser')
		for text in beautifulWebpage.find_all("p", {"class": 'story-body-text'}):
			for link in text.find_all("a"):
				if link.get('class') is None:
					l = link.get('href')
					if l.find("mailto:") == -1:
						mySources.append(l)
		return mySources

	def get_article_title(self, webpage):
		beautifulWebpage = BeautifulSoup(webpage, 'html.parser')
		return beautifulWebpage.find("meta", {"name": "hdl"})['content']
