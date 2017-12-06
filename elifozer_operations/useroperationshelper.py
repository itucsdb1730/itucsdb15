from flask import Blueprint, jsonify, Flask
from flask.globals import request
from werkzeug.utils import redirect
from click.types import STRING

from elifozer_dbmodels.userdbo import User
from elifozer_dbhandler import userhandler
from elifozer_utilities.filterexpression import FilterExpression
from elifozer_utilities.filterparameter import FilterParameter
from elifozer_utilities.commonhelper import IsAuthenticated, SetUserIdSession, GetUserIdSession, SetFullNameSession, SetUsernameSession, StringSplit, UserToJSON


app = Flask(__name__)
useroperationshelper = Blueprint('useroperationshelper', __name__)


@useroperationshelper.route('/login', methods=['GET', 'POST'])
def Login():
    usernameEmail = request.args.get('loginUsernameEmail', "", type=STRING)
    user = userhandler.GetByUsernameOrEmail(usernameEmail)

    if user.userId == -1:
        return jsonify("Invalid username or e-mail")

    if user.password != request.args.get('loginPassword', "", type=STRING):
        return jsonify("Invalid password")

    SetUserIdSession(user.userId)
    SetFullNameSession(user.firstName + " " + user.lastName)
    SetUsernameSession(user.username)

    return jsonify("")


@useroperationshelper.route('/logout', methods=['GET'])
def Logout():
    SetUserIdSession(-1)
    SetFullNameSession("")
    SetUsernameSession("")

    return redirect('/')


@useroperationshelper.route('/register', methods=['GET', 'POST'])
def Register():
    if IsAuthenticated():
        return redirect('/')

    user = User()

    user.firstName = request.args.get('registerFirstName', "", type=STRING)
    user.lastName = request.args.get('registerLastName', "", type=STRING)
    user.username = request.args.get('registerUsername', "", type=STRING)
    user.email = request.args.get('registerEmail', "", type=STRING)
    user.password = request.args.get('registerPassword', "", type=STRING)
    user.userType = 2

    validationMessage = user.IsValid()

    if validationMessage != "":
        return jsonify(validationMessage)

    filterParameter = FilterParameter("USERUSERNAME", "LIKE", user.username)
    filterExpression = FilterExpression()
    filterExpression.AddParameter(filterParameter)
    users = userhandler.Get(filterExpression)

    if len(users) > 0:
        return jsonify("Username already exists")

    filterParameter = FilterParameter("USEREMAIL", "LIKE", user.email)
    filterExpression = FilterExpression()
    filterExpression.AddParameter(filterParameter)
    users = userhandler.Get(filterExpression)

    if len(users) > 0:
        return jsonify("Email already exists")

    user = userhandler.Insert(user)

    SetUserIdSession(user.userId)
    SetFullNameSession(user.firstName + " " + user.lastName)
    SetUsernameSession(user.username)

    return jsonify("")