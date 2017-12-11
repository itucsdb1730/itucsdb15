from elifozer_dbhandler import basehandler
from elifozer_utilities.filterparameter import FilterParameter
from elifozer_utilities.filterexpression import FilterExpression
from bozova_dbmodels.concert_areadbo import Concert_area


def GetByID(concert_areaId):
    filterParameter = FilterParameter("CONCERT_AREAID" , "=", concert_areaId)
    filterExpression = FilterExpression()
    filterExpression.AddParameter(filterParameter)

    return Get(filterExpression)[0]



def Get(filterExpression = None):
    connection, cursor = basehandler.DbConnect()

    myQuery = "SELECT * FROM CONCERT_AREA_DBT"

    if filterExpression is None:
        cursor = basehandler.DbExecute(myQuery, connection, cursor)
    else:
        myQuery += filterExpression.GetWhere()
        cursor = basehandler.DbExecute(myQuery, connection, cursor, filterExpression.GetParameters())

    Concert_areaList = []

    for concert_area in cursor.fetchall():
        tempConcert_area = Concert_area()

        tempConcert_area.concert_areaId = concert_area[0]
        tempConcert_area.name = concert_area[1]
        tempConcert_area.address = concert_area[2]
        tempConcert_area.capacity = concert_area[3]

        Concert_areaList.append(tempConcert_area)

    basehandler.DbClose(connection, cursor)

    return Concert_areaList


def Insert(newConcert_area):
    connection, cursor = basehandler.DbConnect()

    myQuery = """INSERT INTO CONCERT_AREA_DBT(CONCERT_AREANAME, CONCERT_AREAADRESS, CONCERT_AREACAPACITY)
                 VALUES (%s, %s, %s) RETURNING CONCERT_AREAID;"""

    cursor = basehandler.DbExecute(myQuery, connection, cursor, (newConcert_area.name, newConcert_area.address, newConcert_area.capacity))

    newConcert_area.concert_areaId = cursor.fetchone()[0]

    basehandler.DbClose(connection, cursor)

    return newConcert_area


def Update(currentConcert_area):
    connection, cursor = basehandler.DbConnect()

    myQuery = """UPDATE CONCERT_AREA_DBT SET CONCERT_AREANAME = %s,
                                         CONCERT_AREAADRESS = %s,
                                         CONCERT_AREACAPACITY = %s,
                 WHERE CONCERT_AREAID = %s"""

    cursor = basehandler.DbExecute(myQuery, connection, cursor, (currentConcert_area.name, currentConcert_area.address, currentConcert_area.capacity, currentConcert_area.concert_areaId))

    basehandler.DbClose(connection, cursor)

    return currentConcert_area


def Delete(concert_areaId):
    connection, cursor = basehandler.DbConnect()

    myQuery = "DELETE FROM CONCERT_AREA_DBT WHERE CONCERT_AREAID = " + str(concert_areaId)

    cursor = basehandler.DbExecute(myQuery, connection, cursor)

    basehandler.DbClose(connection, cursor)

    return True
