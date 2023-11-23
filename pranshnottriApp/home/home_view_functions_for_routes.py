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
import uuid

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
        memb_session_id = None

        # Create the member object
        memb_id = str(uuid.uuid4())
        session['memb_id'] = memb_id
        memb_id = str(memb_id)
        memb_name = inpt_user_name
        memb_join_time = datetime.now()
        memb_role = ""
        if create_option == False:
            memb_role = "non-creator"
            session["user_role"] = "non-creator"
        else:
            memb_role = "creator"
            session["user_role"] = "creator"

        memb_obj = QuizRoomMember(memb_id, memb_join_time, memb_name, memb_role)

        ''' handle new room creation '''
        if create_option != False:
            # check if room name has been entered or not
            if disp_room_name == "":
                flash("Enter a room name.")
                return render_template("home.html")
            session['disp_room_name'] = disp_room_name
            quiz_room_obj = quiz_room_manager_obj.before_first_join_processing(memb_id, memb_session_id)
            quiz_room_manager_obj.add_quiz_room_obj(quiz_room_obj)
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
                return render_template("home.html", name=inpt_user_name)
            else:
                session['room_code'] = inpt_code
                quiz_room_obj = quiz_room_manager_obj._quiz_room_obj_dict[session['room_code']]
                if quiz_room_obj._quiz_run_bool == True:
                    flash(
                        "The quiz has been started you cannot enter the room now.")
                    return render_template("home.html", name=inpt_user_name)
                if inpt_user_name[0].lower() in quiz_room_obj._members_dict.values():
                    flash(
                        "The user name has been taken by other member of the room, Enter another")
                    return render_template("home.html", name=inpt_user_name)
                else:
                    session['disp_room_name'] = quiz_room_obj._room_name
                    quiz_room_obj.add_member_to_room(memb_name, memb_id, memb_session_id)
                return redirect(url_for('home_blueprint.quiz_room_view_function'))

    return render_template("home.html")


@home_blueprint.route('/quiz_room', methods=['GET', 'POST'])
def quiz_room_view_function():
	# show a list of existing quizzes to users
	conn = get_db_connection()
	get_quizzes = "SELECT quiz_id, quiz_name FROM quiz;"
	sql_rest = None
	try:
		sql_rest = conn.execute(text(get_quizzes))
	except SQLAlchemyError as e:
		print(e)
	close_db_connection()
	quiz_list = sql_rest.fetchall()

	return render_template("room.html", quiz_list=quiz_list)