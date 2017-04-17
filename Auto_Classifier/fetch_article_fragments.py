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
		"""
		Generates the object variables based on given parameters.
		:param subset: Must be "run", "run-all", "test", or "train"
		"Run" generates a list of all unclassified items.
		"run-all" generates a list of all items.
		"test" generates a list of items to test the trained model.
		"train" generates a list of items to train the model with upto 'limit' or 50% (whichever is lower) of the available classified fragments.
		:param categories: The list of categories to put into the list.
		:param random_state: The random seed to use in selecting the test and train sets.
		:param limit: The limit to use in selecting the training and testing sets.
		"""
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
		# Generate test or training set
		for cat in categories:
			index = self.categories_names.index(cat)
			# Get the total number of classified items for the given category
			c.execute("SELECT count(*) FROM `" + self.Fragment_Train_Table + "` WHERE `IsSource` = " + str(index))
			numClassified = c.fetchone()[0]

			# Get any fragments that are classified and set to force training
			c.execute("SELECT * FROM `" + self.Fragment_Train_Table + "` WHERE `IsSource` = " + str(index) + " AND `Train`=1")
			fragments = c.fetchall()
			couldForceTrain = len(fragments)

			select = numClassified / 2
			if limit < select:
				select = limit

			# Generate the force train set by using the whole list or taking a random sample (if the limit is less than half).
			if select < len(fragments):
				forceTrainSet = random.sample(fragments, select)
			else:
				forceTrainSet = list(fragments)
			forceTrain = len(forceTrainSet)

			# Get all classified fragments for this category
			c.execute("SELECT * FROM `" + self.Fragment_Train_Table + "` WHERE `IsSource` = " + str(index))
			allClassified = c.fetchall()
			allClassifiedLen = len(allClassified)
			# Remove from allClassified the fragments which are included in the force training set.
			allClassified = set(allClassified)-set(forceTrainSet)

			trainingSet = forceTrainSet
			# If the number of items in the force training set are less than what should be in the total training set,
			# take a random sample from the remaining trained fragments
			if len(forceTrainSet) < select:
				trainingSet.extend(random.sample(allClassified, select - len(forceTrainSet)))

			if subset == "test":
				# The test set is the set of all classified fragments with all those in the training set removed.
				# As long as the parameters are the same, there will not be any overlap between "train" and "test"
				testSet = set(allClassified)-set(trainingSet)
				# Print how many were selected for testing
				print(cat + " " + str(len(testSet)) + " of " + str(allClassifiedLen))
				d = testSet
			else:
				# Pint how many were selected for training and how many were force-trained
				print(cat + " " + str(len(trainingSet)) + " of " + str(allClassifiedLen) + " : " + str(forceTrain) + " forcibly trained of " + str(couldForceTrain))
				d = trainingSet
			# Generate the object variables used by the driver based on the sets generated from the above.
			for f in d:
				self.data.append(f[2])
				self.data_ids.append(f[0])
				self.target.append(index)

	def save_data_to_db(self, id, data):
		"""
		Save the given data into the database as a `Guess`
		:param id: The ID of the fragment to update
		:param data: The category of the `Guess` to be set
		"""
		c = self.__conn.cursor()
		c.execute("UPDATE `"+self.Big_Table+"` SET `Guess`=%s WHERE `ID`=%s", (data, id))
		self.__conn.commit()
