from flask import Blueprint

quiz_run_blueprint = Blueprint(
    'quiz_run_blueprint', __name__, template_folder='templates')

from . import quiz_run_views
from . import quiz_run_socket_event_handlers