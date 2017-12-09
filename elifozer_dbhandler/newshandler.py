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
        tempNews.content = news[2]
        tempNews.imgUrl = news[3]
        tempNews.createdBy = news[4]
        tempNews.createDate = news[5]
        tempNews.updateDate = news[6]

        newsList.append(tempNews)

    basehandler.DbClose(connection, cursor)

    return newsList


def Insert(newNews):
    connection, cursor = basehandler.DbConnect()

    myQuery = """INSERT INTO NEWS_DBT(NEWSID, NEWSTITLE, NEWSCONTENT, NEWSIMGURL, CREATEDBY, CREATEDATE, UPDATEDATE)
                 VALUES (%s, %s, %s, %s, %s, %s, %S) RETURNING NEWSID;"""

    cursor = basehandler.DbExecute(myQuery, connection, cursor, (newNews.title, newNews.content, newNews.imgUrl, newNews.createdBy, newNews.createdDate, newNews.updateDate))

    newNews.newsId = cursor.fetchone()[0]

    basehandler.DbClose(connection, cursor)

    return newNews


def Update(currentNews):
    connection, cursor = basehandler.DbConnect()

    myQuery = """UPDATE NEWS_DBT SET NEWSTITLE = %s,
                                     NEWSCONTENT = %s,
                                     NEWSIMGURL = %s,
                                     CREATEDBY = %s,
                                     CREATEDATE = %s,
                                     UPDATEDATE = %s,
                 WHERE NEWSID = %s"""

    cursor = basehandler.DbExecute(myQuery, connection, cursor, (currentNews.title, currentNews.content, currentNews.imgUrl, currentNews.createdBy, currentNews.createdDate, currentNews.updateDate, currentNews.newsId))

    basehandler.DbClose(connection, cursor)

    return currentNews


def Delete(newsId):
    connection, cursor = basehandler.DbConnect()

    myQuery = "DELETE FROM NEWS_DBT WHERE NEWSID = " + str(newsId)

    cursor = basehandler.DbExecute(myQuery, connection, cursor)

    basehandler.DbClose(connection, cursor)

    return True
