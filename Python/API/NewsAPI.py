from urllib2 import urlopen
import json


class NewsAPI:
	def __init__(self, key):
		self.APIKEY = key
		self.articleURL = "https://newsapi.org/v1/articles"
		self.sourcesURL = "https://newsapi.org/v1/sources"

	def get_articles(self, source, sortBy=None):
		queryParameters = {}
		if sortBy is not None:
			if self.__verify_sortby(sortBy):
				queryParameters["sortBy"] = sortBy
			else:
				raise ValueError("sortBy must be one of: top, latest, or popular")

		queryParameters["source"] = source

		r = urlopen(self.__build_request_url(self.articleURL, queryParameters))
		return json.loads(r.read())

	def get_articles_list(self, source, sortBy=None):
		articleList = []
		r = self.getLatestArticles(source, sortBy)
		if r["status"] == "ok":
			for ar in r["articles"]:
				articleList.append(ar["url"])
		else:
			raise RuntimeError(r["message"])

		return articleList

	def get_sources(self, language=None, category=None, country=None):
		queryParameters = {}
		if language is not None:
			if self.__verify_languages(language):
				queryParameters["language"] = language
			else:
				raise ValueError("Language must be one of: en, de, or fr")
		if category is not None:
			if self.__verify_category(category):
				queryParameters["category"] = category
			else:
				raise ValueError("Category must be one of: business, entertainment, gaming, general, music, science-and-nature, sports, or technology")
		if country is not None:
			if self.__verify_country(country):
				queryParameters["country"] = country
			else:
				raise ValueError("Country must be one of: au, de, gb, in, it, or us")

		r = urlopen(self.__build_request_url(self.sourcesURL, queryParameters))
		return json.loads(r.read())

	def __build_request_url(self, url, parameters):
		parameters["apiKey"] = self.APIKEY
		qp = url+"?"
		for key, value in parameters.iteritems():
			qp += key+"="+value+"&"
		print qp[:-1]
		return qp[:-1]

	@staticmethod
	def __verify_sortby(s):
		sortOrder = ["top", "latest", "popular"]
		return s.lower() in sortOrder

	@staticmethod
	def __verify_languages(l):
		languages = ["en", "de", "fr"]
		return l.lower() in languages

	@staticmethod
	def __verify_category(c):
		categories = ["business", "entertainment", "gaming", "general", "music", "science-and-nature", "sport", "technology"]
		return c.lower() in categories

	@staticmethod
	def __verify_country(c):
		countries = ["au", "de", "gb", "in", "it", "us"]
		return c.lower() in countries
