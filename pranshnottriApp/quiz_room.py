# quiz_room.py
'''
	The class QuizRoom.
	It encapsulates a quiz room which is a group of users wanting to play
	a quizzes simultaneously with each other.
'''

from datetime import datetime
import random
from string import ascii_uppercase
from flask import session

class QuizRoom:
	
	def __init__(self, room_id, room_name, members_lst, room_creation_time, room_code, room_end_time=None):
		# instance attributes	
		self._room_id = room_id
		self._room_name = room_name # user given name
		self._members_lst = members_lst
		self._room_creation_time = room_creation_time
		self._room_end_time = room_end_time
		self._room_code = room_code

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

	@property
	def room_name(self):
		"""The room_name is the room onwers given name for the room to be displayed"""
		return self._room_id
	@room_name.setter
	def room_name(self, inpt_name):
		try:
			self._room_name = str(inpt_name)
		except ValueError:
			raise ValueError("room_name has to be a string.")
		if len(inpt_name) >= 30:
			raise ValueError("room_name cannot be greater than 30 in length")
		self._room_name = inpt_name

	@property
	def members_lst(self):
		return self._members_lst
	@members_lst.setter
	def members_lst(self, members_lst_inpt):
		try:
			self._members_lst = list(members_lst_inpt)
		except ValueError:
			raise ValueError("members_lst has to be of list type.")
		self._members_lst = members_lst_inpt

	@property
	def room_creation_time(self):
		"""This property identifies the time at which the room was created."""
		return self._room_creation_time
	@room_creation_time.setter
	def room_creation_time(self, inpt_time):
		if isinstance(inpt_time, datetime) is False:
			raise ValueError("room_creation_time has to be a python datetime object.")
		self._room_creation_time = inpt_time

	@property
	def room_end_time(self):
		"""This property identifies the time at which the room was ended."""
		return self._room_end_time
	@room_end_time.setter
	def room_end_time(self, inpt_time):
		if isinstance(inpt_time, datetime) is False:
			raise ValueError("room_end_time has to be a python datetime object.")
		self._room_end_time = inpt_time

	@property
	def room_code(self):
		"""This property stores the unique(among currently active rooms) code correpoding to the room."""
		return self._room_code
	@room_code.setter
	def room_code(self, code):
		try:
			self._room_code = str(code)
		except ValueError:
			raise ValueError("room_code has to be a string.")
		if len(code) != 5:
			raise ValueError("room_code has to be string of length 5.")
		self._room_code = code

	def add_member_to_room(self):
		# TO DO: store the name of the member
		name = session['user_name']
		# TO DO: store their time of latest join
		join_time = datetime.now()
		# TO DO: store their time of last leaving
		# TO DO: add them to members list
		self._members_lst.append(name.lower())