from flask import Blueprint

home_blueprint = Blueprint('home_blueprint', __name__, template_folder='templates')

from . import home_socket_event_handlers
from . import home_view_functions_for_routes