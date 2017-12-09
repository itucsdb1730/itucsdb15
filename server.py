import datetime
import json
import os
import re
from flask import Flask
from flask import render_template
from flask import request

from elifozer_dbhandler import basehandler, musicianhandler
from elifozer_operations.useroperations import useroperations
from elifozer_operations.useroperationshelper import useroperationshelper
from elifozer_operations.musicianoperations import musicianoperations
from elifozer_operations.musicianoperationshelper import musicianoperationshelper
from elifozer_operations.newsoperations import newsoperations
from elifozer_operations.newsoperationshelper import newsoperationshelper
from elifozer_utilities.currentconfig import CurrentConfig
from elifozer_utilities.commonhelper import IsAuthenticated, GetFullNameSession, IsAdmin

app = Flask(__name__)
app.secret_key = 'secretKey'
app.register_blueprint(useroperations)
app.register_blueprint(useroperationshelper)
app.register_blueprint(musicianoperations)
app.register_blueprint(musicianoperationshelper)
app.register_blueprint(newsoperations)
app.register_blueprint(newsoperationshelper)


def get_elephantsql_dsn(vcap_services):
    """Returns the data source name for ElephantSQL."""
    parsed = json.loads(vcap_services)
    uri = parsed["elephantsql"][0]["credentials"]["uri"]
    match = re.match('postgres://(.*?):(.*?)@(.*?)(:(\d+))?/(.*)', uri)
    user, password, host, _, port, dbname = match.groups()
    dsn = """user='{}' password='{}' host='{}' port={}
             dbname='{}'""".format(user, password, host, port, dbname)

    return dsn


@app.route('/', methods=['GET', 'POST'])
def home_page():
    if request.method == 'GET':
        now = datetime.datetime.now()

        return render_template('intro.html', current_time=now.ctime(), authenticated = IsAuthenticated(), fullName = GetFullNameSession())


if __name__ == '__main__':
    VCAP_APP_PORT = os.getenv('VCAP_APP_PORT')

    if VCAP_APP_PORT is not None:
        port, debug = int(VCAP_APP_PORT), False
    else:
        port, debug = 5000, True

    VCAP_SERVICES = os.getenv('VCAP_SERVICES')

    if VCAP_SERVICES is not None:
        app.config['dsn'] = get_elephantsql_dsn(VCAP_SERVICES)
    else:
        app.config['dsn'] = """user='vagrant' password='vagrant'
                               host='localhost' port=5432 dbname='itucsdb'"""

    CurrentConfig.appConfig = app.config['dsn']
    basehandler.DbInitialize()
    app.run(host='0.0.0.0', port=port, debug=debug)
