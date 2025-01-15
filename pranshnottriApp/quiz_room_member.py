# quiz_room_member.py
'''
	The class QuizRoomMember.
	It encapsulates a quiz room member which is a user who 
	has joined to play quiz/quizzes inside a quiz room.
'''

from datetime import datetime

class QuizRoomMember:
	def __init__(self, member_id_inpt, join_time, u_name, memb_role, memb_score=0, leave_time=None):
		self._member_id = member_id_inpt
		self._member_latest_join_time = join_time
		self._member_user_name = u_name
		self._member_role = memb_role
		self._member_current_total_score = memb_score
		self._member_latest_leave_time = leave_time

	@property
	def member_id(self):
		""""""
		return self._member_id
	@member_id.setter
	def member_id(self, id_inpt):
		try:
			self._member_id = str(id_inpt)
		except ValueError:
			raise ValueError("member_id has to be a string.")
		self._member_id = inpt_id

	@property
	def member_latest_join_time(self):
		""""""
		return self._member_latest_join_time
	@member_latest_join_time.setter
	def member_latest_join_time(self, join_time_inpt):
		try:
			self._member_latest_join_time = datetime(join_time_inpt)
		except ValueError:
			raise ValueError(" member_join_time has to be a datetime object.")
		self._member_latest_join_time =  join_time_inpt

	@property
	def member_user_name(self):
		""""""
		return self._member_user_name
	@member_user_name.setter
	def member_user_name(self, name_inpt):
		try:
			self._member_user_name = str(name_inpt)
		except ValueError:
			raise ValueError("user_name has to be a string.")
		if len(name_inpt) >= 30:
			raise ValueError("user name cannot be greater than length 30")
		self._member_user_name = inpt_name 

	@property
	def member_role(self):
		""""""
		return self._member_role
	@member_role.setter
	def member_role(self, role_inpt):
		try:
			self._member_role = str(role_inpt)
		except ValueError:
			raise ValueError("member_role has to be a string.")
		if role_inpt.lower() != "creator" or role_inpt.lower() != "non-creator":
			raise ValueError("invalid value for member_role provided.")
		self._member_role = role_inpt

	@property
	def member_current_total_score(self):
		""""""
		return self._member_current_total_score
	@member_current_total_score.setter
	def member_current_total_score(self, score_inpt):
		try:
			self._member_current_total_score = int(score_inpt)
		except ValueError:
			raise ValueError("score has to be a integer.")
		self._member_current_total_score = score_inpt

	@property
	def member_latest_leave_time(self):
		""""""
		return self._member_latest_leave_time
	@member_latest_leave_time.setter
	def member_latest_leave_time(self, leave_time_inpt):
		try:
			self._member_latest_leave_time = datetime(leave_time_inpt)
		except ValueError:
			raise ValueError(" member_leave_time has to be a datetime object.")
		self._member_latest_leave_time =  leave_time_inpt