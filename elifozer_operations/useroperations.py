from flask import Blueprint, render_template, Flask
from werkzeug.utils import redirect
from datetime import datetime, timedelta

from elifozer_dbmodels.userdbo import User
from elifozer_dbhandler import userhandler
from elifozer_utilities.filterexpression import FilterExpression
from elifozer_utilities.filterparameter import FilterParameter
from elifozer_utilities.commonhelper import IsAuthenticated, GetUserIdSession, GetFullNameSession, GetUsernameSession


app = Flask(__name__)
useroperations = Blueprint('useroperations', __name__)


@useroperations.route('/account', methods=['GET', 'POST'])
def Account():
    if IsAuthenticated():
        return redirect('/')

    return render_template('loginregister.html', currentUser=User(), authenticated = IsAuthenticated(), fullName = GetFullNameSession())


@useroperations.route('/home', methods=['GET'])
def Home():
    if not IsAuthenticated():
        return redirect('/')

    return render_template('userhome.html', currentUser=User(), authenticated = IsAuthenticated(), fullName = GetFullNameSession())