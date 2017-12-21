.. raw:: latex

    \newpage

Parts Implemented by Elif Özer
==============================

In this part, 3 major parts will be explained. These parts are User Operations, Musician Operations and News Operations. In each part,
related SQL tables, SQL queries, Python codes and JavaScript methods will be explained.

You can see the ER diagram for the parts implemented by Elif Özer below:

.. figure:: ../images/1.*
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