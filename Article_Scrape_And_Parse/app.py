import sys
from datetime import datetime as dt
from datetime import timedelta
import time
import Scrapers
from DBConnection import DBConnection
import multiprocessing


def command_error_exit(msg):
	print(msg)
	print_full_help()
	exit(64)


def print_full_help():
	print("Usage: \"python app.py [options]\" With the following options.\r\n")
	print("-f <file path> \t| Specify path of database file to use.")
	print("-q \t| Only adds articles from each publisher to the queue, but does not download and parse them.")
	print("-d \t| Redownloads and reparses all articles in queue, even those that have been downloaded and parsed before. -r is implicit.")
	print("-r \t| Reparses all articles in queue (without redownloading), even those that have been downloaded and parsed before.")
	print("-n \t| Run without saving anything to a database.")
	print("-m \t| Run without multiprocessing.")
	print("-u <url> \t| Specify a URL to parse before the queue starts")
	print("-h \t| Prints this help message.\r\n")


def main():
	database_filename = 'news.db'

	one_url = None
	no_queuing = False
	queue_only = False
	reparse = False
	redownload = False
	no_db = False
	run_multiprocessing = True

	# Parse Command Line Arguments
	if len(sys.argv) > 1:
		args = sys.argv
		recognized_args = ["-q", "-r", "-d", "-n", "-f", "-m", "-u", "-s", "-h"]
		del args[0]  # Remove script name from arguments

		if '-h' in args:
			print_full_help()
			exit(0)
		if '-q' in args:
			queue_only = True
			print("Running in queue only mode")
		if '-n' in args:
			no_db = True
			print("Running with no database. No data will be stored!")
		if '-s' in args:
			no_queuing = True
			print("Running without first queuing!")
		if '-r' in args:
			reparse = True
			print("Running in reparse mode")
		if '-m' in args:
			run_multiprocessing = False
		if '-d' in args:
			reparse = True
			redownload = True
			print("Running in redownload and reparse mode")
		if '-f' in args:
			filename = args.index("-f")
			if len(args) <= filename+1 or args[filename+1] in recognized_args:
				command_error_exit("Database filename must be specified!\r\n")
			database_filename = args[filename + 1]
		if '-u' in args:
			url = args.index("-u")
			if len(args) <= url+1 or args[url+1] in recognized_args:
				command_error_exit("URL must be specified!\r\n")
			one_url = args[url + 1]

		if not any(a in args for a in recognized_args):
			command_error_exit("Unrecognized argument!\r\n")
	else:
		print("Running with defaults\r\n")

	db_options = False
	db = False
	# If we are using a database, then verify or create it
	if not no_db:
		if '-f' in sys.argv:
			db_options = {"db": "sqlite", "file": database_filename}
			db = DBConnection(db_options)
			print("Running with database: " + database_filename)
		else:
			db_options = {"db": "mysql", "file": "newsscraper", "user": "root", "password": "", "host": "localhost"}
			db = DBConnection(db_options)
			print("Running with MySQL database")
	number_cores = multiprocessing.cpu_count()
	if not no_queuing:
		print("Queuing Today's Articles")
		pool = multiprocessing.Pool(processes=number_cores)

		from Router import Router
		my_router = Router()
		if run_multiprocessing:
			r = [pool.apply_async(make_queue, args=(s, no_db, db_options)) for s in my_router.get_scrapers()]
			q = [p.get() for p in r]
			pool.terminate()
		else:
			q = []
			for s in my_router.get_scrapers():
				q += make_queue(s, no_db, db_options)

		if queue_only:
			print("Queuing Complete With " + str(len(q)) + " Articles")
			return

	# If we are running with a database, overwrite the local q with one from the database which will already contain q
	if not no_db:
		q = db.read_article_queue()

	print("Queuing Complete With " + str(len(q)) + " Articles")
	print("Beginning Scraping and Parsing")
	print("==============================\r\n")

	if one_url is not None:
		print("Starting with user-specified URL")
		# Execute a single article with no sleeping, and reparse implicitly set to True
		# because if a user gives us a URL, they want it parsed, even without the -r flag
		execute_article_parse(one_url, db_options, no_db, True, True, False)
		print("Continuing with Queued Articles\r\n")

	if run_multiprocessing:
		pool = multiprocessing.Pool(processes=number_cores)
		r = [pool.apply_async(execute_article_parse, args=(a[1], db_options, no_db, reparse, redownload, True)) for a in q]
		r = [p.get() for p in r]
		pool.terminate()
	else:
		for a in q:
			execute_article_parse(a[1], db_options, no_db, reparse, redownload, True)

	print("\r\n==============================")
	print("Program Complete!")


def make_queue(s, no_db, db_options):
	db = DBConnection(db_options)
	q = []
	# Get today's articles
	articles = s.get_article_list()
	# Get articles from yesterday, if possible
	try:
		articles = articles + s.get_article_list(dt.today() - timedelta(1))
	except ValueError:
		pass
	for a in articles:
		q.append([0, a, dt.now()])
	if not no_db:
		db.queue_article_list(articles)
	return q


def execute_article_parse(url, db_options, no_db, reparse, redownload, sleep=True):
	# Basic setup of objects
	db = DBConnection(db_options)
	from Router import Router
	my_router = Router()
	sc = Scrapers.Scrapers()
	sc.url = url
	sc.my_parser = my_router.get_parsers_by_url(sc.url)
	if sc.my_parser is None:
		print "Could not find parser for "+sc.url
		return

	# Check if we should download and parse the article or not
	if no_db or reparse or not db.is_already_analyzed(sc.url):
		if not no_db and db.is_already_analyzed(sc.url):
			print("Reparsing: " + sc.url)
		else:
			print(sc.url)
		if (sleep and redownload) or (sleep and not (redownload or reparse)):
			time.sleep(1)
		try:
			if redownload or no_db or not db.is_already_analyzed(sc.url):
				sc.get_article_data()
			else:
				sc.get_article_data(db.get_article_html_from_db(url))
			if not no_db:
				db.save_data_to_db(sc)
		except RuntimeError as e:
			print "Runtime Error: "+e.message

if __name__ == '__main__':
	# Execute the main program
	main()
