import sqlite3


class dbConnection(object):
	def __init__(self, db):
		self.__database_name = db

	def get_all_article_text(self):
		conn = sqlite3.connect(self.__database_name)
		c = conn.cursor()
		c.execute("SELECT `ArticleURL`, `ArticleText` FROM `Articles`")
		ret = c.fetchall()
		conn.close()

		return ret

	def get_fragments(self):
		conn = sqlite3.connect(self.__database_name)
		c = conn.cursor()
		c.execute("SELECT `ID`, `Fragment`, `IsSource` FROM `Article-Fragments` WHERE `IsSource` = -1")
		ret = c.fetchall()
		conn.close()

		return ret

	def save_fragment_to_db(self, article_url, fragment, is_source, ID=None):
		conn = sqlite3.connect(self.__database_name)
		c = conn.cursor()
		if ID is None:
			c.execute("REPLACE INTO `Article-Fragments` (`ArticleURL`, `Fragment`, `IsSource`) VALUES (?,?,?)",
				  [article_url, fragment, is_source])
		else:
			c.execute("UPDATE `Article-Fragments` SET `ID`=?, `IsSource`=? WHERE `ID` =?",
					  [ID, is_source, ID])
		conn.commit()
		conn.close()