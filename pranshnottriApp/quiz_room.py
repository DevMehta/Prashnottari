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
	def __init__(self, room_id, room_name, members_dict, room_creation_time, room_code, runs_dict_inpt, currnt_run_id_inpt, room_end_time=None):
		# instance attributes	
		self._room_id = room_id
		self._room_name = room_name # user given name
		self._members_dict = members_dict # key memb_id and value as [name, session_id]
		self._room_creation_time = room_creation_time
		self._room_end_time = room_end_time
		self._room_code = room_code
		self._runs_dict = runs_dict_inpt # consist of quiz_run_objs with run_ids as keys
		self._currnt_run_id = currnt_run_id_inpt

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
		self._room_id = room_id_inpt

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
	def members_dict(self):
		return self._members_dict
	@members_dict.setter
	def members_dict(self, members_dict_inpt):
		try:
			self._members_dict = dict(members_lst_dict)
		except ValueError:
			raise ValueError("members_dict has to be of dict type.")
		self._members_dict = members_dict_inpt

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

	@property
	def runs_dict(self):
		return self._runs_dict
	@runs_dict.setter
	def runs_dict(self, runs_dict_inpt):
		try:
			self.runs_dict = dict(runs_dict_inpt)
		except ValueError:
			raise ValueError("runs_dict has to be a dictionary.")
		self._runs_dict = runs_dict_inpt

	@property
	def currnt_run_id(self):
		"""The currnt_run_id is id of current run of a quiz"""
		return self._currnt_run_id
	@currnt_run_id.setter
	def currnt_run_id(self, currnt_run_id_inpt):
		try:
			self._currnt_run_id = str(currnt_run_id_inpt)
		except ValueError:
			raise ValueError("currnt_run_id has to be a string.")
		self._currnt_run_id = currnt_run_id_inpt

	def add_member_to_room(self, memb_name, memb_id, memb_session_id):
		# TO DO: store the name of the member
		# TO DO: store their time of latest join
		join_time = datetime.now()
		# TO DO: store their time of last leaving
		# TO DO: add them to members list
		self._members_dict[memb_id] = [memb_name.lower(), memb_session_id]