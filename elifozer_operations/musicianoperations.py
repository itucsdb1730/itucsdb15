from flask import Blueprint, render_template, Flask
from werkzeug.utils import redirect
from datetime import datetime, timedelta

from elifozer_dbmodels.musiciandbo import Musician
from elifozer_dbhandler import musicianhandler
from elifozer_utilities.filterexpression import FilterExpression
from elifozer_utilities.filterparameter import FilterParameter
from elifozer_utilities.commonhelper import IsAuthenticated, GetUserIdSession, GetFullNameSession, GetUsernameSession, IsAdmin


app = Flask(__name__)
musicianoperations = Blueprint('musicianoperations', __name__)

@musicianoperations.route('/musicians', methods=['GET'])
def Musicians():
    musicianList = musicianhandler.Get()

    return render_template('musicians.html', musicianList = musicianList, authenticated = IsAuthenticated(), admin = IsAdmin(), fullName = GetFullNameSession())