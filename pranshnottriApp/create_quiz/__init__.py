from flask import Blueprint

create_quiz_blueprint = Blueprint(
    'create_quiz_blueprint', __name__, template_folder='templates')

from . import create_quiz_view