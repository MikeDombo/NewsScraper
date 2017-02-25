#!/bin/python
import sys
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
limit = 10

def train_and_print():
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
		train_and_print()
	elif sys.argv[1] == "-p":
		if os.path.isfile(model_filename):
			text_clf = joblib.load(model_filename)
			predicted = text_clf.predict([sys.argv[2]])
			print(predicted[0])
else:
	print("You must specify a command")
