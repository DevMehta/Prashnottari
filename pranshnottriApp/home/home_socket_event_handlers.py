from flask import session, redirect, url_for, current_app, request
from flask_socketio import join_room, leave_room, send, emit
from .. import socketio
from threading import Thread
import time
from .. quiz import Quiz
from .. quiz_question import QuizQuestion
from .. quiz_room_manager import QuizRoomManager
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from .. db import get_db_connection, close_db_connection
import uuid
from datetime import datetime
from .. quiz_run import MemberStats, QuizRun
from sortedcontainers import SortedDict
import random

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
    memb_id = session.get('memb_id')
    join_room(room_code)
    quiz_room_obj = QuizRoomManager._quiz_room_obj_dict[room_code]
    quiz_room_obj._members_dict[memb_id][1] = request.sid
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
def start_quiz_handler(data):
    quiz_id = str(data['inpt_quiz_id'])
    print("QUIZ ID" + quiz_id)
    room_code = session.get("room_code")
    quiz_set_up = socketio.start_background_task(set_up_question, current_app.app_context(), current_app.test_request_context(), quiz_id)
    quiz_run_setup_thrd = socketio.start_background_task(quiz_run_setup, current_app.app_context(), quiz_id, room_code)
    for i in range(10, -1, -1):
        emit('before_start_timer', {'time': i}, namespace='/quiz_room_namespace', to=room_code)
        socketio.sleep(1)

    quiz_set_up.join()
    quiz_run_setup_thrd.join()

    quiz_ques_lst = QuizQuestion._quiz_question_obj_dict[quiz_id]
    no_of_ques = len(quiz_ques_lst)

    '''
    Store the session ids of all members in a dict with memb.
    Get the sessions ids of all members
    use that to send questions to individual members
    per member dict is the only better soln. for that
    '''
    quiz_room_obj = QuizRoomManager._quiz_room_obj_dict[room_code]
    run_id = quiz_room_obj._currnt_run_id
    # get QuizRun object
    quiz_run_obj = quiz_room_obj._runs_dict[run_id]
    membs_dict = quiz_room_obj._members_dict

    for memb_id_key in membs_dict.keys():
        ques_range_obj = range(0, no_of_ques, 1)
        ques_range_list = list(ques_range_obj)
        random.shuffle(ques_range_list)
        quiz_run_obj._member_ques_show_dict[memb_id_key] = ques_range_list

    print(quiz_run_obj._member_ques_show_dict)
       
    for memb_id_key in membs_dict.keys():
        sid = membs_dict[memb_id_key][1]
        ques_range_list_shuffled = quiz_run_obj._member_ques_show_dict[memb_id_key]
        socketio.start_background_task(disp_ques, current_app.app_context(), sid, ques_range_list_shuffled, quiz_ques_lst, current_app.test_request_context())
    
    for i in range(len(quiz_ques_lst)):
        socketio.start_background_task(quiz_timer_func, room_code, current_app.app_context(), quiz_id)
        socketio.sleep(11)
        show_leaderboard_thrd = socketio.start_background_task(show_leaderboard, current_app.app_context(), room_code)


    '''
    for i in range(len(quiz_ques_lst)):
        json_quiz_ques_msg = {
            'question_id' : quiz_ques_lst[i]._question_id,
            'ques_txt' : quiz_ques_lst[i]._question_text,
            'op1' : quiz_ques_lst[i]._op1,
            'op2' : quiz_ques_lst[i]._op2,
            'op3' : quiz_ques_lst[i]._op3,
            'op4' : quiz_ques_lst[i]._op4
        }
        socketio.start_background_task(quiz_timer_func, room_code, current_app.app_context(), quiz_id)
        emit('show_ques', json_quiz_ques_msg, namespace="/quiz_room_namespace", to=room_code)
        socketio.sleep(11)
        show_leaderboard_thrd = socketio.start_background_task(show_leaderboard, current_app.app_context(), room_code)
    '''
def quiz_timer_func(room_code, app_cntxt, quiz_id):
    with app_cntxt:
        for i in range(10, -1, -1):
            emit('quiz_timer', {'time': i, 'quiz_id' : quiz_id}, namespace='/quiz_room_namespace', to=room_code)
            socketio.sleep(1)

def set_up_question(app_cntxt, req_cntxt, quiz_id):
    with app_cntxt:
        # get the quiz from the db
        conn = get_db_connection()
        get_quiz_query = "SELECT * FROM quiz WHERE quiz_id = ( %s );" % (quiz_id)
        sql_rest = None
        try:
            sql_rest = conn.execute(text(get_quiz_query))
        except SQLAlchemyError as e:
            print(e)
            
        row = sql_rest.fetchone()
        #qid = row[0]
        qname = row[1]
        qcateg = row[2]
        qcdate = row[3]
        qntmes_played = int(row[4])
        with req_cntxt:
            session['quiz_name'] = qname
            session['quiz_id'] = quiz_id
        conn.commit()

        # update number of times quiz has been played
        update_no_times_played_query = "UPDATE quiz SET no_of_times_played = (%s) WHERE quiz_id = ( %s );" % (qntmes_played + 1 ,quiz_id)
        sql_rest = None
        try:
            sql_rest = conn.execute(text(update_no_times_played_query))
        except SQLAlchemyError as e:
            print(e)
        conn.commit()
        
        # make the quiz object
        quiz_obj = Quiz(quiz_id, qname, qcateg, qcdate, qntmes_played)
        Quiz._quiz_obj_dict[quiz_id] = quiz_obj
        print(quiz_obj.__str__())
        
        # get quiz questions
        get_quiz_ques_query = "SELECT * FROM quiz_question WHERE quiz_id = ( %s );" % (quiz_id)
        sql_rest2 = None
        try:
            sql_rest2 = conn.execute(text(get_quiz_ques_query))
        except SQLAlchemyError as e:
            print(e)

        questions_recd = sql_rest2.fetchall()
        ques_lst = []
        for recd in questions_recd:
            print(recd)
            #q_id = str(recd[0])
            ques_id = str(recd[1])
            op1 = recd[2]
            op2 = recd[3]
            op3 = recd[4]
            op4 = recd[5]
            correct_ans = recd[6]
            ques_txt = recd[7]
            quiz_ques_obj = QuizQuestion(quiz_id, ques_id, op1, op2, op3, op4, correct_ans, ques_txt)
            ques_lst.append(quiz_ques_obj)

        QuizQuestion._quiz_question_obj_dict[quiz_id] = ques_lst

        close_db_connection()

def quiz_run_setup(app_cntxt, quiz_id, room_code):
    with app_cntxt:
    
        # set up memeber score class obj for each member
        memb_stats_obj_dict = {}
        quiz_room_obj = QuizRoomManager._quiz_room_obj_dict[room_code]
        members_dict = quiz_room_obj._members_dict
        for k in members_dict:
            memb_name = members_dict[k][0]
            memb_id = k
            member_per_ques_score_dict = {}
            member_stats_obj = MemberStats(memb_id, 0, member_per_ques_score_dict)
            memb_stats_obj_dict[memb_id] = member_stats_obj

        # Set up quiz run class objs
        run_id = str(uuid.uuid4())
        run_start_time = datetime.now()
        leaderboard_inpt = SortedDict()
        quiz_run_obj = QuizRun(run_id, run_start_time, leaderboard_inpt, memb_stats_obj_dict, {})


        # set current run id
        quiz_room_obj._currnt_run_id = run_id
        # add run class obj to a dict of runs
        quiz_room_obj._runs_dict[run_id] = quiz_run_obj

first_resp_flag = True    
@socketio.on("resp_evnt", namespace="/quiz_room_namespace")
def resp_handler(data):
    user_resp_option = str(data['resp'])
    user_resp_option = user_resp_option[2]
    question_id = str(data['question_id'])
    quiz_id = data['quiz_id']
    room_code = session['room_code']

    correct_ans = None
    lst_of_ques_objs = QuizQuestion._quiz_question_obj_dict[quiz_id]
    for ques_obj in lst_of_ques_objs:
        if ques_obj._question_id == question_id:
            correct_ans = str(ques_obj._correct_ans)

    # get the QuizRoom object
    quiz_room_obj = QuizRoomManager._quiz_room_obj_dict[room_code]
    # get quiz_run_id
    run_id = quiz_room_obj._currnt_run_id
    # get QuizRun object
    quiz_run_obj = quiz_room_obj._runs_dict[run_id]

    # find which member using id
    memb_id = str(session['memb_id'])

    # get MemberStas object
    memb_stat_obj = quiz_run_obj._member_stats_obj_dict[memb_id]
    # update scores
    positive_score = 10
    leaderboard = quiz_run_obj._leaderboard

    global first_resp_flag
    if first_resp_flag == True:
        first_resp_flag = False
        all_memb_lst = []
        membs_dict = quiz_room_obj._members_dict
        for memb_id_vals in membs_dict.keys():
            all_memb_lst.append(memb_id_vals)
        leaderboard[0] = all_memb_lst
    
    if correct_ans == user_resp_option:
        prev_score = memb_stat_obj._member_total_score
        memb_stat_obj._member_total_score  += 10
        memb_stat_obj._member_per_ques_score_dict[question_id] = True # True for correct ans
        # remove id from old list
        old_lst_of_memb_with_same_score = leaderboard[prev_score]
        old_lst_of_memb_with_same_score.remove(memb_id)

        if memb_stat_obj._member_total_score not in leaderboard.keys():
            lst_of_memb_with_same_score = []
            lst_of_memb_with_same_score.append(memb_id)
            leaderboard[memb_stat_obj._member_total_score] = lst_of_memb_with_same_score
        else:
            lst_of_memb_with_same_score = leaderboard[memb_stat_obj._member_total_score]
            lst_of_memb_with_same_score.append(memb_id)
    else:
        memb_stat_obj._member_per_ques_score_dict[question_id] = False # False for incorrect ans

def show_leaderboard(app_cntxt, room_code):
    with app_cntxt:
        # get the QuizRoom object
        quiz_room_obj = QuizRoomManager._quiz_room_obj_dict[room_code]
        # get quiz_run_id
        run_id = quiz_room_obj._currnt_run_id
        # get QuizRun object
        quiz_run_obj = quiz_room_obj._runs_dict[run_id]

        leaderboard = quiz_run_obj._leaderboard

        # show leaderboard
        rev_leaderboard = reversed(leaderboard)
        for score in rev_leaderboard:
            for memb_id in leaderboard[score]:
                # get name correcponding to id
                memb_name = quiz_room_obj._members_dict[memb_id][0]
                json_resp_msg = {
                    'memb_id' : memb_id,
                    'name' : memb_name,
                    'score' : score
                }
                socketio.emit("show_leaderboard_evnt", json_resp_msg, namespace="/quiz_room_namespace", to=room_code)
        # show to users on the frontend

def disp_ques(app_cntxt, user_session_id, ques_range_list_shuffled, quiz_ques_lst, req_cntxt):
    with app_cntxt:
        with req_cntxt:
            print(user_session_id)
            for i in ques_range_list_shuffled:
                json_quiz_ques_msg = {
                    'question_id' : quiz_ques_lst[i]._question_id,
                    'ques_txt' : quiz_ques_lst[i]._question_text,
                    'op1' : quiz_ques_lst[i]._op1,
                    'op2' : quiz_ques_lst[i]._op2,
                    'op3' : quiz_ques_lst[i]._op3,
                    'op4' : quiz_ques_lst[i]._op4
                }
                emit('show_ques', json_quiz_ques_msg, namespace="/quiz_room_namespace", to=user_session_id)
                socketio.sleep(11)