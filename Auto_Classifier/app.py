#!/bin/python
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from sklearn.linear_model import SGDClassifier
from sklearn.pipeline import Pipeline
from sklearn import metrics
from fetch_article_fragments import dataset

seed = 534654321

#categories = ['alt.atheism', 'soc.religion.christian','comp.graphics', 'sci.med']
#twenty_train = fetch_20newsgroups(subset='train', categories=categories, shuffle=True, random_state=seed)

#categories = ["Not a Source", "Original Reporting", "Primary Source", "Secondary Source", "Quote", "Should Source"]
categories = ["Not a Source",  "Original Reporting", "Primary Source", "Quote", "Should Source"]
limit = 40

my_train = dataset("train", categories, seed, limit=limit)


# Train linear SVM model
text_clf = Pipeline([('vect', CountVectorizer()),
                          ('tfidf', TfidfTransformer()),
                          ('clf', SGDClassifier(loss='hinge', penalty='l2', alpha=1e-3, n_iter=5, random_state=seed))
						 ])
#_ = text_clf.fit(twenty_train.data, twenty_train.target)
_ = text_clf.fit(my_train.data, my_train.target)

print "\r\nDone fitting"
my_test = dataset("test", categories, seed, limit=limit)
print "Done making test set"

#twenty_test = fetch_20newsgroups(subset='test', categories=categories, shuffle=True, random_state=seed)
#predicted = text_clf.predict(twenty_test.data)

predicted = text_clf.predict(my_test.data)
print(metrics.classification_report(my_test.target, predicted, target_names=my_test.target_names))
#print(metrics.classification_report(twenty_test.target, predicted, target_names=twenty_test.target_names))
