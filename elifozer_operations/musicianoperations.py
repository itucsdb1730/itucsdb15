from flask import Blueprint, render_template, Flask, request
from werkzeug.utils import redirect
from datetime import datetime, timedelta
from click.types import STRING

from elifozer_dbmodels.musiciandbo import Musician
from elifozer_dbhandler import musicianhandler
from elifozer_utilities.filterexpression import FilterExpression
from elifozer_utilities.filterparameter import FilterParameter
from elifozer_utilities.commonhelper import IsAuthenticated, GetUserIdSession, GetFullNameSession, GetUsernameSession, IsAdmin


app = Flask(__name__)
musicianoperations = Blueprint('musicianoperations', __name__)


@musicianoperations.route('/musicians', methods=['GET'])
def Musicians():
    searchBy = request.args.get('searchBy', "", type=STRING)

    filterParameter = FilterParameter("MUSICIANNAME", "LIKE", "%" + searchBy + "%")
    filterExpression = FilterExpression()
    filterExpression.AddParameter(filterParameter)

    musicianList = musicianhandler.Get(filterExpression)

    return render_template('musicians.html', musicianList = musicianList, authenticated = IsAuthenticated(), admin = IsAdmin(), fullName = GetFullNameSession())