#!/bin/python
import sys

import MySQLdb
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn import metrics
from fetch_article_fragments import dataset
from sklearn.externals import joblib
import os.path

seed = 534654321
model_filename = 'trained.pkl'

categories = ["Not a Source", "Original Reporting", "Primary Source", "Secondary Source", "Quote", "Should Source"]

def train_and_print(limit=10):
	my_train = dataset("train", categories, seed, limit=limit)
	# Train linear SVM model
	text_clf = Pipeline([('vect', CountVectorizer()),
						 ('tfidf', TfidfTransformer()),
						 ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=seed))
						 ])
	_ = text_clf.fit(my_train.data, my_train.target)
	joblib.dump(text_clf, model_filename)

	print("\r\nDone fitting")
	my_test = dataset("test", categories, seed, limit=limit)
	print("Done making test set")
	predicted = text_clf.predict(my_test.data)
	print(metrics.classification_report(my_test.target, predicted, target_names=my_test.target_names))

if len(sys.argv) > 1:
	if sys.argv[1] == "-t":
		if len(sys.argv) > 2:
			train_and_print(int(sys.argv[2]))
		else:
			train_and_print()

	elif sys.argv[1] == "-p":
		if os.path.isfile(model_filename):
			text_clf = joblib.load(model_filename)
			predicted = text_clf.predict([sys.argv[2]])
			print(predicted[0])

	elif sys.argv[1] == "-l":
		conn = MySQLdb.connect(host="localhost", user="root", passwd="", db="newsscraper", charset="utf8")
		Train_Table = dataset.Fragment_Train_Table
		Big_Table = dataset.Big_Table
		c = conn.cursor()
		c.execute("SELECT * FROM `"+Train_Table+"` WHERE `IsSource` > -1")
		trained = c.fetchall()
		for a in trained:
			c.execute("UPDATE `"+Big_Table+"` SET `IsSource`=%s WHERE `ArticleURL`=%s AND `Fragment`=%s",
					  (a[3], a[1], a[2]))
			conn.commit()

	elif sys.argv[1] == "-r":
		if os.path.isfile(model_filename):
			running_set = dataset("run", categories, seed)
			text_clf = joblib.load(model_filename)
			for i, text in enumerate(running_set.data):
				predicted = text_clf.predict([text])
				running_set.save_data_to_db(running_set.data_ids[i], predicted[0])
else:
	print("You must specify a command")
