from flask import Blueprint, jsonify, Flask
from flask.globals import request
from click.types import STRING

from elifozer_dbmodels.newsdbo import News
from elifozer_dbhandler import newshandler, musicianhandler
from elifozer_utilities.filterexpression import FilterExpression
from elifozer_utilities.filterparameter import FilterParameter
from elifozer_utilities.commonhelper import IsAuthenticated, GetUserIdSession, IsAdmin


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

    musicianName = request.args.get('addnews_musician', "", type=STRING)

    musician = musicianhandler.GetByMusicianName(musicianName)
    news.musicianId = musician.musicianId

    imgUrl = request.args.get('addnews_imgUrl', "", type=STRING)

    if imgUrl != "":
        news.imgUrl = imgUrl

    validationMsg = news.IsValid()

    if validationMsg != "":
        return jsonify(validationMsg)

    news.createdBy = GetUserIdSession()

    newshandler.Insert(news)

    return jsonify("")


@newsoperationshelper.route('/deletenews', methods=['GET', 'POST'])
def DeleteNews():
    if not IsAuthenticated():
        return redirect('/')

    if not IsAdmin():
        return redirect('/')

    newsId = request.args.get('newsId', "", type=int)

    try:
        newshandler.Delete(newsId)

        return jsonify(True)
    except:
        return jsonify(False)