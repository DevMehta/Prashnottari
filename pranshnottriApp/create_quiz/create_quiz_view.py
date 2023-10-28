from flask import render_template, request, session, redirect, url_for
from . import create_quiz_blueprint

@create_quiz_blueprint.route('/createQuiz', methods=['GET', 'POST'])
def create_quiz_function():
    return render_template('quiz.html')