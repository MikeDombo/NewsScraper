import sys
import sqlite3
from db_connection import dbConnection
import re
import unidecode


def command_error_exit(msg):
	print(msg)
	print_full_help()
	exit(64)


def print_full_help():
	print("Usage: \"python app.py [options]\" With the following options.\r\n")
	print("-f <file path> \t| Specify path of database file to use.")
	print("-h \t| Prints this help message.\r\n")


def main():
	database_filename = 'news.db'

	quote_regex = r'(\"[^\"]*\")'
	sentence_regex = r'[\.\?!]\s+(\"[A-Z][^\"]*[\.\?!]+\")|[\.\?!][\'\"\)\]]*\s*(?<!\w\.\w.)(?<![A-Z][a-z][a-z]\.)(?<![A-Z][a-z]\.)(?<![A-Z]\.)\s+'

	# Parse Command Line Arguments
	if len(sys.argv) > 1:
		args = sys.argv
		recognized_args = ["-f", "-h"]
		del args[0]  # Remove script name from arguments

		if '-h' in args:
			print_full_help()
			exit(0)
		if '-f' in args:
			filename = args.index("-f")
			if len(args) <= filename+1 or args[filename+1] in recognized_args:
				command_error_exit("Database filename must be specified!\r\n")
			database_filename = args[filename + 1]

		if not any(a in args for a in recognized_args):
			command_error_exit("Unrecognized argument!\r\n")
	else:
		print("Running with defaults\r\n")

	verify_db(database_filename)
	db = dbConnection(database_filename)
	articles = db.get_all_article_text()

	new_fragments = []
	for i, a in enumerate(articles):
		print "WORKING ON: "+a[0]
		fragments = re.split(sentence_regex, unidecode.unidecode(a[1]))
		for f in fragments:
			if f is not None:
				f = f.strip()
				if len(f) >= 20:
					new_fragments.append(f)
		for f in new_fragments:
			db.save_fragment_to_db(a[0], f, -1)

def verify_db(file):
	# Verify the database
	conn = sqlite3.connect(file)
	c = conn.cursor()
	c.execute("""SELECT name FROM sqlite_master WHERE type='table';""")
	tables = c.fetchall()

	create_table = True
	for t in tables:
		if t[0] == "Article-Fragments":
			create_table = False

	if create_table:
		# Create Article-Fragments Table
		c.execute('''CREATE TABLE `Article-Fragments` (
						`ID` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
						`ArticleURL` TEXT,
						`Fragment` TEXT UNIQUE,
						`IsSource` INTEGER
					);''')
		conn.commit()
	conn.close()

if __name__ == '__main__':
	# Execute the main program
	main()
