import MySQLdb
from warnings import filterwarnings


class dbConnection(object):
	conn = None

	def __init__(self, options):
		filterwarnings('ignore', category=MySQLdb.Warning)
		self.conn = MySQLdb.connect(host=options["host"],user=options["user"],passwd=options["password"],
									db=options["file"],charset="utf8")

	def get_all_article_text(self):
		c = self.conn.cursor()
		c.execute("SELECT `ArticleURL`, `ArticleText` FROM `Articles`")
		ret = c.fetchall()

		return ret

	def get_fragments(self):
		c = self.conn.cursor()
		c.execute("SELECT `ID`, `Fragment`, `IsSource` FROM `Article-Fragments` WHERE `IsSource` = -1")
		ret = c.fetchall()

		return ret

	def save_fragment_to_db(self, article_url, fragment, is_source, ID=None):
		c = self.conn.cursor()
		if ID is None:
			c.execute("INSERT INTO `Article-Fragments` (`ArticleURL`, `Fragment`, `IsSource`) VALUES (%s,%s,%s)",
					  (article_url, fragment, is_source))
		else:
			c.execute("UPDATE `Article-Fragments` SET `ID`=%s, `IsSource`=%s WHERE `ID` =%s",
					  (ID, is_source, ID))
		self.conn.commit()