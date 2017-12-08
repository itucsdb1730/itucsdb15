import psycopg2 as dbapi2
from elifozer_utilities.currentconfig import CurrentConfig

dbVersion = 6


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


def CheckDbVersion():
    checkQuery = """SELECT CONFIGVALUE FROM CONFIG_DBT WHERE CONFIGID = 1"""

    connection,cursor = DbConnect()
    cursor = DbExecute(checkQuery, connection, cursor)
    currentDbVersion = cursor.fetchone()

    if currentDbVersion is None:
        insertConfigQuery = """INSERT INTO CONFIG_DBT(CONFIGID, CONFIGNAME, CONFIGVALUE) VALUES (1, %s, %s)"""

        DbExecute(insertConfigQuery, connection, cursor, ('dbVersion', dbVersion))

        insertAdminQuery = """INSERT INTO USER_DBT(USERFIRSTNAME, USERLASTNAME, USERUSERNAME, USERPASSWORD, USEREMAIL, USERTYPE) VALUES (%s, %s, %s, %s, %s, %s)"""

        DbExecute(insertAdminQuery, connection, cursor, ('admin', 'admin', 'elif', 'adem', 'ozere@itu.edu.tr', 1))

        return
    else:
        DbClose(connection, cursor)

        currentDbVersionInt = int(currentDbVersion[0])

        if currentDbVersionInt < dbVersion:
            DropTable()
            DbInitialize()


def DropTable():
    connection, cursor = DbConnect()

    dropQuery =  """DROP TABLE IF EXISTS MUSICIAN_DBT;
                    DROP TABLE IF EXISTS USERS_DBT;
                    DROP TABLE IF EXISTS CONFIG_DBT;"""

    DbExecute(dropQuery, connection, cursor)
    DbClose(connection, cursor)


def DbInitialize():
    connection, cursor = DbConnect()

    configQuery = """CREATE TABLE IF NOT EXISTS CONFIG_DBT(
                     CONFIGID SERIAL PRIMARY KEY,
                     CONFIGNAME VARCHAR(40),
                     CONFIGVALUE VARCHAR(40))"""

    DbExecute(configQuery, connection, cursor)

    userQuery = """CREATE TABLE IF NOT EXISTS USER_DBT(
                   USERID SERIAL PRIMARY KEY,
                   USERFIRSTNAME VARCHAR(40),
                   USERLASTNAME VARCHAR(40),
                   USERUSERNAME VARCHAR(40) NOT NULL UNIQUE,
                   USERPASSWORD VARCHAR(40) NOT NULL,
                   USEREMAIL VARCHAR(60) NOT NULL UNIQUE,
                   USERTYPE INTEGER NOT NULL)"""

    DbExecute(userQuery, connection, cursor)

    musicianQuery = """CREATE TABLE IF NOT EXISTS MUSICIAN_DBT(
                       MUSICIANID SERIAL PRIMARY KEY,
                       MUSICIANNAME VARCHAR(40) NOT NULL,
                       MUSICIANGENRE VARCHAR(40),
                       MUSICIANESTYEAR VARCHAR(4),
                       MUSICIANIMGURL VARCHAR(200),
                       MUSICIANDESC VARCHAR(300))"""

    DbExecute(musicianQuery, connection, cursor)
    DbClose(connection, cursor)
    CheckDbVersion()