'''
	# quiz_question.py

	This file represents a class called as quiz_question.
'''

class QuizQuestion:
	_quiz_question_obj_dict = {}
	def __init__(self, quiz_id_inpt, question_id_inpt, op1_inpt, op2_inpt, op3_inpt, op4_inpt, correct_ans_inpt, question_text_inpt):
		self._quiz_id = quiz_id_inpt
		self._question_id = question_id_inpt
		self._op1 = op1_inpt
		self._op2 = op2_inpt
		self._op3 = op3_inpt
		self._op4 = op4_inpt
		self._correct_ans = correct_ans_inpt
		self._question_text = question_text_inpt


	@property
	def quiz_id(self):
		""""""
		return self._quiz_id
	@quiz_id.setter
	def quiz_id(self, quiz_id_inpt):
		try:
			self._quiz_id = str(quiz_id_inpt)
		except ValueError:
			raise ValueError("quiz_id has to be a string.")
		self._quiz_id =  quiz_id_inpt

	@property
	def question_id(self):
		""""""
		return self._question_id
	@question_id.setter
	def question_id(self, join_time_inpt):
		try:
			self._question_id = str(question_id_inpt)
		except ValueError:
			raise ValueError("question_id has to be a string.")
		self._question_id =  question_id_inpt

	@property
	def op1(self):
		""""""
		return self._op1
	@op1.setter
	def op1(self, join_time_inpt):
		try:
			self._op1 = str(join_time_inpt)
		except ValueError:
			raise ValueError("op1 has to be a string.")
		self._op1 =  join_time_inpt

	@property
	def op2(self):
		""""""
		return self._op2
	@op2.setter
	def op2(self, join_time_inpt):
		try:
			self._op2 = str(join_time_inpt)
		except ValueError:
			raise ValueError("op2 has to be a string.")
		self._op2 =  join_time_inpt

	@property
	def op3(self):
		""""""
		return self._op3
	@op3.setter
	def op3(self, join_time_inpt):
		try:
			self._op3 = str(join_time_inpt)
		except ValueError:
			raise ValueError("op3 has to be a string.")
		self._op3 =  join_time_inpt

	@property
	def op4(self):
		""""""
		return self._op4
	@op4.setter
	def op4(self, join_time_inpt):
		try:
			self._op4 = str(join_time_inpt)
		except ValueError:
			raise ValueError("op4 has to be a string.")
		self._op4 =  join_time_inpt

	@property
	def correct_ans(self):
		""""""
		return self._correct_ans
	@correct_ans.setter
	def correct_ans(self, join_time_inpt):
		try:
			self._correct_ans = str(join_time_inpt)
		except ValueError:
			raise ValueError("correct_ans has to be a string.")
		self._correct_ans =  join_time_inpt

	@property
	def question_text(self):
		""""""
		return self._question_text
	@question_text.setter
	def question_text(self, join_time_inpt):
		try:
			self._question_text = str(join_time_inpt)
		except ValueError:
			raise ValueError("question_text has to be a string.")
		self._question_text =  join_time_inpt