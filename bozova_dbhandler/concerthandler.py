from elifozer_dbhandler import basehandler
from elifozer_utilities.filterparameter import FilterParameter
from elifozer_utilities.filterexpression import FilterExpression
from bozova_dbmodels.concertdbo import Concert


def GetByID(concertId):
    filterParameter = FilterParameter("CONCERTID" , "=", concertId)
    filterExpression = FilterExpression()
    filterExpression.AddParameter(filterParameter)

    return Get(filterExpression)[0]



def Get(filterExpression = None):
    connection, cursor = basehandler.DbConnect()

    myQuery = "SELECT * FROM CONCERT_DBT"

    if filterExpression is None:
        cursor = basehandler.DbExecute(myQuery, connection, cursor)
    else:
        myQuery += filterExpression.GetWhere()
        cursor = basehandler.DbExecute(myQuery, connection, cursor, filterExpression.GetParameters())

    ConcertList = []

    for concert in cursor.fetchall():
        tempConcert = concert()

        tempConcert.concertId = concert[0]
        tempConcert.concert_areaId = concert[1]
        tempConcert.musicianId = concert[2]
        tempConcert.date = concert[3]

        ConcertList.append(tempConcert)

    basehandler.DbClose(connection, cursor)

    return ConcertList


def Insert(newConcert):
    connection, cursor = basehandler.DbConnect()

    myQuery = """INSERT INTO CONCERT_DBT(CONCERTCONCERT_AREAID, CONCERTMUSICIANID, CONCERTDATE)
                 VALUES (%s, %s, %s) RETURNING CONCERTID;"""

    cursor = basehandler.DbExecute(myQuery, connection, cursor, (newConcert.concert_areaId, newConcert.musicianId, newConcert.date))

    newConcert.concertId = cursor.fetchone()[0]

    basehandler.DbClose(connection, cursor)

    return newConcert


def Update(currentConcert):
    connection, cursor = basehandler.DbConnect()

    myQuery = """UPDATE CONCERT_DBT SET  CONCERTCONCERT_AREAID = %s,
                                         CONCERTMUSICIANID = %s,
                                         CONCERTDATE = %s,
                 WHERE CONCERTID = %s"""

    cursor = basehandler.DbExecute(myQuery, connection, cursor, (currentConcert.concert_areaId, currentConcert.musicianId, currentConcert.date, currentConcert.ConcertId))

    basehandler.DbClose(connection, cursor)

    return currentConcert


def Delete(ConcertId):
    connection, cursor = basehandler.DbConnect()

    myQuery = "DELETE FROM CONCERT_DBT WHERE CONCERTID = " + str(ConcertId)

    cursor = basehandler.DbExecute(myQuery, connection, cursor)

    basehandler.DbClose(connection, cursor)

    return True
