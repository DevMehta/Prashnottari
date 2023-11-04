from flask import session, redirect, url_for, current_app
from flask_socketio import join_room, leave_room, send, emit
from .. import socketio
from threading import Thread
import time
from .. quiz import Quiz
from .. quiz_question import QuizQuestion

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
    for i in range(10, -1, -1):
        time.sleep(1)
        emit('before_start_timer', {'time': i}, namespace='/quiz_room_namespace', to=room_code)

    quiz_id = session.get('quiz_id')

    quiz_ques_lst = QuizQuestion._quiz_question_obj_dict[quiz_id]
    for i in range(len(quiz_ques_lst)):
        json_quiz_ques_msg = {
            'ques_txt' : quiz_ques_lst[i]._question_text,
            'op1' : quiz_ques_lst[i]._op1,
            'op2' : quiz_ques_lst[i]._op2,
            'op3' : quiz_ques_lst[i]._op3,
            'op4' : quiz_ques_lst[i]._op4
        }
        timer_thread = Thread(target=quiz_timer_func, args=(room_code, current_app.app_context(),), daemon=True)
        timer_thread.start()
        emit('show_ques', json_quiz_ques_msg, namespace="/quiz_room_namespace", to=room_code)
        time.sleep(10)
    

def quiz_timer_func(room_code, app_cntxt):
    with app_cntxt:
        for i in range(10, -1, -1):
            emit('quiz_timer', {'time': i}, namespace='/quiz_room_namespace', to=room_code)
            time.sleep(1)