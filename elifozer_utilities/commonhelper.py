import re
from flask import session

from elifozer_dbmodels.userdbo import User
from elifozer_dbhandler import userhandler


def IsAuthenticated():
    if 'userId' not in session:
        return False;

    if session['userId'] == -1:
        return False;

    return True;

def IsAdmin():
    if 'userId' not in session:
        return False;

    if session['userId'] == -1:
        return False;

    user = userhandler.GetByID(GetUserIdSession())

    if(user.userType == 1):
        return True

    return False

def SetUserIdSession(userId):
    session['userId'] = userId


def GetUserIdSession():
    if 'userId' not in session:
        session['userId'] = -1

    return session['userId']


def SetFullNameSession(fullName):
    session['fullName'] = fullName


def GetFullNameSession():
    if 'fullName' not in session:
        session['fullName'] = ""

    return session['fullName']


def SetUsernameSession(username):
    session['username'] = username


def GetUsernameSession():
    if 'username' not in session:
        session['username'] = ""

    return session['username']


def UserToJSON(self):
    return {'userId': self.userId, 'firstName': self.firstName, 'lastName': self.lastName, 'username': self.username, 'email': self.email}


def StringSplit(self):
    return [p.replace("\x00", " ") for p in re.sub('".+?"', lambda m: m.group(0).replace(" ", "\x00"), self).split()]