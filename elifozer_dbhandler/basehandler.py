import psycopg2 as dbapi2
from elifozer_utilities.currentconfig import CurrentConfig

dbVersion = 33

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

        DbExecute(insertAdminQuery, connection, cursor, ('admin1', 'admin1', 'elif', 'elif', 'elif@elif.com', 1))
        DbExecute(insertAdminQuery, connection, cursor, ('admin2', 'admin2', 'adem', 'adem', 'adem@adem.com', 1))
        DbExecute(insertAdminQuery, connection, cursor, ('admin3', 'admin3', 'egemen', 'egemen', 'egemen@egemen.com', 1))

        return
    else:
        DbClose(connection, cursor)

        currentDbVersionInt = int(currentDbVersion[0])

        if currentDbVersionInt < dbVersion:
            DropTable()
            DbInitialize()


def DropTable():
    connection, cursor = DbConnect()

    dropQuery =  """DROP TABLE IF EXISTS TICKET_DBT CASCADE;
                    DROP TABLE IF EXISTS CONCERT_DBT CASCADE;
                    DROP TABLE IF EXISTS CONCERT_AREA_DBT CASCADE;
                    DROP VIEW IF EXISTS NEWSVIEW CASCADE;
                    DROP TABLE IF EXISTS NEWS_DBT CASCADE;
                    DROP TABLE IF EXISTS MUSICIAN_DBT CASCADE;
                    DROP TABLE IF EXISTS USERS_DBT CASCADE;
                    DROP TABLE IF EXISTS CONFIG_DBT CASCADE;"""

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
                       MUSICIANNAME VARCHAR(40) UNIQUE NOT NULL,
                       MUSICIANGENRE VARCHAR(40),
                       MUSICIANESTYEAR VARCHAR(4) NOT NULL,
                       MUSICIANIMGURL VARCHAR(200),
                       MUSICIANDESC VARCHAR(300))"""

    DbExecute(musicianQuery, connection, cursor)

    newsQuery = """CREATE TABLE IF NOT EXISTS NEWS_DBT(
                   NEWSID SERIAL PRIMARY KEY,
                   NEWSTITLE VARCHAR(200) NOT NULL,
                   NEWSMUSICIANID INTEGER REFERENCES MUSICIAN_DBT (MUSICIANID) ON DELETE CASCADE ON UPDATE CASCADE,
                   NEWSCONTENT VARCHAR(400) NOT NULL,
                   NEWSIMGURL VARCHAR(200),
                   CREATEDBY INTEGER REFERENCES USER_DBT (USERID) ON DELETE CASCADE ON UPDATE CASCADE,
                   CREATEDATE TIMESTAMP DEFAULT LOCALTIMESTAMP,
                   UPDATEDATE TIMESTAMP DEFAULT LOCALTIMESTAMP)"""

    DbExecute(newsQuery, connection, cursor)

    newsViewQuery = """CREATE VIEW NEWSVIEW AS
                            SELECT N.*, U.USERUSERNAME AS CREATORNAME, M.MUSICIANNAME FROM NEWS_DBT N
                                      INNER JOIN USER_DBT U ON N.CREATEDBY = U.USERID
                                      INNER JOIN MUSICIAN_DBT M ON N.NEWSMUSICIANID = M.MUSICIANID"""

    DbExecute(newsViewQuery, connection, cursor)

    concert_areaQuery = """CREATE TABLE IF NOT EXISTS CONCERT_AREA_DBT(
                           CONCERT_AREAID SERIAL PRIMARY KEY,
                           CONCERT_AREANAME VARCHAR(40) NOT NULL,
                           CONCERT_AREAADRESS VARCHAR(400) NOT NULL,
                           CONCERT_AREACAPACITY VARCHAR(7) NOT NULL)"""

    DbExecute(concert_areaQuery, connection, cursor)

    concertQuery = """CREATE TABLE IF NOT EXISTS CONCERT_DBT(
                      CONCERTID SERIAL PRIMARY KEY,
                      CONCERTCONCERT_AREAID INTEGER REFERENCES CONCERT_AREA_DBT (CONCERT_AREAID) ON DELETE CASCADE ON UPDATE CASCADE,
                      CONCERTMUSICIANID INTEGER REFERENCES MUSICIAN_DBT (MUSICIANID) ON DELETE CASCADE ON UPDATE CASCADE,
                      CONCERTDATE VARCHAR(12) NOT NULL)"""

    DbExecute(concertQuery, connection, cursor)

    ticketQuery = """CREATE TABLE IF NOT EXISTS TICKET_DBT(
                     TICKETID SERIAL PRIMARY KEY,
                     TICKETCONCERT_ID INTEGER REFERENCES CONCERT_DBT (CONCERTID) ON DELETE CASCADE ON UPDATE CASCADE,
                     TICKETPRICE VARCHAR(10) NOT NULL,
                     TICKETAVAILABLE VARCHAR(7) NOT NULL)"""

    DbExecute(ticketQuery, connection, cursor)

    DbClose(connection, cursor)
    CheckDbVersion()