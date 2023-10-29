'''
	# quiz_room_manager.py
	encapsulates all the functionality related to a class called QuizRoomManager
	QuizRoomManager: manages all the functions realted to before join preprocessing, join, end etc.
	of quiz rooms
	Note: Creation of rooms is not required since a room is assigned to all clients when they connect,
	named with session_id of the connection
'''

from flask import session
from . quiz_room import QuizRoom
import random
from string import ascii_uppercase
from datetime import datetime

class QuizRoomManager:
	# Class attributes
	_rooms_current_count = 0 # will keep the count of number of currently active quiz rooms
	# TO DO: to take this value from the database at the time of app start
	# TO DO: to update thos value to the DB at the end or within some time frame
	_rooms_overall_count = 0 # will keep the count of number of quiz rooms which have been active ever
	_room_codes = set() # a dictonary which keeps all the quiz_room codes which are currently in use
	
	_quiz_room_obj_dict = {}

	@classmethod
	def set_current_room_cnt(cls, new_cnt):
		cls._rooms_current_count = new_cnt

	@classmethod
	def set_overall_room_cnt(cls, new_cnt):
		cls._rooms_overall_count = new_cnt

	@classmethod	
	def generate_unique_room_code(cls, length):
	    while True:
	        generated_code = ""
	        for i in range(length):
	            generated_code += random.choice(ascii_uppercase)

	        # checking uniqueness of generated code through a _room_codes set
	        if generated_code not in QuizRoomManager._room_codes:
	            break

	    return generated_code

	@classmethod
	def add_quiz_room_obj(cls, obj):
		cls._quiz_room_obj_dict[session['room_code']] = obj

	def before_first_join_processing(self):
		# increment the count of currently active quiz rooms  
		QuizRoomManager.set_current_room_cnt(QuizRoomManager._rooms_current_count + 1)

		'''
			Creating a new QuizRoom object by passing the required
			arguments and preparing the arguments before passing 
		'''

		# assign a unique quiz room id
		QuizRoomManager.set_overall_room_cnt(QuizRoomManager._rooms_overall_count + 1)
		num_of_prefix_0_in_id = 10 - len(str(QuizRoomManager._rooms_overall_count))
		prefix_str = ""
		for i in range(num_of_prefix_0_in_id):
			prefix_str = prefix_str.join("0")
		new_room_id = prefix_str.join(str(QuizRoomManager._rooms_overall_count))

		# user input room name to be displayed
		room_name = session['disp_room_name']

		# generate new unique code
		new_code = QuizRoomManager.generate_unique_room_code(5)
		
		# store the creation time and date of the quiz
		quiz_room_creation_datetime = datetime.now()
		
		# add the room owner to the list of members
		member_list = []
		member_list.append(session['user_name'].lower())
		session["room_code"] = new_code
		
		print(new_code)
		new_room = QuizRoom(new_room_id, room_name, member_list, quiz_room_creation_datetime, new_code)
		QuizRoomManager._room_codes.add(new_room.room_code)

		return new_room # returns the newly created quiz room object

	def after_leave_processing():
		# TO DO: decrement the count of currently active quiz rooms
		# TO DO: to store the quizRoom end time & date
		pass