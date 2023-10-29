from flask import render_template, request, session, redirect, url_for
from . import create_quiz_blueprint


from sqlalchemy import text
from .. db import get_db_connection, close_db_connection

@create_quiz_blueprint.route('/createQuiz', methods=['GET', 'POST'])
def create_quiz_function():

    conn = get_db_connection()
    
    # SQL SELECT query
    query = text("SELECT * FROM quiz_question")
    resp = conn.execute(query)
    for row in resp:
        print(row)

    close_db_connection()
    
    return render_template('quiz.html')