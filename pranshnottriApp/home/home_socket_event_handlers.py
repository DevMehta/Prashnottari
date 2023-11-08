from flask import session, redirect, url_for, current_app
from flask_socketio import join_room, leave_room, send, emit
from .. import socketio
from threading import Thread
import time
from .. quiz import Quiz
from .. quiz_question import QuizQuestion
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from .. db import get_db_connection, close_db_connection

'''
Event handler for the event of creating a new quiz room.
A room is always assigned to each of the client when they connect
but other processing which completes room creation from business logic 
point of view has to be done here.
Namespace: quiz_room_namespace
'''
@socketio.on("joined", namespace="/quiz_room_namespace")
def join_quiz_room_handler(data):
    room_code = session.get('room_code')
    user_name = session.get('user_name')
    join_room(room_code)
    emit('joined_ack', {'msg': user_name + " HAS JOINED"}, namespace="/quiz_room_namespace", to=room_code)


@socketio.on("disconnect", namespace='quiz_room_namespace')
def disconnect_event_handler():
    room_code = session.get("room_code")
    user_name = session.get("user_name")
    leave_room(room_code)

    '''
    if room_code in quiz_room_manager_obj._room_codes:
        quiz_room_manager_obj._room_codes.remove(room_code)
    '''

    emit('left_room',{"name": user_name, "message": "has left the room"}, namespace="/quiz_room_namespace", to=room_code)
    print(f"{user_name} has left the room {room_code}")

@socketio.on("start_quiz_btn_evnt", namespace='/quiz_room_namespace')
def start_quiz_handler():
    room_code = session.get("room_code")
    quiz_set_up = socketio.start_background_task(set_up_question, current_app.app_context(), current_app.test_request_context())
    for i in range(10, -1, -1):
        emit('before_start_timer', {'time': i}, namespace='/quiz_room_namespace', to=room_code)
        #time.sleep(1)
        socketio.sleep(1)

    quiz_set_up.join()
        
    #quiz_id = session.get('quiz_id')
    quiz_id = '1001'

    quiz_ques_lst = QuizQuestion._quiz_question_obj_dict[quiz_id]
    for i in range(len(quiz_ques_lst)):
        json_quiz_ques_msg = {
            'ques_txt' : quiz_ques_lst[i]._question_text,
            'op1' : quiz_ques_lst[i]._op1,
            'op2' : quiz_ques_lst[i]._op2,
            'op3' : quiz_ques_lst[i]._op3,
            'op4' : quiz_ques_lst[i]._op4
        }
        '''timer_thread = Thread(target=quiz_timer_func, args=(room_code, current_app.app_context(),), daemon=True)
        timer_thread.start()'''
        socketio.start_background_task(quiz_timer_func, room_code, current_app.app_context())
        emit('show_ques', json_quiz_ques_msg, namespace="/quiz_room_namespace", to=room_code)
        #time.sleep(10)'''
        socketio.sleep(11)
    
def quiz_timer_func(room_code, app_cntxt):
    with app_cntxt:
        for i in range(10, -1, -1):
            emit('quiz_timer', {'time': i}, namespace='/quiz_room_namespace', to=room_code)
            #time.sleep(1)
            socketio.sleep(1)

def set_up_question(app_cntxt, req_cntxt):
    with app_cntxt:
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
        with req_cntxt:
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