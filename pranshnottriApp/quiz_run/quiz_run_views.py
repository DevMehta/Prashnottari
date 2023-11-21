from flask import render_template, request, session, redirect, url_for, flash, redirect
from . import quiz_run_blueprint
from .. quiz_room_manager import QuizRoomManager
from .. quiz_room import QuizRoom
from .. quiz_room_member import QuizRoomMember
#from .. quiz_run import QuizRun
from .. quiz import Quiz
from .. quiz_question import QuizQuestion

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy import text
from .. db import get_db_connection, close_db_connection


from datetime import datetime


@quiz_run_blueprint.route('/quiz_run', methods=['GET', 'POST'])
def quiz_run_view_function():
	
	return render_template("quiz_run.html")