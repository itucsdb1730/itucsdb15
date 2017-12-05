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


def Insert(newUser):
    connection, cursor = basehandler.DbConnect()

    myQuery = """INSERT INTO USER_DBT(USERFIRSTNAME, USERLASTNAME, USERUSERNAME, USERPASSWORD, USEREMAIL, USERTYPE)
                 VALUES (%s, %s, %s, %s, %s, %s) RETURNING USERID;"""

    cursor = basehandler.DbExecute(myQuery, connection, cursor, (newUser.firstName, newUser.lastName, newUser.username, newUser.password, newUser.email, newUser.userType))

    newUser.userId = cursor.fetchone()[0]

    basehandler.DbClose(connection, cursor)

    return newUser


def Update(currentUser):
    connection, cursor = basehandler.DbConnect()

    myQuery = """UPDATE USER_DBT SET USERFIRSTNAME = %s,
                                     USERLASTNAME = %s,
                                     USERUSERNAME = %s,
                                     USERPASSWORD = %s,
                                     USEREMAIL = %s
                 WHERE USERID = %s"""

    cursor = basehandler.DbExecute(myQuery, connection, cursor, (currentUser.firstName, currentUser.lastName, currentUser.username, currentUser.password, currentUser.email, currentUser.userId))

    basehandler.DbClose(connection, cursor)

    return currentUser


def Delete(userId):
    connection, cursor = basehandler.DbConnect()

    myQuery = "DELETE FROM USER_DBT WHERE USERID = " + str(userId)

    cursor = basehandler.DbExecute(myQuery, connection, cursor)

    basehandler.DbClose(connection, cursor)

    return True
