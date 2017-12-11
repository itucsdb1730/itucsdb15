from elifozer_dbhandler import basehandler
from elifozer_utilities.filterparameter import FilterParameter
from elifozer_utilities.filterexpression import FilterExpression
from bozova_dbmodels.ticketdbo import Ticket


def GetByID(ticketId):
    filterParameter = FilterParameter("TICKETID" , "=", ticketId)
    filterExpression = FilterExpression()
    filterExpression.AddParameter(filterParameter)

    return Get(filterExpression)[0]



def Get(filterExpression = None):
    connection, cursor = basehandler.DbConnect()

    myQuery = "SELECT * FROM TICKET_DBT"

    if filterExpression is None:
        cursor = basehandler.DbExecute(myQuery, connection, cursor)
    else:
        myQuery += filterExpression.GetWhere()
        cursor = basehandler.DbExecute(myQuery, connection, cursor, filterExpression.GetParameters())

    TicketList = []

    for ticket in cursor.fetchall():
        tempTicket = Ticket()

        tempTicket.ticketId = ticket[0]
        tempTicket.concertId = ticket[1]
        tempTicket.price = ticket[2]
        tempTicket.avilable_ticket = ticket[3]

        TicketList.append(tempTicket)

    basehandler.DbClose(connection, cursor)

    return TicketList


def Insert(newTicket):
    connection, cursor = basehandler.DbConnect()

    myQuery = """INSERT INTO TICKET_DBT(TICKETCONCERTID, TICKETPRICE, TICKETAVALILABLE)
                 VALUES (%s, %s, %s) RETURNING TICKETID;"""

    cursor = basehandler.DbExecute(myQuery, connection, cursor, (newTicket.concertId, newTicket.price, newTicket.available_ticket))

    newTicket.TicketId = cursor.fetchone()[0]

    basehandler.DbClose(connection, cursor)

    return newTicket


def Update(currentTicket):
    connection, cursor = basehandler.DbConnect()

    myQuery = """UPDATE TICKET_DBT   SET TICKETCONCERTID = %s,
                                         TICKETPRICE = %s,
                                         TICKETAVAILABLE = %s,
                 WHERE TICKETID = %s"""

    cursor = basehandler.DbExecute(myQuery, connection, cursor, (currentTicket.concertId, currentTicket.price, currentTicket.available_ticket, currentTicket.TicketId))

    basehandler.DbClose(connection, cursor)

    return currentTicket


def Delete(TicketId):
    connection, cursor = basehandler.DbConnect()

    myQuery = "DELETE FROM TICKET_DBT WHERE TICKETID = " + str(TicketId)

    cursor = basehandler.DbExecute(myQuery, connection, cursor)

    basehandler.DbClose(connection, cursor)

    return True
