import MySQLdb
import random
#import numpy as np


class dataset(object):
	__conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="newsscraper", charset="utf8")
	data = []
	target = []
	categories_names = ["Not a Source", "Original Reporting", "Primary Source", "Secondary Source", "Quote", "Should Source"]
	target_names = []

	def __init__(self, subset, categories, random_state, limit=0):
		self.target_names = categories
		random.seed(random_state)
		assert subset == "train" or subset == "test" or subset == "run"
		c = self.__conn.cursor()
		if subset == "run":
			c.execute("SELECT * FROM `Article-Fragments` WHERE `IsSource` = -1")
			fragments = c.fetchall()
			for f in fragments:
				self.data.append(f[2])
				i = self.target_names.index(self.categories_names[(f[3])])
				self.target.append(i)
			return
		for cat in categories:
			index = self.categories_names.index(cat)
			c.execute("SELECT * FROM `Article-Fragments` WHERE `IsSource` = "+str(index))
			fragments = c.fetchall()
			select = len(fragments)/2
			if limit > 0 and limit < select:
				select = limit
			d = random.sample(fragments, select)
			if subset == "test":
				d = set(fragments)-set(d)
			print cat + " " + str(len(d)) + " of " + str(len(fragments))
			for f in d:
				self.data.append(f[2])
				self.target.append(index)
