.. raw:: latex

    \newpage

Parts Implemented by Elif Özer
==============================

In this part, 3 major parts will be explained. These parts are User Operations, Musician Operations and News Operations. In each part,
related SQL tables, SQL queries, Python codes and JavaScript methods will be explained.

You can see the ER diagram for the parts implemented by Elif Özer below:

.. figure:: ../images/2.*
     :scale: 100 %
     :alt: ER Diagram
     :align: center

     ER Diagram implemented by Elif Özer


Whenever the project is ordered to run,


.. code-block:: python
   :linenos:

   CurrentConfig.appConfig = app.config['dsn']
   basehandler.DbInitialize()


in server.py are executed. Through appConfig, the database to be connected is determined. After this operation via DbInitialize function, database is created if it does not exist,
or it is updated with a newer version if exists. DbInitialize function also includes all create table queries.


.. code-block:: python
   :linenos:

   def DbInitialize():
       connection, cursor = DbConnect()

       configQuery = """CREATE TABLE IF NOT EXISTS CONFIG_DBT(
                        CONFIGID SERIAL PRIMARY KEY,
                        CONFIGNAME VARCHAR(40),
                        CONFIGVALUE VARCHAR(40))"""

       DbExecute(configQuery, connection, cursor)

      ...

      DbClose(connection, cursor)
      CheckDbVersion()


CheckDbVersion function reads the database version from CONFIG_DBT. After that, if value does not exist or is smaller than our hard-coded version, all tables will be dropped
and recreated with a newer database version.

In the following function, admin users are introduced into system.


.. code-block:: python
   :linenos:

   def CheckDbVersion():
       checkQuery = """SELECT CONFIGVALUE FROM CONFIG_DBT WHERE CONFIGID = 1"""

       connection,cursor = DbConnect()
       cursor = DbExecute(checkQuery, connection, cursor)
       currentDbVersion = cursor.fetchone()

       if currentDbVersion is None:
           insertConfigQuery = """INSERT INTO CONFIG_DBT(CONFIGID, CONFIGNAME, CONFIGVALUE) VALUES (1, %s, %s)"""

           DbExecute(insertConfigQuery, connection, cursor, ('dbVersion', dbVersion))

           insertAdminQuery = """INSERT INTO USER_DBT(USERFIRSTNAME, USERLASTNAME, USERUSERNAME, USERPASSWORD, USEREMAIL, USERTYPE) VALUES (%s, %s, %s, %s, %s, %s)"""

           DbExecute(insertAdminQuery, connection, cursor, ('admin1', 'admin1', ... , ... , ... , 1))
           DbExecute(...)
           DbExecute(...)

           return
       else:
           DbClose(connection, cursor)

           currentDbVersionInt = int(currentDbVersion[0])

           if currentDbVersionInt < dbVersion:
               DropTable()
               DbInitialize()


Dropping all tables is done (in reverse create order) by the below function:


.. code-block:: python
   :linenos:

   def DropTable():
       connection, cursor = DbConnect()

       dropQuery =  """DROP TABLE IF EXISTS TICKET_DBT CASCADE;
                       DROP TABLE IF EXISTS CONCERT_DBT CASCADE;
                       DROP TABLE IF EXISTS CONCERT_AREA_DBT CASCADE;
                       DROP VIEW IF EXISTS NEWSVIEW CASCADE;
                       DROP TABLE IF EXISTS NEWS_DBT CASCADE;
                       DROP TABLE IF EXISTS MUSICIAN_DBT CASCADE;
                       DROP TABLE IF EXISTS USER_DBT CASCADE;
                       DROP TABLE IF EXISTS CONFIG_DBT CASCADE;"""

       DbExecute(dropQuery, connection, cursor)
       DbClose(connection, cursor)


User Operations
===============

In this section, developments required for user operations will be explained.

SQL
---

Information regarding the user such as user first name, user last name, user username etc. kept in the database table USER_DBT.
News table will be explained later on, but this table has a foreign key relation to USER_DBT table.

Create table query for USER_DBT can be seen below:

.. code-block:: sql
   :linenos:

    CREATE TABLE IF NOT EXISTS USER_DBT(
                   USERID SERIAL PRIMARY KEY,
                   USERFIRSTNAME VARCHAR(40),
                   USERLASTNAME VARCHAR(40),
                   USERUSERNAME VARCHAR(40) NOT NULL UNIQUE,
                   USERPASSWORD VARCHAR(40) NOT NULL,
                   USEREMAIL VARCHAR(60) NOT NULL UNIQUE,
                   USERTYPE INTEGER NOT NULL)

Insert, Update and Delete queries for USER_DBT are:


.. code-block:: sql
   :linenos:

   INSERT INTO USER_DBT(
                  USERFIRSTNAME,
                  USERLASTNAME,
                  USERUSERNAME,
                  USERPASSWORD,
                  USEREMAIL,
                  USERTYPE)
               VALUES (%s, %s, %s, %s, %s, %s) RETURNING USERID;

.. code-block:: sql
   :linenos:

   UPDATE USER_DBT SET USERFIRSTNAME = %s,
                       USERLASTNAME = %s,
                       USERUSERNAME = %s,
                       USERPASSWORD = %s,
                       USEREMAIL = %s
                 WHERE USERID = %s

.. code-block:: python
   :linenos:

   myQuery = "DELETE FROM USER_DBT WHERE USERID = " + str(userId)


%s parameters are filled with python format functions.
