'''
	# quiz.py

	This file represents a class called as quiz.
'''

from datetime import datetime

class Quiz:
	_quiz_obj_dict = {}
	
	def __init__(self, quiz_id, quiz_name, quiz_category, quiz_creation_date, number_of_times_played):
		# instance attributes	
		self._quiz_id = quiz_id
		self._quiz_name = quiz_name
		self._quiz_category = quiz_category
		self._quiz_creation_date = quiz_creation_date
		self._number_of_times_played = number_of_times_played

	@property
	def quiz_id(self):
		"""The quiz_id property uniquely identifies a quiz."""
		return self._quiz_id
	@quiz_id.setter
	def quiz_id(self, quiz_id_inpt):
		try:
			self._quiz_id = str(quiz_id_inpt)
		except ValueError:
			raise ValueError("quiz_id has to be a string.")
		self._quiz_id = quiz_id_inpt
	
	@property
	def quiz_name(self):
		return self._quiz_name
	@quiz_name.setter
	def quiz_name(self, quiz_name_inpt):
		try:
			self._quiz_name = str(quiz_name_inpt)
		except ValueError:
			raise ValueError("quiz_name has to be a string.")
		self._quiz_name = quiz_name_inpt

	@property
	def quiz_category(self):
		return self._quiz_category
	@quiz_category.setter
	def quiz_category(self, quiz_category_inpt):
		try:
			self._quiz_category = str(quiz_category_inpt)
		except ValueError:
			raise ValueError("quiz_category has to be of datetime type.")
		self._quiz_category = quiz_category_inpt
	
	@property
	def quiz_creation_date(self):
		return self._quiz_creation_date
	@quiz_creation_date.setter
	def quiz_creation_date(self, quiz_creation_date_inpt):
		try:
			self._quiz_creation_date = datetime(quiz_creation_date_inpt)
		except ValueError:
			raise ValueError("quiz_creation_date has to be of datetime type.")
		self._quiz_creation_date = quiz_creation_date_inpt
			

	@property
	def number_of_times_played(self):
		return self._number_of_times_played
	@number_of_times_played.setter
	def number_of_times_played(self, number_of_times_played_inpt):
		try:
			self._number_of_times_played = int(number_of_times_played_inpt)
		except ValueError:
			raise ValueError("number_of_times_played has to be a integer.")
		self._number_of_times_played = number_of_times_played_inpt