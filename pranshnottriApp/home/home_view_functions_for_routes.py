from flask import render_template, request, session, redirect, url_for
from . import home_blueprint
from .. quiz_room_manager import QuizRoomManager
from .. quiz_room import QuizRoom
from .. quiz_room_member import QuizRoomMember
from datetime import datetime


quiz_room_manager_obj = QuizRoomManager()

@home_blueprint.route('/', methods=['GET', 'POST'])
def home_view_function():
	#session.clear()
	if request.method == 'POST':
		inpt_user_name = request.form.get("user-name-inpt")
		disp_room_name = request.form.get("room-name-inpt")
		inpt_code = request.form.get("code-inpt")
		join_option = request.form.get("join-btn", False)
		create_option = request.form.get("create-btn", False)

		session['user_name'] = inpt_user_name

		# Create the member object
		memb_name = inpt_user_name
		memb_join_time = datetime.now()
		memb_role = ""
		if create_option != False:
			memb_role = "creator"
		else:
			memb_role = "non-creator"

		memb_obj = QuizRoomMember(memb_join_time, memb_name, memb_role)

		''' handle new room creation '''
		if create_option != False:
			session['disp_room_name'] = disp_room_name
			quiz_room_manager_obj.before_first_join_processing()

			return render_template("room.html", name=inpt_user_name)

		''' handle joining to an existing room '''	
		if join_option != False:
			# TO DO: check if the entered room code is valid or not
			# TO DO: 
			session['room_code'] = inpt_code
			return render_template("room.html", name=inpt_user_name)
			
	return render_template("home.html")