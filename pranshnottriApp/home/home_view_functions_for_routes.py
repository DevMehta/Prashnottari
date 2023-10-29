from flask import render_template, request, session, redirect, url_for, flash
from . import home_blueprint
from .. quiz_room_manager import QuizRoomManager
from .. quiz_room import QuizRoom
from .. quiz_room_member import QuizRoomMember
from datetime import datetime

quiz_room_manager_obj = QuizRoomManager()

@home_blueprint.route('/', methods=['GET', 'POST'])
def home_view_function():
	if request.method == 'POST':
		inpt_user_name = request.form.get("user-name-inpt")
		disp_room_name = request.form.get("room-name-inpt")
		inpt_code = request.form.get("code-inpt")
		join_option = request.form.get("join-btn", False)
		create_option = request.form.get("create-btn", False)
		print("CO",create_option)
		print("JO",join_option)
		session['user_name'] = inpt_user_name

		# Create the member object
		memb_name = inpt_user_name
		memb_join_time = datetime.now()
		memb_role = ""
		if create_option == False:
			memb_role = "non-creator"
		else:
			memb_role = "creator"

		memb_obj = QuizRoomMember(memb_join_time, memb_name, memb_role)


		''' handle new room creation '''
		if create_option != False:
			session['disp_room_name'] = disp_room_name
			quiz_room_obj = quiz_room_manager_obj.before_first_join_processing()
			quiz_room_manager_obj.add_quiz_room_obj(quiz_room_obj)
			print(quiz_room_manager_obj._room_codes)
			print(quiz_room_manager_obj._rooms_current_count)
			return render_template("room.html", name=inpt_user_name)

		''' handle joining to an existing room '''	
		if join_option != False:
			# TO DO: check if the entered room code is valid or not
			if inpt_code not in quiz_room_manager_obj._room_codes:
				# TO DO return an error that invalid quiz room code
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
					quiz_room_obj.add_member_to_room()
					print(quiz_room_obj._members_lst)
					print(quiz_room_manager_obj._room_codes)
				return render_template("room.html", name=inpt_user_name)

		print(quiz_room_manager_obj._room_codes)		
	return render_template("home.html")



@home_blueprint.route('/quiz_run', methods=['GET', 'POST'])
def quiz_run_view_function():
	pass