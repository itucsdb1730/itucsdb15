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


@useroperationshelper.route('/updateuser', methods=['GET', 'POST'])
def UpdateUser():
    if not IsAuthenticated():
        return redirect('/')

    try:
        user = User()

        user.firstName = request.args.get('usersettings_firstName', "", type=STRING)
        user.lastName = request.args.get('usersettings_lastName', "", type=STRING)
        user.username = request.args.get('usersettings_username', "", type=STRING)
        user.email = request.args.get('usersettings_email', "", type=STRING)
        user.password = request.args.get('usersettings_password', "", type=STRING)

        user.userId = GetUserIdSession()

        validationMessage = user.IsValid()

        if validationMessage != "":
            return jsonify(validationMessage)

        filterParameter = FilterParameter("USERUSERNAME", "LIKE", user.username)
        filterExpression = FilterExpression()
        filterExpression.AddParameter(filterParameter)
        users = userhandler.Get(filterExpression)

        if len(users) > 0 and users[0].userId != GetUserIdSession():
            return jsonify("This username is already taken")

        filterParameter = FilterParameter("USEREMAIL", "LIKE", user.email)
        filterExpression = FilterExpression()
        filterExpression.AddParameter(filterParameter)
        users = userhandler.Get(filterExpression)

        if len(users) > 0 and users[0].userId != GetUserIdSession():
            return jsonify("This e-mail address is already taken")

        userhandler.Update(user)
        SetUserIdSession(user.userId)
        SetFullNameSession(user.firstName + " " + user.lastName)
        SetUsernameSession(user.username)

        return jsonify("")
    except:
        return jsonify("Unexpected error occured")


@useroperationshelper.route('/deleteuser', methods=['GET', 'POST'])
def DeleteUser():
    if not IsAuthenticated():
        return redirect('/')

    try:
        userhandler.Delete(GetUserIdSession())
        SetUserIdSession(-1)
        SetFullNameSession("")
        SetUsernameSession("")

        return jsonify(True)
    except:
        return jsonify(False)