import MySQLdb
import random


class dataset(object):
	__conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="newsscraper", charset="utf8")
	Big_Table = "Fragments-Table"
	Fragment_Train_Table = "Article-Fragments"
	data = []
	target = []
	categories_names = ["Not a Source", "Original Reporting", "Primary Source", "Secondary Source", "Quote", "Should Source"]
	target_names = []
	data_ids = []

	def __init__(self, subset, categories, random_state, limit=0):
		self.target_names = categories
		random.seed(random_state)
		assert subset == "train" or subset == "test" or subset == "run"
		c = self.__conn.cursor()
		if subset == "run":
			c.execute("SELECT * FROM `"+self.Big_Table+"` WHERE `IsSource` = -1")
			fragments = c.fetchall()
			for f in fragments:
				self.data.append(f[2])
				self.data_ids.append(f[0])
				i = self.target_names.index(self.categories_names[(f[3])])
				self.target.append(i)
			return
		for cat in categories:
			index = self.categories_names.index(cat)
			c.execute("SELECT * FROM `"+self.Fragment_Train_Table+"` WHERE `IsSource` = "+str(index))
			fragments = c.fetchall()
			select = len(fragments)/2
			if 0 < limit < select:
				select = limit
			d = random.sample(fragments, select)
			if subset == "test":
				d = set(fragments)-set(d)
			print cat + " " + str(len(d)) + " of " + str(len(fragments))
			for f in d:
				self.data.append(f[2])
				self.data_ids.append(f[0])
				self.target.append(index)

	def save_data_to_db(self, id, data):
		c = self.__conn.cursor()
		c.execute("UPDATE `"+self.Big_Table+"` SET `Guess`=%s WHERE `ID`=%s", (data, id))
		self.__conn.commit()
