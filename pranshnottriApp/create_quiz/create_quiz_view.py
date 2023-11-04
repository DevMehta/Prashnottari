from flask import render_template, request, session, redirect, url_for, flash
from . import create_quiz_blueprint
from sqlalchemy.exc import SQLAlchemyError

from sqlalchemy import text
from .. db import get_db_connection, close_db_connection


@create_quiz_blueprint.route('/createQuiz', methods=['GET', 'POST'])
def create_quiz_function():

    if request.method == "POST":
        submit_quiz = request.form.get("submit_quiz", False)
        if submit_quiz != False:
            try:
                user_name = session['user_name']
                quiz_name = request.form['quiz_name']
                conn = get_db_connection()
                query_count_quizID = "Select count(*) from quiz"
                resp = conn.execute(text(query_count_quizID))

                quiz_id = int(resp.scalar()) + 1001
                columns = "quiz_id, username, quiz_topic"
                values = str("'" + str(quiz_id) + "' , '" +
                             str(user_name) + "', '" + str(quiz_name) + "'")
                query_insert_quiz = "INSERT INTO %s ( %s ) VALUES ( %s );" % (
                    'quiz', columns, values)

                resp = conn.execute(text(query_insert_quiz))

            # quiz_id = 1001  # request.form.getlist('quiz_id')
                question_id = request.form.getlist('question_id')
                op1 = request.form.getlist('op1')
                op2 = request.form.getlist('op2')
                op3 = request.form.getlist('op3')
                op4 = request.form.getlist('op4')
                correct_ans = request.form.getlist('correct_ans')
                question_text = request.form.getlist('question_text')
                data_quiz_question = [{'quiz_id': quiz_id, 'question_id': question_id[k], 'op1': op1[k], 'op2': op2[k], 'op3': op3[k], 'op4': op4[k], 'correct_ans': correct_ans[k], 'question_text': question_text[k]}
                                      for k, v in enumerate(question_text)]

            # print(data_quiz_question)

            # conn = get_db_connection()
            # sql = """INSERT INTO quiz_question ( quiz_id, question_id, op1, op2, op3, op4, correct_ans, question_text ) VALUES ( "1001", "2002", "Q1O1", "Q1O2", "Q1O3", "Q1O4", "1", "Q1" );"""
            # try:
            #     conn.execute(text(sql))
            # except SQLAlchemyError as e:
            #     error = str(e.__dict__['orig'])
            #     print(error)
            # close_db_connection()

                for mydict in data_quiz_question:
                    placeholders = ', '.join(['%s'] * len(mydict))
                    columns = ', '.join(str(x).replace('/', '_')
                                        for x in mydict.keys())
                    values = ', '.join(
                        "'" + str(x).replace('/', '_') + "'" for x in mydict.values())
                    query_insert_qiuz_question = "INSERT INTO %s ( %s ) VALUES ( %s );" % (
                        'quiz_question', columns, values)
                    try:
                        resp = conn.execute(text(query_insert_qiuz_question))
                    except Exception as e:
                        print(e)
                conn.commit()
                close_db_connection()

            except Exception as e:
                print(e)

        flash("Submitted Successfully")
        return redirect(url_for('home_blueprint.home_view_function'))

    question_count = 3
    return render_template('quiz.html', question_count=question_count)