import datetime

from elifozer_dbhandler import basehandler
from elifozer_utilities.filterparameter import FilterParameter
from elifozer_utilities.filterexpression import FilterExpression
from elifozer_dbmodels.newsdbo import News


def GetByID(newsId):
    filterParameter = FilterParameter("NEWSID" , "=", newsId)
    filterExpression = FilterExpression()
    filterExpression.AddParameter(filterParameter)

    return Get(filterExpression)[0]


def Get(filterExpression = None):
    connection, cursor = basehandler.DbConnect()

    myQuery = "SELECT * FROM NEWS_DBT"

    if filterExpression is None:
        cursor = basehandler.DbExecute(myQuery, connection, cursor)
    else:
        myQuery += filterExpression.GetWhere()
        cursor = basehandler.DbExecute(myQuery, connection, cursor, filterExpression.GetParameters())

    newsList = []

    for news in cursor.fetchall():
        tempNews = News()

        tempNews.newsId = news[0]
        tempNews.title = news[1]
        tempNews.musicianId = news[2]
        tempNews.content = news[3]
        tempNews.imgUrl = news[4]
        tempNews.createdBy = news[5]
        tempNews.createDate = news[6]
        tempNews.updateDate = news[7]

        newsList.append(tempNews)

    basehandler.DbClose(connection, cursor)

    return newsList


def Insert(newNews):
    connection, cursor = basehandler.DbConnect()

    myQuery = """INSERT INTO NEWS_DBT(NEWSTITLE, NEWSMUSICIANID, NEWSCONTENT, NEWSIMGURL, CREATEDBY)
                 VALUES (%s, %s, %s, %s, %s) RETURNING NEWSID;"""

    cursor = basehandler.DbExecute(myQuery, connection, cursor, (newNews.title, newNews.musicianId, newNews.content, newNews.imgUrl, newNews.createdBy))

    newNews.newsId = cursor.fetchone()[0]

    basehandler.DbClose(connection, cursor)

    return newNews


def Update(currentNews):
    connection, cursor = basehandler.DbConnect()

    myQuery = """UPDATE NEWS_DBT SET NEWSTITLE = %s,
                                     NEWSMUSICIANID = %s,
                                     NEWSCONTENT = %s,
                                     NEWSIMGURL = %s
                 WHERE NEWSID = %s"""

    cursor = basehandler.DbExecute(myQuery, connection, cursor, (currentNews.title, currentNews.musicianId, currentNews.content, currentNews.imgUrl, currentNews.newsId))

    myQuery = """UPDATE NEWS_DBT SET UPDATEDATE = LOCALTIMESTAMP WHERE NEWSID =""" + str(currentNews.newsId) + ";"

    cursor = basehandler.DbExecute(myQuery, connection, cursor)

    basehandler.DbClose(connection, cursor)

    return currentNews


def Delete(newsId):
    connection, cursor = basehandler.DbConnect()

    myQuery = "DELETE FROM NEWS_DBT WHERE NEWSID = " + str(newsId)

    cursor = basehandler.DbExecute(myQuery, connection, cursor)

    basehandler.DbClose(connection, cursor)

    return True
