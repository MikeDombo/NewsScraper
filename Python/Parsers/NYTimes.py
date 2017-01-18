from Parsers import Parsers
from bs4 import BeautifulSoup


class NYTimes(Parsers):
	def __init__(self):
		super(NYTimes, self).__init__()

	__recognized_urls = ["nytimes.com", "nyt.com", "nyti.ms", "newyorktimes.com", "thenewyorktimes.com"]

	@classmethod
	def get_article_publisher(cls, webpage, url):
		return "The New York Times"

	@staticmethod
	def get_article_section(webpage, url):
		pass

	@staticmethod
	def get_article_text(webpage):
		bw = BeautifulSoup(webpage, 'html.parser')
		return_text = ""
		for text in bw.find_all("p", {"class": 'story-body-text'}):
			for br in text.find_all("br"):
				br.replace_with("\r\n")
			return_text += text.text + "\r\n\r\n"
		return_text = return_text.strip()
		return return_text

	@staticmethod
	def get_article_sources(webpage):
		my_sources = []
		bw = BeautifulSoup(webpage, 'html.parser')
		for text in bw.find_all("p", {"class": 'story-body-text'}):
			for link in text.find_all("a"):
				if link.get('class') is None:
					l = link.get('href')
					if l.find("mailto:") == -1:
						my_sources.append(l)
		return my_sources

	@staticmethod
	def get_article_title(webpage):
		bw = BeautifulSoup(webpage, 'html.parser')
		return bw.find("meta", {"name": "hdl"})['content']
