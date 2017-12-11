from flask import Blueprint, render_template, Flask, request
from flask.globals import request
from click.types import STRING

from bozova_dbmodels.concert_areadbo import Concert_area
from bozova_dbhandler import concert_areahandler
from elifozer_utilities.filterexpression import FilterExpression
from elifozer_utilities.filterparameter import FilterParameter
from elifozer_utilities.commonhelper import IsAuthenticated, GetUserIdSession, GetFullNameSession, GetUsernameSession, IsAdmin


app = Flask(__name__)
concert_areaoperationshelper = Blueprint('concert_areaoperationshelper', __name__)


@concert_areaoperationshelper.route('/addconcert_area', methods=['GET', 'POST'])
def AddConcert_area():
    if not IsAuthenticated():
        return jsonify("You must be logged in to add a concert area")

    if not IsAdmin():
        return jsonify("You must have admin privileges to add a concert area")

    concert_area = Concert_area()

    concert_area.name = request.args.get('concert_areaadd_concert_areaName', "", type=STRING)
    concert_area.address = request.args.get('concert_areaadd_concert_areaaddress', "", type=STRING)
    concert_area.capacity = request.args.get('concert_areaadd_concert_areacapacity', "", type=STRING)


    filterParameter = FilterParameter("CONCERT_AREANAME", "LIKE", concert_area.name)
    filterExpression = FilterExpression()
    filterExpression.AddParameter(filterParameter)

    concert_area = concert_areahandler.Get(filterExpression)

    if len(concert_area) > 0:
        return jsonify("This concert area already exists")

    if len(concert_area.capacity) != 7 and not musician.establishYear.isdigit():
        return jsonify("Concert area's capacity cannot be equal or bigger than 1000000")


    concert_areahandler.Insert(concert_area)

    return jsonify("")

@concert_areaoperationshelper.route('/updateconcert_area', methods=['GET', 'POST'])
def UpdateMusician():
    if not IsAuthenticated():
        return jsonify("You must be logged in to update a concert area")

    if not IsAdmin():
        return jsonify("You must have admin privileges to update a concert area")

    concert_areaId = request.args.get('concert_areaId', "", type=int)
    name = request.args.get('name', "", type=STRING)
    address = request.args.get('address', "", type=STRING)
    date = request.args.get('date', "", type=STRING)

    filterParameter1 = FilterParameter("CONCERT_AREANAME", "LIKE", name)

    filterExpression = FilterExpression()
    filterExpression.AddParameter(filterParameter1)

    concert_areaList = concert_areahandler.Get(filterExpression)

    if len(musicianList) > 0:
        return jsonify("This musician already exists. Enter a different musician name.")

    concert_area = concert_areahandler.GetByID(concert_areaId)

    concert_area.name = name
    concert_area.address = address
    concert_area.capacity = capacity

    concert_areahandler.Update(concert_area)

    return jsonify("")


@concert_areaoperationshelper.route('/deleteconcert_area', methods=['GET', 'POST'])
def DeleteConcert_area():
    if not IsAuthenticated():
        return redirect('/')

    if not IsAdmin():
        return redirect('/')

    concert_areaId = request.args.get('concert_areaId', "", type=int)

    try:
        concert_areahandler.Delete(concert_areaId)

        return jsonify(True)
    except:
        return jsonify(False)