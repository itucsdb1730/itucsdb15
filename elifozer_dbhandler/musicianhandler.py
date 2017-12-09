from elifozer_dbhandler import basehandler
from elifozer_utilities.filterparameter import FilterParameter
from elifozer_utilities.filterexpression import FilterExpression
from elifozer_dbmodels.musiciandbo import Musician


def GetByID(musicianId):
    filterParameter = FilterParameter("MUSICIANID" , "=", musicianId)
    filterExpression = FilterExpression()
    filterExpression.AddParameter(filterParameter)

    return Get(filterExpression)[0]


def GetByMusicianName(musicianName):
    filterParameter = FilterParameter("MUSICIANNAME" , "LIKE", musicianName)
    filterExpression = FilterExpression()
    filterExpression.AddParameter(filterParameter)

    musicianList = Get(filterExpression)

    if len(musicianList) > 0:
        return musicianList[0]

    return Musician()


def Get(filterExpression = None):
    connection, cursor = basehandler.DbConnect()

    myQuery = "SELECT * FROM MUSICIAN_DBT"

    if filterExpression is None:
        cursor = basehandler.DbExecute(myQuery, connection, cursor)
    else:
        myQuery += filterExpression.GetWhere()
        cursor = basehandler.DbExecute(myQuery, connection, cursor, filterExpression.GetParameters())

    musicianList = []

    for musician in cursor.fetchall():
        tempMusician = Musician()

        tempMusician.musicianId = musician[0]
        tempMusician.name = musician[1]
        tempMusician.genre = musician[2]
        tempMusician.establishYear = musician[3]
        tempMusician.imgUrl = musician[4]
        tempMusician.description = musician[5]

        musicianList.append(tempMusician)

    basehandler.DbClose(connection, cursor)

    return musicianList


def Insert(newMusician):
    connection, cursor = basehandler.DbConnect()

    myQuery = """INSERT INTO MUSICIAN_DBT(MUSICIANNAME, MUSICIANGENRE, MUSICIANESTYEAR, MUSICIANIMGURL, MUSICIANDESC)
                 VALUES (%s, %s, %s, %s, %s) RETURNING MUSICIANID;"""

    cursor = basehandler.DbExecute(myQuery, connection, cursor, (newMusician.name, newMusician.genre, newMusician.establishYear, newMusician.imgUrl, newMusician.description))

    newMusician.musicianId = cursor.fetchone()[0]

    basehandler.DbClose(connection, cursor)

    return newMusician


def Update(currentMusician):
    connection, cursor = basehandler.DbConnect()

    myQuery = """UPDATE MUSICIAN_DBT SET MUSICIANNAME = %s,
                                         MUSICIANGENRE = %s,
                                         MUSICIANESTYEAR = %s,
                                         MUSICIANIMGURL = %s,
                                         MUSICIANDESC = %s
                 WHERE MUSICIANID = %s"""

    cursor = basehandler.DbExecute(myQuery, connection, cursor, (currentMusician.name, currentMusician.genre, currentMusician.establishYear, currentMusician.imgUrl, currentMusician.description, currentMusician.musicianId))

    basehandler.DbClose(connection, cursor)

    return currentMusician


def Delete(musicianId):
    connection, cursor = basehandler.DbConnect()

    myQuery = "DELETE FROM MUSICIAN_DBT WHERE MUSICIANID = " + str(musicianId)

    cursor = basehandler.DbExecute(myQuery, connection, cursor)

    basehandler.DbClose(connection, cursor)

    return True
