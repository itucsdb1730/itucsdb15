from flask import Blueprint, jsonify, Flask
from flask.globals import request
from click.types import STRING

from elifozer_dbmodels.musiciandbo import Musician
from elifozer_dbhandler import musicianhandler
from elifozer_utilities.filterexpression import FilterExpression
from elifozer_utilities.filterparameter import FilterParameter
from elifozer_utilities.commonhelper import IsAuthenticated, GetUserIdSession, IsAdmin


app = Flask(__name__)
musicianoperationshelper = Blueprint('musicianoperationshelper', __name__)


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