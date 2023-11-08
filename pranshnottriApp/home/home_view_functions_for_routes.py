from flask import render_template, request, session, redirect, url_for, flash, redirect
from . import home_blueprint
from .. quiz_room_manager import QuizRoomManager
from .. quiz_room import QuizRoom
from .. quiz_room_member import QuizRoomMember
from .. quiz import Quiz
from .. quiz_question import QuizQuestion
from datetime import datetime
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from .. db import get_db_connection, close_db_connection


quiz_room_manager_obj = QuizRoomManager()

@home_blueprint.route('/', methods=['GET', 'POST'])
def home_view_function():
	if request.method == 'POST':
		inpt_user_name = str(request.form.get("user-name-inpt")).strip()
		disp_room_name = str(request.form.get("room-name-inpt")).strip()
		inpt_code = str(request.form.get("code-inpt")).strip()
		join_option = request.form.get("join-btn", False)
		create_option = request.form.get("create-btn", False)
		create_quiz_option = request.form.get("create-quiz-btn", False)

		if create_quiz_option != False:
			return redirect(url_for('create_quiz_blueprint.create_quiz_function'))

		# check if user name has been entered or not
		if inpt_user_name == "":
			flash("Enter a user name.")
			return render_template("home.html")

		session['user_name'] = inpt_user_name

		# Create the member object
		memb_name = inpt_user_name
		memb_join_time = datetime.now()
		memb_role = ""
		if create_option == False:
			memb_role = "non-creator"
			session["user_role"] = "non-creator"
		else:
			memb_role = "creator"
			session["user_role"] = "creator"

		memb_obj = QuizRoomMember(memb_join_time, memb_name, memb_role)


		''' handle new room creation '''
		if create_option != False:
			# check if room name has been entered or not
			if disp_room_name == "":
				flash("Enter a room name.")
				return render_template("home.html")
			session['disp_room_name'] = disp_room_name
			quiz_room_obj = quiz_room_manager_obj.before_first_join_processing()
			quiz_room_manager_obj.add_quiz_room_obj(quiz_room_obj)
			print(quiz_room_manager_obj._room_codes)
			print(quiz_room_manager_obj._rooms_current_count)
			return redirect(url_for('home_blueprint.quiz_room_view_function'))
			
		''' handle joining to an existing room '''	
		if join_option != False:
			# Check if room code is an empty string
			if inpt_code == "":
				flash("Enter a room code.")
				return render_template("home.html")
			# check if the entered room code is valid or not
			if inpt_code not in quiz_room_manager_obj._room_codes:
				# return an error that invalid quiz room code entered
				flash("Invalid room code entered.")
				print(quiz_room_manager_obj._room_codes)
				return render_template("home.html", name=inpt_user_name)
			else:
				session['room_code'] = inpt_code
				quiz_room_obj = quiz_room_manager_obj._quiz_room_obj_dict[session['room_code']]
				if inpt_user_name.lower() in quiz_room_obj._members_lst:
					flash("The user name has been taken by other member of the room, Enter another")
					print(quiz_room_obj._members_lst)
					print(quiz_room_manager_obj._room_codes)
					return render_template("home.html", name=inpt_user_name)
				else:
					session['disp_room_name'] = quiz_room_obj._room_name
					quiz_room_obj.add_member_to_room()
					print(quiz_room_obj._members_lst)
					print(quiz_room_manager_obj._room_codes)
				return redirect(url_for('home_blueprint.quiz_room_view_function'))

		print(quiz_room_manager_obj._room_codes)		
	return render_template("home.html")

@home_blueprint.route('/quiz_room', methods=['GET', 'POST'])
def quiz_room_view_function():
	# show a list of existing quizzes to
	if request.method == 'POST':
		inpt_quiz_id = '1001'
		# get the quiz from the db
		conn = get_db_connection()
		get_quiz_query = "SELECT * FROM quiz WHERE quiz_id = ( %s );" % (inpt_quiz_id)
		sql_rest = None
		try:
			sql_rest = conn.execute(text(get_quiz_query))
		except SQLAlchemyError as e:
			print(e)
			
		row = sql_rest.fetchone()
		qid = row[0]
		qname = row[1]
		qcateg = row[2]
		qcdate = row[3]
		qntmes_played = row[4]
		session['quiz_name'] = qname
		session['quiz_id'] = qid
		conn.commit()
		
		# make the quiz object
		quiz_obj = Quiz(qid, qname, qcateg, qcdate, qntmes_played)
		Quiz._quiz_obj_dict['1001'] = quiz_obj
		print(quiz_obj.__str__())
		
		# get quiz questions
		get_quiz_ques_query = "SELECT * FROM quiz_question WHERE quiz_id = ( %s );" % (inpt_quiz_id)
		sql_rest2 = None
		try:
			sql_rest2 = conn.execute(text(get_quiz_ques_query))
		except SQLAlchemyError as e:
			print(e)

		questions_recd = sql_rest2.fetchall()
		ques_lst = []
		for recd in questions_recd:
			print(recd)
			q_id = str(recd[0])
			ques_id = str(recd[1])
			op1 = recd[2]
			op2 = recd[3]
			op3 = recd[4]
			op4 = recd[5]
			correct_ans = recd[6]
			ques_txt = recd[7]
			quiz_ques_obj = QuizQuestion(q_id, ques_id, op1, op2, op3, op4, correct_ans, ques_txt)
			ques_lst.append(quiz_ques_obj)

		QuizQuestion._quiz_question_obj_dict['1001'] = ques_lst

		close_db_connection()

	return render_template("room.html")