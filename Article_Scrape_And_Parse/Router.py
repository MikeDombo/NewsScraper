import importlib
import pkgutil
import Scrapers
import Parsers


class Router(object):
	def __init__(self, db):
		self.db = db
		self.__import_submodules(Scrapers)
		self.__import_submodules(Parsers)

		self.__scrapers = [Scrapers.NYTimes.NYTimes(self.db), Scrapers.WashingtonPost.WashingtonPost(self.db),
						   Scrapers.TheIndependent.TheIndependent(self.db), Scrapers.TheGuardian.TheGuardian(self.db)]
		self.__parsers = [Parsers.NYTimes.NYTimes(), Parsers.WashingtonPost.WashingtonPost(),
						  Parsers.TheIndependent.TheIndependent(), Parsers.TheGuardian.TheGuardian()]

	def get_scrapers(self):
		for s in self.__scrapers:
			yield s

	def get_parsers(self):
		for p in self.__parsers:
			yield p

	def get_parsers_by_url(self, url):
		for p in self.__parsers:
			if p.url_recognized(url):
				return p
		return None

	def __import_submodules(self, package, recursive=True):
		""" Import all submodules of a module, recursively, including subpackages

		:param package: package (name or actual module)
		:type package: str | module
		:rtype: dict[str, types.ModuleType]
		"""

		if isinstance(package, str):
			package = importlib.import_module(package)
		results = {}
		for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
			full_name = package.__name__ + '.' + name
			results[full_name] = importlib.import_module(full_name)
			if recursive and is_pkg:
				results.update(self.__import_submodules(full_name))
		return results
