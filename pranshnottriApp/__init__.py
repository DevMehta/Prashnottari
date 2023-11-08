from flask import Flask
from flask_socketio import SocketIO

socketio = SocketIO(async_mode='threading')

def create_app(debug=False):
    """Create an application."""
    app = Flask(__name__)
    app.debug = debug
    app.config['SECRET_KEY'] = 'gjr39dkjn344_!67#'

    from . home import home_blueprint
    app.register_blueprint(home_blueprint)

    '''
    from . create_quiz import create_quiz_blueprint
    app.register_blueprint(create_quiz_blueprint)
    '''

    socketio.init_app(app)
    return app