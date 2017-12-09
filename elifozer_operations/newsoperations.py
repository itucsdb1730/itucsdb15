from flask import Blueprint, render_template, Flask, request
from werkzeug.utils import redirect
from datetime import datetime, timedelta
from click.types import STRING

from elifozer_dbmodels.newsdbo import News
from elifozer_dbhandler import newsviewhandler
from elifozer_utilities.filterexpression import FilterExpression
from elifozer_utilities.filterparameter import FilterParameter
from elifozer_utilities.commonhelper import IsAuthenticated, GetUserIdSession, GetFullNameSession, GetUsernameSession, IsAdmin


app = Flask(__name__)
newsoperations = Blueprint('newsoperations', __name__)


@newsoperations.route('/news', methods=['GET'])
def News():
    newsList = newsviewhandler.Get()

    return render_template('news.html', newsList = newsList, authenticated = IsAuthenticated(), admin = IsAdmin(), fullName = GetFullNameSession())