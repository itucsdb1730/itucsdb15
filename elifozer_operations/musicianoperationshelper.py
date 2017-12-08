from flask import Blueprint, jsonify, Flask
from flask.globals import request
from click.types import STRING

from elifozer_dbmodels.musiciandbo import Musician
from elifozer_dbhandler import musicianhandler, userhandler
from elifozer_utilities.filterexpression import FilterExpression
from elifozer_utilities.filterparameter import FilterParameter
from elifozer_utilities.commonhelper import IsAuthenticated, GetUserIdSession


app = Flask(__name__)
musicianoperationshelper = Blueprint('musicianoperationshelper', __name__)

