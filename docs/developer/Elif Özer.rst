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