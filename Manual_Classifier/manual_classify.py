from Tkinter import *
from db_connection import dbConnection
import pygubu

class App:
	database_filename = '../news-old-1.db'
	fragments = []
	current_fragment = 0

	def __init__(self, master):
		self.db = dbConnection(self.database_filename)

		self.builder = builder = pygubu.Builder()
		# 2: Load an ui file
		builder.add_from_file('myUI.ui')
		# 3: Create the widget using a master as parent
		self.mainwindow = builder.get_object('Toplevel_1', master)

		builder.connect_callbacks(self)
		master.bind_all('o', lambda e: self.original_push())
		master.bind_all('p', lambda e: self.primary_push())
		master.bind_all('s', lambda e: self.secondary_push())
		master.bind_all('q', lambda e: self.quote_push())
		master.bind_all('n', lambda e: self.not_push())
		master.bind_all('k', lambda e: self.skip_push())

		self.mainwindow.master.title("Classify Sentences")

		self.fragments = self.db.get_fragments()
		self.next_message(-2)

		master.protocol("WM_DELETE_WINDOW", self.on_close_window)

	def on_close_window(self, event=None):
		# Call destroy on toplevel to finish program
		print("You Categorized or Skipped " + str(self.current_fragment-1) + " Fragments!")
		self.mainwindow.master.destroy()

	def next_message(self, result):
		self.builder.get_object('Message_1')["text"] = self.fragments[self.current_fragment][1]
		if result > -2:
			my_fragment = self.fragments[self.current_fragment - 1]
			self.db.save_fragment_to_db(None, my_fragment[1], result, my_fragment[0])
		self.current_fragment += 1
		
	def original_push(self):
		self.next_message(1)

	def primary_push(self):
		self.next_message(2)

	def secondary_push(self):
		self.next_message(3)

	def quote_push(self):
		self.next_message(4)

	def not_push(self):
		self.next_message(0)

	def skip_push(self):
		self.next_message(-1)

root = Tk()

app = App(root)

root.mainloop()
