from flask import Blueprint, jsonify, Flask
from flask.globals import request
from click.types import STRING

from elifozer_dbmodels.newsdbo import News
from elifozer_dbhandler import newshandler
from elifozer_utilities.filterexpression import FilterExpression
from elifozer_utilities.filterparameter import FilterParameter
from elifozer_utilities.commonhelper import IsAuthenticated, GetUserIdSession, GetUsernameSession, IsAdmin


app = Flask(__name__)
newsoperationshelper = Blueprint('newsoperationshelper', __name__)


@newsoperationshelper.route('/addnews', methods=['GET', 'POST'])
def AddNews():
    if not IsAuthenticated():
        return jsonify("You must be logged in to add news")

    if not IsAdmin():
        return jsonify("You must have admin privileges to add news")

    news = News()

    news.title = request.args.get('addnews_title', "", type=STRING)
    news.content = request.args.get('addnews_content', "", type=STRING)

    imgUrl = request.args.get('addnews_imgUrl', "", type=STRING)

    if imgUrl != "":
        news.imgUrl = imgUrl

    validationMsg = news.IsValid()

    if validationMsg != "":
        return jsonify(validationMsg)

    news.createdBy = GetUsernameSession()

    newshandler.Insert(news)

    return jsonify("")