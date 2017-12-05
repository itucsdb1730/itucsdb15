from elifozer_dbhandler import basehandler
from elifozer_utilities.filterparameter import FilterParameter
from elifozer_utilities.filterexpression import FilterExpression
from elifozer_dbmodels.userdbo import User


def GetByID(userId):
    filterParameter = FilterParameter("USERID" , "=", userId)
    filterExpression = FilterExpression()
    filterExpression.AddParameter(filterParameter)

    return Get(filterExpression)[0]


def GetByUsernameOrEmail(usernameEmail):
    filterParameter1 = FilterParameter("USERUSERNAME" , "LIKE", usernameEmail, "OR ")
    filterParameter2 = FilterParameter("USEREMAIL" , "LIKE", usernameEmail)
    filterExpression = FilterExpression()
    filterExpression.AddParameter(filterParameter1)
    filterExpression.AddParameter(filterParameter2)

    userList = Get(filterExpression)

    if len(userList) > 0:
        return userList[0]

    return User()


def Get(filterExpression = None):
    connection, cursor = basehandler.DbConnect()

    myQuery = "SELECT * FROM USER_DBT"

    if filterExpression is None:
        cursor = basehandler.DbExecute(myQuery, connection, cursor)
    else:
        myQuery += filterExpression.GetWhere()
        cursor = basehandler.DbExecute(myQuery, connection, cursor, filterExpression.GetParameters())

    userList = []

    for user in cursor.fetchall():
        tempUser = User()

        tempUser.userId = user[0]
        tempUser.firstName = user[1]
        tempUser.lastName = user[2]
        tempUser.username = user[3]
        tempUser.password = user[4]
        tempUser.email = user[5]
        tempUser.userType = user[6]

        userList.append(tempUser)

    basehandler.DbClose(connection, cursor)

    return userList