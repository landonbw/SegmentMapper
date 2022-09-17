from argparse import ArgumentError
from curses.ascii import US
import functools
from flask import Blueprint, flash, redirect
from flask import render_template, request, session
from flask import current_app, url_for, g
import datetime as dt

from werkzeug.security import check_password_hash, generate_password_hash

from webapp.models import User, Activity, Segment, Effort
from webapp.database import db_session
from webapp.auth import login_required
from webapp.strava.stravaqueries import user_activities, activity_lookup, segment_lookup, effort_lookup

bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/')
@login_required
def user_screen():
    return render_template('user/user.html')

@bp.route('/color', methods=['GET', 'POST'])
@login_required
def color():
    if request.method == 'GET':
        return {color: g.user.color}
    if request.method == 'POST':
        newcolor = request.json.get('color')
        if newcolor:
            g.user.color = newcolor + '80' 
            db_session.commit()
        return {'color': g.user.color}

@bp.route('/pulldata')
@login_required
def pulldata():
    if g.user.activities:
        n = 50
    else:
        n = 100
    activities = user_activities(n=n, page=1)
    for i, act in enumerate(activities):
        act_obj = db_session.merge(Activity(id=act['id']))
        print(i, act_obj.id)
        actinfo = activity_lookup(act_obj.id)
        act_obj.distance = actinfo['distance']
        act_obj.movingtime = actinfo['moving_time']
        act_obj.name = actinfo['name']
        act_obj.date = dt.datetime.fromisoformat(actinfo['start_date'][:-1])
        for effort in actinfo['segment_efforts']:
            segment = db_session.merge(Segment(id=effort['segment']['id']))
            segment.distance = effort['segment']['distance']
            if not segment.polyline or not segment.name:
                segmentinfo = segment_lookup(segment.id)
                segment.polyline = segmentinfo['map']['polyline']
                segment.name = segmentinfo['name']
            effortobj = db_session.merge(Effort(id=effort['id'], duration=effort['moving_time']))
            effortobj.user = g.user
            effortobj.activity = act_obj
            segment.efforts.append(effortobj)
            db_session.commit()

        g.user.activities.append(act_obj)
        db_session.commit()
    activities = [a.name for a in g.user.activities]
    return activities
    # 

@bp.route('/activity_bounds')
@login_required
def activity_bounds():
    user = g.user
    return {'earliest_activity':user.earliest_activity(), 'latest_activity':user.latest_activity()}
