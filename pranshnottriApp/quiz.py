'''
	# quiz.py

	This file represents a class called as quiz.
'''

class quiz:
	def __init__(self, ):
		# instance attributes	
		self._quiz_id
		self._quiz_name
		self._category
		self.quiz_creation_date
		self._number_of_times_played
		self._question_ans_dict

	@property
	def room_id(self):
		"""The room_id property uniquely identifies a room."""
		return self._room_id
	@room_id.setter
	def room_id(self, room_id_inpt):
		try:
			self._room_id = str(room_id_inpt)
		except ValueError:
			raise ValueError("room_id has to be a string.")
		if len(room_id_inpt) != 10:
			raise ValueError("room_id has to be a string of length 10")
		self._room_id = room_id