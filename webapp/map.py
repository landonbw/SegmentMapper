
from flask import Blueprint, flash, g, redirect
from flask import render_template, request, url_for, current_app

from werkzeug.exceptions import abort

from webapp.auth import login_required
from webapp.database import db_session
from webapp.models import Segment
import requests
import json
from sqlalchemy import select

bp = Blueprint('map', __name__)

@bp.route('/map')
@login_required
def index():
    # id = 7661747970
    # sid = 4386861
    # aid = 7690107756
    # # url = f"https://www.strava.com/api/v3/activities/{id}?access_token={g.user.stravadetails.access_token}"
    # atoken = g.user.stravadetails.get_access_token(current_app.config['strava_secret'])
    # url = f"https://www.strava.com/api/v3/activities/{aid}?access_token={atoken}"
    # segment = requests.get(url)
    # paths = []
    # if segment.status_code == 200:
    #     dat = segment.json()
    #     line = dat['map']['polyline']
    #     paths.append(line)

    segments = db_session.execute(select(Segment)).all()
    return render_template('map/map.html', segments=segments)

    # return render_template('map/map.html', paths=paths[0].__repr__()[1:-1])
@bp.route('/mapsegments')
@login_required
def mapsegments():
    segments = db_session.execute(select(Segment)).scalars().all()
    ret = []
    for s in segments:
        best = s.fastest()
        d = {'id':s.id, 'line':s.polyline, 'name':s.name, 'min': best.duration, 
        # 'color':'#9e12f380'}
        'color': best.user.color}
        ret.append(d)
    return ret    