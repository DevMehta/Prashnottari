'''
	# quiz_run.py

	This file represents a class called as quiz_run.
	This class encapsulates the attributes and methods related to a specific run of a quiz
'''
from datetime import datetime
from sortedcontainers import SortedDict

class MemberStats:
	def __init__(self, member_id_inpt, member_total_score_inpt, member_per_ques_score_inpt):
		self._member_id = member_id_inpt
		self._member_total_score = member_total_score_inpt # an int 
		self._member_per_ques_score_dict = member_per_ques_score_inpt # a dict with quesid. & score	

	@property
	def member_id(self):
		return self._member_id
	@member_id.setter
	def member_id(self, member_id_inpt):
		try:
			self._member_id = str(member_id_inpt)
		except ValueError:
			raise ValueError("member_id has to be a string.")
		self._member_id = member_id_inpt

	@property
	def member_total_score(self):
		return self._member_total_score
	@member_total_score.setter
	def member_total_score(self, member_total_score_inpt):
		try:
			self._member_total_score = int(member_total_score_inpt)
		except ValueError:
			raise ValueError("member_total_score has to be a int.")
		self._member_total_score = member_total_score_inpt

	@property
	def member_per_score_dict(self):
		return self._member_per_score_dict
	@member_per_score_dict.setter
	def member_per_score_dict(self, member_per_score_dict_inpt):
		try:
			self._member_per_score_dict = dict(member_per_score_dict_inpt)
		except ValueError:
			raise ValueError("member_per_score_dict has to be a dict.")
		self._member_per_score_dict = member_per_score_dict_inpt

class QuizRun:
	def __init__(self, quiz_run_id_inpt, quiz_run_start_time_inpt, quiz_leaderboard_inpt, memb_stats_obj_dict_inpt, memb_ques_show_dict_inpt, quiz_run_end_time_inpt=None):
		self._quiz_run_id = quiz_run_id_inpt
		self._run_start_time = quiz_run_start_time_inpt
		self._run_end_time = quiz_run_end_time_inpt
		self._leaderboard = quiz_leaderboard_inpt # a sorteddict from sortedcontainers library
		self._member_stats_obj_dict = memb_stats_obj_dict_inpt # a dict of MemberStats class objects with memb_id as key
		self._member_ques_show_dict = memb_ques_show_dict_inpt	# a dict with key as member_ids and values as a set which contains the question ids showed so far

	@property
	def quiz_run_id(self):
		return self._quiz_run_id
	@quiz_run_id.setter
	def quiz_run_id(self, quiz_run_id_inpt):
		try:
			self._quiz_run_id = str(quiz_run_id_inpt)
		except ValueError:
			raise ValueError("quiz_run_id has to be a string.")
		self._quiz_run_id = quiz_run_id_inpt	

	@property
	def run_start_time(self):
		return self._run_start_time
	@run_start_time.setter
	def run_start_time(self, run_start_time_inpt):
		try:
			self._run_start_time = datetime(run_start_time_inpt)
		except ValueError:
			raise ValueError("run_start_time has to be a datetime.")
		self._run_start_time = run_start_time_inpt

	@property
	def run_end_time(self):
		return self._run_end_time
	@run_end_time.setter
	def run_end_time(self, run_end_time_inpt):
		try:
			self._run_end_time = datetime(run_end_time_inpt)
		except ValueError:
			raise ValueError("run_end_time has to be a datetime.")
		self._run_end_time = run_end_time_inpt

	@property
	def leaderboard(self):
		return self._leaderboard
	@leaderboard.setter
	def leaderboard(self, leaderboard_inpt):
		try:
			self._leaderboard = SortedDict(leaderboard_inpt)
		except ValueError:
			raise ValueError("leaderboard has to be a SortedDict.")
		self._leaderboard = leaderboard_inpt

	@property
	def member_stats_obj_dict(self):
		return self._member_stats_obj_dict
	@member_stats_obj_dict.setter
	def member_stats_obj_dict(self, member_stats_obj_dict_inpt):
		try:
			self._member_stats_obj_dict = dict(member_stats_obj_dict_inpt)
		except ValueError:
			raise ValueError("member_stats_obj_dict has to be a dict.")
		self._member_stats_obj_dict = member_stats_obj_dict_inpt

	@property
	def member_ques_show_dict(self):
		return self._member_ques_show_dict
	@member_ques_show_dict.setter
	def member_ques_show_dict(self, member_ques_show_dict_inpt):
		try:
			self._member_ques_show_dict = dict(member_ques_show_dict_inpt)
		except ValueError:
			raise ValueError("member_ques_show_dict has to be a dict.")
		self._member_ques_show_dict = member_ques_show_dict_inpt