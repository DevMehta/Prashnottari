from flask import render_template, request, session, redirect, url_for, flash
from . import create_quiz_blueprint
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy import text
from .. db import get_db_connection, close_db_connection



@create_quiz_blueprint.route('/create_quiz', methods=['GET', 'POST'])
def create_quiz_view_function():

    if request.method == "POST":
        flash("Submitted Successfully")
        submit_quiz = request.form.get("submit_quiz", False)
        if submit_quiz != False:
            quiz_name = request.form['quiz_name']
            quiz_id = request.form.getlist('quiz_id')
            question_id = request.form.getlist('question_id')
            op1 = request.form.getlist('op1')
            op2 = request.form.getlist('op2')
            op3 = request.form.getlist('op3')
            op4 = request.form.getlist('op4')
            correct_ans = request.form.getlist('correct_ans')
            question_text = request.form.getlist('question_text')
            data = [{'quiz_id': quiz_id[0], 'question_id': question_id[k], 'op1': op1[k], 'op2': op2[k], 'op3': op3[k], 'op4': op4[k], 'correct_ans': correct_ans[k], 'question_text': question_text[k]}
                    for k, v in enumerate(question_text)]

            conn = get_db_connection()
            for mydict in data:
                placeholders = ', '.join(['%s'] * len(mydict))
                columns = ', '.join(str(x).replace('/', '_')
                                    for x in mydict.keys())
                values = ', '.join(
                    "'" + str(x).replace('/', '_') + "'" for x in mydict.values())
                sql = "INSERT INTO %s ( %s ) VALUES ( %s );" % (
                    'quiz_question', columns, values)
                print(sql)
                try:
                    resp = conn.execute(text(sql))
                except Exception as e:
                    print(e)
                print(resp)
            conn.commit()
            close_db_connection()

        return redirect(url_for('home_blueprint.home_view_function'))

    question_count = 3
    return render_template('quiz.html', question_count=question_count)