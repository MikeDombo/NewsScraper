class Article(object):
	url = ""
	title = ""
	subtitle = ""
	author = ""
	publisher = ""
	publish_date = ""
	article_text = u""
	full_html = ""
	sources = []
	text_sources = []
	fetch_date = ""
	grade_level = 0
	updates = False
	editor_notes = False
	corrections = False
	section = []

	def __init__(self):
		pass
