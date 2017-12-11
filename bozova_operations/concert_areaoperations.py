from flask import Blueprint, render_template, Flask, request
from werkzeug.utils import redirect
from datetime import datetime, timedelta
from click.types import STRING

from bozova_dbmodels.concert_areadbo import Concert_area
from bozova_dbhandler import concert_areahandler
from elifozer_utilities.filterexpression import FilterExpression
from elifozer_utilities.filterparameter import FilterParameter
from elifozer_utilities.commonhelper import IsAuthenticated, GetUserIdSession, GetFullNameSession, GetUsernameSession, IsAdmin


app = Flask(__name__)
concert_areaoperations = Blueprint('concert_areaoperations', __name__)


@concert_areaoperations.route('/concert_area', methods=['GET'])
def Concert_area():
    searchBy = request.args.get('searchBy', "", type=STRING)

    filterParameter = FilterParameter("CONCERT_AREANAME", "LIKE", "%" + searchBy + "%")
    filterExpression = FilterExpression()
    filterExpression.AddParameter(filterParameter)

    concert_areaList = concert_areahandler.Get(filterExpression)

    return render_template('concert_area.html', concert_areaList = concert_areaList, authenticated = IsAuthenticated(), admin = IsAdmin(), fullName = GetFullNameSession())


