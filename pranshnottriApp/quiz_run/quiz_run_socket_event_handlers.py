from flask import session
from flask_socketio import emit
from .. import socketio
from threading import Thread
import time

from .. quiz import Quiz
from .. quiz_question import QuizQuestion

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from .. db import get_db_connection, close_db_connection


@socketio.on("request_questions", namespace="/quiz_run_namespace")
def request_questions_handler(sent_data):
    room_code = session.get('room_code')
    print(room_code)
    user_name = session.get('user_name')
    #bg_task_obj = socketio.start_background_task(question_ret_func, sent_data['quiz_id'])

    #bg_task_obj.join()
    print()
    emit('evnt1', {'msg': user_name + " HAS JOINED"}, namespace="/quiz_run_namespace", to=room_code)

def question_ret_func(quiz_id):
	# get the quiz from the db
    conn = get_db_connection()
    get_quiz_query = "SELECT * FROM quiz WHERE quiz_id = ( %s );" % (inpt_quiz_id)
    sql_rest = None
    try:
    	sql_rest = conn.execute(text(get_quiz_query))
    except SQLAlchemyError as e:
    	print(e)

    for row in sql_rest:
    	print(row)
	    
    conn.commit()
    close_db_connection()
	# make the quiz object
	# get quiz questions