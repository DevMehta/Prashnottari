from flask import Blueprint

homeBP = Blueprint('homeBP', __name__)

from . import home