import MySQLdb
from db_connection import dbConnection
import re
import random

def main():

	quote_regex = r'(\"[^\"]*\")'
	sentence_regex = ur'([\.\?!][\'\"\u2018\u2019\u201c\u201d\)\]]*\s*(?<!\w\.\w.)(?<![A-Z][a-z][a-z]\.)(?<![A-Z][a-z]\.)(?<![A-Z]\.)\s*)'
	#sentence_regex = ur'(.*[\.\?!][\'\"\u2018\u2019\u201c\u201d\)\]]*\s*(?<!\w\.\w.)(?<![A-Z][a-z][a-z]\.)(?<![A-Z][a-z]\.)(?<![A-Z]\.))\s+'

	dbOptions = {'host': 'localhost', 'user': 'root', 'password': '', 'file': 'newsscraper'}
	verify_db(dbOptions)
	db = dbConnection(dbOptions)
	articles = list(db.get_all_article_text())
	random.shuffle(articles)

	for a in articles:
		print "WORKING ON: "+a[0]
		fragments = re.split(sentence_regex, a[1])
		new_fragments = []
		for f in fragments:
			if f is not None:
				f = f.strip()
				if len(f) >= 20:
					# Find delimeter and append it to the end of the sentence
					frag = re.search(sentence_regex, a[1][a[1].find(f):])
					if frag is not None:
						f = f+frag.groups()[0].strip()
					new_fragments.append(f)
		for f in new_fragments:
			is_source = -1
			# Check if fragment is a quote (exclude apostrophes, but include single quotes)
			if re.search(ur'([\"\u201c\u201d])|([^\w][\'\u2018\u2019])|([\'\u2018\u2019][^\w])', f) is not None:
				is_source = 4
			db.save_fragment_to_db(a[0], f, is_source)


def verify_db(options):
	# Verify the database
	conn = MySQLdb.connect(host=options["host"], user=options["user"], passwd=options["password"],
							db=options["file"], charset="utf8")
	c = conn.cursor()
	c.execute("SHOW TABLES")
	tables = c.fetchall()

	create_table = True
	for t in tables:
		if t[0].lower() == dbConnection.Fragment_Table:
			create_table = False

	if create_table:
		# Create Article-Fragments Table
		c.execute('''CREATE TABLE `'''+dbConnection.Fragment_Table+'''` (
						`ID` integer NOT NULL PRIMARY KEY auto_increment,
						`ArticleURL` text NOT NULL,
						`Fragment` text NOT NULL ,
						`IsSource` integer DEFAULT -1,
						`Guess` integer NULL
					);''')
		conn.commit()
	conn.close()

if __name__ == '__main__':
	# Execute the main program
	main()
