.. raw:: latex

    \newpage

Parts Implemented by Elif Özer
******************************

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

Select query can be found in the below function:

.. code-block:: python
   :linenos:

   def Get(filterExpression = None):
       connection, cursor = basehandler.DbConnect()

       myQuery = "SELECT * FROM USER_DBT"

       if filterExpression is None:
           cursor = basehandler.DbExecute(myQuery, connection, cursor)
       else:
           myQuery += filterExpression.GetWhere()
           cursor = basehandler.DbExecute(myQuery, connection, cursor, filterExpression.GetParameters())

       userList = []

       for user in cursor.fetchall():
           tempUser = User()

           tempUser.userId = user[0]
           tempUser.firstName = user[1]
           tempUser.lastName = user[2]
           tempUser.username = user[3]
           tempUser.password = user[4]
           tempUser.email = user[5]
           tempUser.userType = user[6]

           userList.append(tempUser)

       basehandler.DbClose(connection, cursor)

       return userList

FilterExpression class holds the list of column name, the operator and the operand. When we call GetWhere function, we use FilterExpression class to create a generic where contidion.
FilterParameter holds the column name, the operator and the operand. FilterExpression is a list of FilterParameters.

Register User
-------------

In order to register a new user, after user provides data via the interface and click the submit button, JavaScript combines this data. After combining,
AJAX request triggers our Python Code. JavaScript and Python codes can be seen below.

.. code-block:: javascript
   :linenos:

   function RegisterOperation()
   {
      $.getJSON('/register',
      {
         registerFirstName: $('input[name="registerFirstName"]').val(),
         registerLastName: $('input[name="registerLastName"]').val(),
         registerUsername: $('input[name="registerUsername"]').val(),
         registerEmail: $('input[name="registerEmail"]').val(),
         registerPassword: $('input[name="registerPassword"]').val()
      },
      function(data)
      {
         if(data !== "")
         {
            var modal = $('#userWarningModal');

            modal.find('#userWarningModalMsg').text(data);
            $('#userWarningModal').modal('show');
         }
         else
            window.location = "/home";
      });

      return false;
   }


.. code-block:: python
   :linenos:

   @useroperationshelper.route('/register', methods=['GET', 'POST'])
   def Register():
       if IsAuthenticated():
           return redirect('/')

       user = User()

       user.firstName = request.args.get('registerFirstName', "", type=STRING)
       user.lastName = request.args.get('registerLastName', "", type=STRING)
       user.username = request.args.get('registerUsername', "", type=STRING)
       user.email = request.args.get('registerEmail', "", type=STRING)
       user.password = request.args.get('registerPassword', "", type=STRING)
       user.userType = 2

       validationMessage = user.IsValid()

       if validationMessage != "":
           return jsonify(validationMessage)

       filterParameter = FilterParameter("USERUSERNAME", "LIKE", user.username)
       filterExpression = FilterExpression()
       filterExpression.AddParameter(filterParameter)
       users = userhandler.Get(filterExpression)

       if len(users) > 0:
           return jsonify("Username already exists")

       filterParameter = FilterParameter("USEREMAIL", "LIKE", user.email)
       filterExpression = FilterExpression()
       filterExpression.AddParameter(filterParameter)
       users = userhandler.Get(filterExpression)

       if len(users) > 0:
           return jsonify("Email already exists")

       user = userhandler.Insert(user)

       SetUserIdSession(user.userId)
       SetFullNameSession(user.firstName + " " + user.lastName)
       SetUsernameSession(user.username)

       return jsonify("")

Login User
----------

In order to login to our website, after registered user provides data via the interface and click the submit button, JavaScript combines this data. After combining,
AJAX request triggers our Python Code. JavaScript and Python codes can be seen below.

.. code-block:: javascript
   :linenos:

   function LoginOperation()
   {
      $.getJSON('/login',
      {
         loginUsernameEmail: $('input[name="loginUsernameEmail"]').val(),
         loginPassword: $('input[name="loginPassword"]').val()
      },
      function(data)
      {
         if(data == "")
            window.location = "/home";
         else
         {
            var modal = $('#userWarningModal');

            modal.find('#userWarningModalMsg').text(data);
            $('#userWarningModal').modal('show');
         }
      });

      return false;
   }


.. code-block:: python
   :linenos:

   @useroperationshelper.route('/login', methods=['GET', 'POST'])
   def Login():
       usernameEmail = request.args.get('loginUsernameEmail', "", type=STRING)
       user = userhandler.GetByUsernameOrEmail(usernameEmail)

       if user.userId == -1:
           return jsonify("Invalid username or e-mail")

       if user.password != request.args.get('loginPassword', "", type=STRING):
           return jsonify("Invalid password")

       SetUserIdSession(user.userId)
       SetFullNameSession(user.firstName + " " + user.lastName)
       SetUsernameSession(user.username)

       return jsonify("")

Users can log out using the dropdown menu on the upper right corner of the secret. Clicking this "logout" link will trigger the operation.

.. code-block:: python
   :linenos:

   @useroperationshelper.route('/logout', methods=['GET'])
   def Logout():
       SetUserIdSession(-1)
       SetFullNameSession("")
       SetUsernameSession("")

       return redirect('/')

User Settings
-------------

In this section (on user home page), the fields are filled with user's information. If user wants to change his/her information, he/she needs to provide new data. After the user provides new data and clicks the update button, AJAX call is made.
After this request, updated values will be updated in the database.

Also, removing a user from the database is triggered after user clicks the delete button.

Update and delete user functions can be seen below.

.. code-block:: python
   :linenos:

   @useroperationshelper.route('/updateuser', methods=['GET', 'POST'])
   def UpdateUser():
       if not IsAuthenticated():
           return redirect('/')

       try:
           user = User()

           user.firstName = request.args.get('usersettings_firstName', "", type=STRING)
           user.lastName = request.args.get('usersettings_lastName', "", type=STRING)
           user.username = request.args.get('usersettings_username', "", type=STRING)
           user.email = request.args.get('usersettings_email', "", type=STRING)
           user.password = request.args.get('usersettings_password', "", type=STRING)

           user.userId = GetUserIdSession()

           validationMessage = user.IsValid()

           if validationMessage != "":
               return jsonify(validationMessage)

           filterParameter = FilterParameter("USERUSERNAME", "LIKE", user.username)
           filterExpression = FilterExpression()
           filterExpression.AddParameter(filterParameter)
           users = userhandler.Get(filterExpression)

           if len(users) > 0 and users[0].userId != GetUserIdSession():
               return jsonify("This username is already taken")

           filterParameter = FilterParameter("USEREMAIL", "LIKE", user.email)
           filterExpression = FilterExpression()
           filterExpression.AddParameter(filterParameter)
           users = userhandler.Get(filterExpression)

           if len(users) > 0 and users[0].userId != GetUserIdSession():
               return jsonify("This e-mail address is already taken")

           userhandler.Update(user)
           SetUserIdSession(user.userId)
           SetFullNameSession(user.firstName + " " + user.lastName)
           SetUsernameSession(user.username)

           return jsonify("")
       except:
           return jsonify("Unexpected error occured")


.. code-block:: python
   :linenos:

   @useroperationshelper.route('/deleteuser', methods=['GET', 'POST'])
   def DeleteUser():
       if not IsAuthenticated():
           return redirect('/')

       try:
           userhandler.Delete(GetUserIdSession())
           SetUserIdSession(-1)
           SetFullNameSession("")
           SetUsernameSession("")

           return jsonify(True)
       except:
           return jsonify(False)


Musician Operations
===================

In this section, developments required for musician operations will be explained.


SQL
---

Information regarding musicians such as musician name, genre, establish year etc. kept in the database table MUSICIAN_DBT. This table also will be referenced by some tables that my project colleague worked on.

Create table query for MUSICIAN_DBT can be seen below:

.. code-block:: sql
   :linenos:

   CREATE TABLE IF NOT EXISTS MUSICIAN_DBT(
                          MUSICIANID SERIAL PRIMARY KEY,
                          MUSICIANNAME VARCHAR(40) UNIQUE NOT NULL,
                          MUSICIANGENRE VARCHAR(40),
                          MUSICIANESTYEAR VARCHAR(4) NOT NULL,
                          MUSICIANIMGURL VARCHAR(200),
                          MUSICIANDESC VARCHAR(300))


Insert, Update and Delete queries for MUSICIAN_DBT are:


.. code-block:: sql
   :linenos:

   INSERT INTO MUSICIAN_DBT(MUSICIANNAME,
                            MUSICIANGENRE,
                            MUSICIANESTYEAR,
                            MUSICIANIMGURL,
                            MUSICIANDESC)
                    VALUES (%s, %s, %s, %s, %s) RETURNING MUSICIANID;

.. code-block:: sql
   :linenos:

   UPDATE MUSICIAN_DBT SET MUSICIANNAME = %s,
                           MUSICIANGENRE = %s,
                           MUSICIANESTYEAR = %s,
                           MUSICIANIMGURL = %s,
                           MUSICIANDESC = %s
                    WHERE MUSICIANID = %s

.. code-block:: python
   :linenos:

   myQuery = "DELETE FROM MUSICIAN_DBT WHERE MUSICIANID = " + str(musicianId)


%s parameters are filled with python format functions.

Select query is performed for MUSICIAN_DBT like the user's select query with FilterExpression class generically. Select query can be seen below.

.. code-block:: sql
   :linenos:

   def Get(filterExpression = None):
       connection, cursor = basehandler.DbConnect()

       myQuery = "SELECT * FROM MUSICIAN_DBT"

       if filterExpression is None:
           cursor = basehandler.DbExecute(myQuery, connection, cursor)
       else:
           myQuery += filterExpression.GetWhere()
           cursor = basehandler.DbExecute(myQuery, connection, cursor, filterExpression.GetParameters())

       musicianList = []

       for musician in cursor.fetchall():
           tempMusician = Musician()

           tempMusician.musicianId = musician[0]
           tempMusician.name = musician[1]
           tempMusician.genre = musician[2]
           tempMusician.establishYear = musician[3]
           tempMusician.imgUrl = musician[4]
           tempMusician.description = musician[5]

           musicianList.append(tempMusician)

       basehandler.DbClose(connection, cursor)

       return musicianList

Add Musician
------------

This is strictly an admin privilege. After logining in and entering the musician page, admins face across with a section that lets them add new musicians. When they fill the text areas with the regarding information and clicking the add button,
JavaScript function will be triggered. This function collects whole data into a musician class. After object construction, AJAX request rises and sends this information to the server
side. Server side captures the object and after various validations (such as information being not null etc.), if data is valid, insert operation will be successfully executed.

Created JavaScript funcion and the AJAX call are:

.. code-block:: javascript
   :linenos:

   function AddMusician()
   {
      var desc = document.getElementById("musicianadd_musicianDesc");

      $.getJSON('/addmusician',
      {
         musicianadd_musicianName: $('input[name="musicianadd_musicianName"]').val(),
         musicianadd_musicianGenre: $('input[name="musicianadd_musicianGenre"]').val(),
         musicianadd_musicianEstYear: $('input[name="musicianadd_musicianEstYear"]').val(),
         musicianadd_musicianImgUrl: $('input[name="musicianadd_musicianImgUrl"]').val(),
         musicianadd_musicianDesc: desc.value
      },
      function(data)
      {
         if(data == "")
            location.reload();
         else
         {
            CustomAlert(data);
         }
      });

      return false;
   }

Server side codes can be seen below.

.. code-block:: python
   :linenos:

   @musicianoperationshelper.route('/addmusician', methods=['GET', 'POST'])
   def AddMusician():
       if not IsAuthenticated():
           return jsonify("You must be logged in to add a musician")

       if not IsAdmin():
           return jsonify("You must have admin privileges to add a musician")

       musician = Musician()

       musician.name = request.args.get('musicianadd_musicianName', "", type=STRING)
       musician.genre = request.args.get('musicianadd_musicianGenre', "", type=STRING)
       musician.establishYear = request.args.get('musicianadd_musicianEstYear', "", type=STRING)

       imgUrl = request.args.get('musicianadd_musicianImgUrl', "", type=STRING)

       if imgUrl != "":
           musician.imgUrl = imgUrl

       musician.description = request.args.get('musicianadd_musicianDesc', "", type=STRING)

       filterParameter = FilterParameter("MUSICIANNAME", "LIKE", musician.name)
       filterExpression = FilterExpression()
       filterExpression.AddParameter(filterParameter)

       musicians = musicianhandler.Get(filterExpression)

       if len(musicians) > 0:
           return jsonify("This musician already exists")

       if len(musician.establishYear) != 4 and not musician.establishYear.isdigit():
           return jsonify("Establish year must consist of 4 digits")

       if int(musician.establishYear) < 1800:
           return jsonify("Establish year must be bigger than 1800")

       musicianhandler.Insert(musician)

       return jsonify("")

Update Musician
---------------

Admins can update musician information. After clicking the update button for a specific musician, admins can change the information for the musicians. After clicking submit,
the changes that are done are sent to server side by AJAX call. On server side, with the help of the python code, changes are applied to the database if there are no restrictions. If admins desire to change the musician name however, the musician name must be new to the database.

.. code-block:: python
   :linenos:

   @musicianoperationshelper.route('/updatemusician', methods=['GET', 'POST'])
   def UpdateMusician():
       if not IsAuthenticated():
           return jsonify("You must be logged in to update a musician")

       if not IsAdmin():
           return jsonify("You must have admin privileges to update a musician")

       musicianId = request.args.get('musicianId', "", type=int)
       name = request.args.get('name', "", type=STRING)
       genre = request.args.get('genre', "", type=STRING)
       establishYear = request.args.get('establishYear', "", type=STRING)
       imgUrl = request.args.get('imgUrl', "", type=STRING)
       description = request.args.get('description', "", type=STRING)

       filterParameter1 = FilterParameter("MUSICIANNAME", "LIKE", name)

       filterExpression = FilterExpression()
       filterExpression.AddParameter(filterParameter1)

       musicianList = musicianhandler.Get(filterExpression)

       if len(musicianList) > 0:
           return jsonify("This musician already exists. Enter a different musician name.")

       musician = musicianhandler.GetByID(musicianId)

       musician.name = name
       musician.genre = genre
       musician.establishYear = establishYear
       musician.imgUrl = imgUrl
       musician.description = description

       musicianhandler.Update(musician)

       return jsonify("")


Delete Musician
---------------

Admins can delete any musician. After clicking the delete button for a specific musician, admins can delete
the message. After clicking submit, the changes that are done are sent to server side by AJAX call. On server side, with the help of the python code, that musician
is removed from the database.

.. code-block:: python
   :linenos:

   @musicianoperationshelper.route('/deletemusician', methods=['GET', 'POST'])
   def DeleteMusician():
       if not IsAuthenticated():
           return redirect('/')

       if not IsAdmin():
           return redirect('/')

       musicianId = request.args.get('musicianId', "", type=int)

       try:
           musicianhandler.Delete(musicianId)

           return jsonify(True)
       except:
           return jsonify(False)

Showing Musicians
-----------------

Any user type can see the musicians. Showing musician is implemented on musicians page. On this page, all musicians are shown in a list form for everyone. Also, musicians can be searched. When searching, they are filtered by containing the musician name.
When showing, all musicians (or searched musicians) are ordered alphabetically.

All musicians in the database are shown if there are no search data is provided. The filtering is done in the below code:

.. code-block:: python
   :linenos:

   @musicianoperations.route('/musicians', methods=['GET'])
   def Musicians():
       searchBy = request.args.get('searchBy', "", type=STRING)

       filterParameter = FilterParameter("MUSICIANNAME", "LIKE", "%" + searchBy + "%")
       filterExpression = FilterExpression()
       filterExpression.AddParameter(filterParameter)

       musicianList = musicianhandler.Get(filterExpression)

       return render_template('musicians.html', musicianList = musicianList, authenticated = IsAuthenticated(), admin = IsAdmin(), fullName = GetFullNameSession())

Login users can also trigger a collapsed area about the musicians. This area will provide detailed musician information. If it is not a logged in user, only the musician list (not in clickable form) will be shows. Collapse area for the musician information section is applied by checking if the user is authenticated.

Musicians on the musician page are shown by the following html code:

.. code-block:: html
   :linenos:

   <section id="musicianListSection" style="margin-top: 40px;">
   <ul class="list-group">
      {% for m in musicianList|sort(attribute="name") %}
      <table>
         <tr>
            <td>
               <li class="list-group-item" {% if not authenticated %} style="width: 600px;" {% endif %} {% if authenticated %} style="width: 600px; cursor: pointer;" data-toggle="collapse" data-target='#{{ loop.index }}' {% endif %}>{{ m.name }}</li>
            </td>

            {% if admin %}
            <td style="padding-left: 20px;">
               <button class="glyphicon-button update" value="{{ m.musicianId }}" data-toggle="modal" data-target="#updateMusicianModal"
                     onclick="return UpdateMusicianModal({{ m.musicianId }}, '{{ m.name }}', '{{ m.genre }}', '{{ m.establishYear }}', '{{ m.imgUrl }}', '{{ m.description }}');">

                  <span class="glyphicon glyphicon-pencil"></span>
               </button>
            </td>

            <td>
               <button class='glyphicon-button delete' value="{{ m.musicianId }}" data-toggle="modal" data-target="#deleteMusicianModal"
                     onclick='return DeleteMusicianModal({{ m.musicianId }});'>

                  <span class="glyphicon glyphicon-trash"></span>
               </button>
            </td>
            {% endif %}
         </tr>
      </table>

      <div class="collapse" id={{ loop.index }}>
         <div class="media list-group-item" style="margin: 15px 0 15px 0; margin-left: 100px; width: 600px; background: #d5d38f;">
            <div class="media-left">
               <img class="media-object" src="{{ m.imgUrl }}" height="64" width="64">
            </div>

            <div class="media-body">
               <p class="media-heading"><strong>Genre: </strong>{{ m.genre }}</p>
               <p class="media-heading"><strong>Establish Year: </strong>{{ m.establishYear }}</p>
               <p style="margin-top: 26px; word-break: break-all;">{{ m.description }}</p>
            </div>
         </div>
      </div>
      {% endfor %}
   </ul>
   </section>