import sys
import sqlite3
from datetime import datetime as dt
import time
import Scrapers


def command_error_exit(msg):
	print(msg)
	print_full_help()
	exit(64)


def print_full_help():
	print("Usage: \"python app.py [options]\" With the following options.\r\n")
	print("-f <file path> \t| Specify path of database file to use.")
	print("-q \t| Only adds articles from each publisher to the queue, but does not download and parse them.")
	print("-r \t| Reparses all articles in queue, even those that have been downloaded and parsed before.")
	print("-n \t| Run without saving anything to a database.")
	print("-h \t| Prints this help message.\r\n")


def main():
	NewsDatabase = 'news.db'

	queueOnly = False
	reparse = False
	noDB = False

	# Parse Command Line Arguments
	if len(sys.argv) > 1:
		args = sys.argv
		recognizedArgs = ["-q", "-r", "-n", "-f", "-h"]
		del args[0]  # Remove script name from arguments

		if '-h' in args:
			print_full_help()
			exit(0)
		if '-q' in args:
			queueOnly = True
			print("Running in queue only mode")
		if '-n' in args:
			noDB = True
			print("Running with no database. No data will be stored!")
		if '-r' in args:
			reparse = True
			print("Running in reparse mode")
		if '-f' in args:
			filename = args.index("-f")
			if len(args) <= filename+1 or args[filename+1] in recognizedArgs:
				command_error_exit("Database filename must be specified!\r\n")
			NewsDatabase = args[filename+1]

		if not any(a in args for a in recognizedArgs):
			command_error_exit("Unrecognized argument!\r\n")
	else:
		print("Running with defaults\r\n")

	# If we are using a database, then verify or create it
	if not noDB:
		verify_db(NewsDatabase)
		print("Running with database: " + NewsDatabase)

	print("Queuing Today's Articles")

	q = []
	from Router import Router
	my_router = Router(NewsDatabase)
	i = 0
	for s in my_router.get_scrapers():
		articles = s.get_article_list()
		for a in articles:
			q.append([i, a, dt.now()])
			i += 1
		if not noDB:
			s.queue_article_list(articles)

	print("Queuing Complete With " + str(i) + " Articles")
	if queueOnly:
		return

	sc = Scrapers.Scrapers(NewsDatabase)
	# If we are running with a database, overwrite the local q with one from the database
	if not noDB:
		q = sc.read_article_queue()

	print("Beginning Scraping and Parsing")
	print("==============================\r\n")

	for a in q:
		sc = Scrapers.Scrapers(NewsDatabase)
		sc.url = a[1]
		sc.myParser = my_router.get_parsers_by_url(sc.url)
		if noDB or reparse or not sc.is_already_analyzed():
			if not noDB and sc.is_already_analyzed():
				print("Reparsing: " + sc.url)
			else:
				print(sc.url)
			time.sleep(1)
			sc.get_article_data()
			if not noDB:
				sc.save_data_to_db()

	print("\r\n==============================")
	print("Program Complete!")


def is_sqlite3(filename):
	from os.path import isfile, getsize
	if not isfile(filename):
		return False
	if getsize(filename) < 100: # SQLite database file header is 100 bytes
		return False
	with open(filename, 'rb') as fd:
		header = fd.read(100)
	return header[:16] == 'SQLite format 3\x00'


def verify_db(file):
	# Verify the database
	if not is_sqlite3(file):
		conn = sqlite3.connect(file)
		c = conn.cursor()
		# Create Article Table
		c.execute('''CREATE TABLE `Articles` (
						`ID` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
						`ArticleURL` TEXT UNIQUE,
						`Headline` TEXT,
						`Subtitle` TEXT,
						`Author` TEXT,
						`Publisher` TEXT,
						`PublishDate` TEXT,
						`ArticleText` TEXT,
						`ArticleHTML` TEXT,
						`ArticleSources` TEXT,
						`RetrievalDate` TEXT,
						`ArticleSection` TEXT,
						`IsPrimarySource` INTEGER,
						`HasUpdates` INTEGER,
						`HasNotes` INTEGER
					);''')
		# Create Queue Table
		c.execute('''CREATE TABLE `Queue` (
						`ID` INTEGER PRIMARY KEY AUTOINCREMENT UNIQUE,
						`url` TEXT UNIQUE,
						`dateAdded` TEXT
					);''')
		conn.commit()

if __name__ == '__main__':
	# Execute the main program
	main()
