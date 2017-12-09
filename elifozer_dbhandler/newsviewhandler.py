from elifozer_dbhandler import basehandler
from elifozer_utilities.filterparameter import FilterParameter
from elifozer_utilities.filterexpression import FilterExpression
from elifozer_dbmodels.newsviewdbo import NewsView


def GetByID(newsId):
    filterParameter = FilterParameter("NEWSID" , "=", newsId)
    filterExpression = FilterExpression()
    filterExpression.AddParameter(filterParameter)

    return Get(filterExpression)[0]


def Get(filterExpression = None):
    connection, cursor = basehandler.DbConnect()

    myQuery = "SELECT * FROM NEWSVIEW"

    if filterExpression is None:
        cursor = basehandler.DbExecute(myQuery, connection, cursor)
    else:
        myQuery += filterExpression.GetWhere()
        cursor = basehandler.DbExecute(myQuery, connection, cursor, filterExpression.GetParameters())

    newsViewList = []

    for nv in cursor.fetchall():
        tempNewsView = NewsView()

        tempNewsView.newsId = nv[0]
        tempNewsView.title = nv[1]
        tempNewsView.musicianId = nv[2]
        tempNewsView.content = nv[3]
        tempNewsView.imgUrl = nv[4]
        tempNewsView.createdBy = nv[5]
        tempNewsView.createDate = nv[6]
        tempNewsView.updateDate = nv[7]
        tempNewsView.creatorName = nv[8]
        tempNewsView.musicianName = nv[9]

        tempNewsView.updateDate = tempNewsView.updateDate.strftime('%d.%m.%Y')

        newsViewList.append(tempNewsView)

    basehandler.DbClose(connection, cursor)

    return newsViewList