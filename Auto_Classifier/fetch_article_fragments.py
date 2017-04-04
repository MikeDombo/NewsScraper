import MySQLdb
import random


class dataset(object):
	__conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="newsscraper", charset="utf8")
	Big_Table = "Fragments-Table"
	Fragment_Train_Table = "Fragments-Table"
	data = []
	target = []
	categories_names = ["Not a Source", "Original Reporting", "Primary Source", "Secondary Source", "Quote", "Should Source"]
	target_names = []
	data_ids = []

	def __init__(self, subset, categories, random_state, limit=0):
		self.target_names = categories
		random.seed(random_state)
		assert subset == "train" or subset == "test" or subset == "run" or subset == "run-all"
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
		elif subset == "run-all":
			c.execute("SELECT * FROM `" + self.Big_Table + "`")
			fragments = c.fetchall()
			for f in fragments:
				self.data.append(f[2])
				self.data_ids.append(f[0])
				i = self.target_names.index(self.categories_names[(f[3])])
				self.target.append(i)
			return
		for cat in categories:
			index = self.categories_names.index(cat)

			c.execute("SELECT count(*) FROM `" + self.Fragment_Train_Table + "` WHERE `IsSource` = " + str(index))
			numClassified = c.fetchone()[0]

			c.execute("SELECT * FROM `" + self.Fragment_Train_Table + "` WHERE `IsSource` = " + str(index) + " AND `Train`=1")
			fragments = c.fetchall()
			couldForceTrain = len(fragments)

			select = numClassified / 2
			if limit < select:
				select = limit

			if select < len(fragments):
				forceTrainSet = random.sample(fragments, select)
			else:
				forceTrainSet = list(fragments)
			forceTrain = len(forceTrainSet)

			c.execute("SELECT * FROM `" + self.Fragment_Train_Table + "` WHERE `IsSource` = " + str(index))
			allClassified = c.fetchall()
			allClassifiedLen = len(allClassified)
			allClassified = set(allClassified)-set(forceTrainSet)

			trainingSet = forceTrainSet
			if len(forceTrainSet) < select:
				trainingSet.extend(random.sample(allClassified, select - len(forceTrainSet)))

			if subset == "test":
				testSet = set(allClassified)-set(trainingSet)
				print(cat + " " + str(len(testSet)) + " of " + str(allClassifiedLen))
				d = testSet
			else:
				print(cat + " " + str(len(trainingSet)) + " of " + str(allClassifiedLen) + " : " + str(forceTrain) + " forcibly trained of " + str(couldForceTrain))
				d = trainingSet
			for f in d:
				self.data.append(f[2])
				self.data_ids.append(f[0])
				self.target.append(index)

	def save_data_to_db(self, id, data):
		c = self.__conn.cursor()
		c.execute("UPDATE `"+self.Big_Table+"` SET `Guess`=%s WHERE `ID`=%s", (data, id))
		self.__conn.commit()
