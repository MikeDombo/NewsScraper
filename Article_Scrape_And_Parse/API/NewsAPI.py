from urllib2 import urlopen
import json


class NewsAPI(object):
	def __init__(self, key):
		self.APIKEY = key
		self.articles_endpoint = "https://newsapi.org/v1/articles"
		self.sources_endpoint = "https://newsapi.org/v1/sources"

	def get_articles(self, source, sort_by=None):
		query_parameters = {}
		if sort_by is not None:
			if self.__verify_sortby(sort_by):
				query_parameters["sortBy"] = sort_by
			else:
				raise ValueError("sortBy must be one of: top, latest, or popular")

		query_parameters["source"] = source

		r = urlopen(self.__build_request_url(self.articles_endpoint, query_parameters))
		return json.loads(r.read())

	def get_articles_url_list(self, source, sort_by=None):
		article_list = []
		r = self.get_articles(source, sort_by)
		if r["status"] == "ok":
			for ar in r["articles"]:
				article_list.append(ar["url"])
		else:
			raise RuntimeError(r["message"])

		return article_list

	def get_sources(self, language=None, category=None, country=None):
		query_parameters = {}
		if language is not None:
			if self.__verify_languages(language):
				query_parameters["language"] = language
			else:
				raise ValueError("Language must be one of: en, de, or fr")
		if category is not None:
			if self.__verify_category(category):
				query_parameters["category"] = category
			else:
				raise ValueError("Category must be one of: business, entertainment, gaming, general, music, science-and-nature, sports, or technology")
		if country is not None:
			if self.__verify_country(country):
				query_parameters["country"] = country
			else:
				raise ValueError("Country must be one of: au, de, gb, in, it, or us")

		r = urlopen(self.__build_request_url(self.sources_endpoint, query_parameters))
		return json.loads(r.read())

	def __build_request_url(self, url, parameters):
		parameters["apiKey"] = self.APIKEY
		qp = url+"?"
		for key, value in parameters.iteritems():
			qp += key+"="+value+"&"
		return qp[:-1]

	@staticmethod
	def __verify_sortby(s):
		sort_order = ["top", "latest", "popular"]
		return s.lower() in sort_order

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
