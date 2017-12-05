import psycopg2 as dbapi2
from elifozer_utilities.currentconfig import CurrentConfig

dbVersion = 1


def DbConnect():
    try:
        connection = dbapi2.connect(CurrentConfig.appConfig)
        cursor = connection.cursor()

    except dbapi2.DatabaseError:
        connection.rollback()
        connection.close()

    return connection, cursor


def DbExecute(myQuery, connection, cursor, param = None):
    try:
        if param is None:
            cursor.execute(myQuery)
        else:
            cursor.execute(myQuery, param)

        connection.commit()

    except dbapi2.DatabaseError:
        connection.rollback()

    return cursor


def DbClose(connection, cursor):
    try:
        cursor.close()
        connection.close()

    except dbapi2.DatabaseError:
        connection.rollback()
        connection.close()