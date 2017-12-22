Installation Guide
******************

Every team member has to install the following tools on their computers:

Git
===

Most Linux distributions already include “git” as a package, so you can install it
through the package manager. For other systems, visit https://git-scm.com/downloads.

We used:


.. code-block:: console

   sudo apt-get install git


Python
======

Python (version 3.4): Most Linux distributions already include “python3” as a package, so
you can install it through the package manager. For other systems, visit
https://www.python.org/downloads/.

We used:


.. code-block:: console

   sudo apt-get install python3.5


Flask
-----

On Linux, run the command “ sudo pip3 install -U flask ”. For other
systems, visit http://flask.pocoo.org/.

We used:


.. code-block:: console

   sudo pip3 install -U flask


.. raw:: latex

    \clearpage


Psycopg2
--------

On Linux, run the command “ sudo pip3 install -U psycopg2 ”. For
other systems, visit http://initd.org/psycopg/.

We used:


.. code-block:: console

   sudo pip3 install -U psycopg2


Sphinx
------

On Linux, run the command “ sudo pip3 install -U sphinx ”. For other
systems, visit http://sphinx-doc.org/.

We used:


.. code-block:: console

   sudo pip3 install -U sphinx


Eclipse
=======

Download it from https://www.eclipse.org/downloads/. Choose the
“Eclipse IDE for Java Developers” bundle. On Linux, it's safer NOT to use packages that
might be provided by the distribution.
Install the following plugins through the Eclipse Marketplace: PyDev, AnyEdit Tools,
HTML Editor, ReST Editor.

We Downloaded it from ecipse.org

P.S. Python Interpreter should be selected. In Eclipse follow the path: Window → Preferences → PyDev → Interpreters → Python Interpreter and select your interpreter.
