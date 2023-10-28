from flask import session
from flask_socketio import join_room, leave_room, send, emit
from .. import socketio


'''
Event handler for the event of creating a new quiz room.
A room is always assigned to each of the client when they connect
but other processing which completes room creation from business logic 
point of view has to be done here.
Namespace: quiz_room
'''
@socketio.on("joined", namespace="/quiz_room_namespace")
def join_quiz_room_handler(data):
    print(data['msg'])
    room_code = session.get('room_code')
    user_name = session.get('user_name')
    join_room(room_code)
    emit('joined_ack', {'msg': user_name + " HAS JOINED"}, namespace="/quiz_room_namespace", to=room_code)


@socketio.on("disconnect")
def disconnect_event_handler():
    room_code = session.get("room_code")
    user_name = session.get("user_name")
    leave_room(room_code)

    if room_code in quiz_room_manager_obj._room_codes:
        quiz_room_manager_obj._room_codes.remove(room_code)

    emit({"name": name, "message": "has left the room"}, to=room_code)
    print(f"{name} has left the room {room}")