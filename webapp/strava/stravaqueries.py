
import requests
from flask import g, current_app
from webapp.strava.raw import _activity_lookup, _segment_effort, _segment_lookup, _activities

def user_token():
    return g.user.stravadetails.get_access_token(current_app.config['strava_secret'])

def run_query(func, pid):
    atoken = user_token()
    return func(pid, atoken)

def activity_lookup(aid):
    return run_query(_activity_lookup, aid)

def segment_lookup(sid):
    return run_query(_segment_lookup, sid)

def effort_lookup(eid):
    return run_query(_segment_effort, eid)

def user_activities(n, page):
    at = user_token()
    if g.user.activities:
        return _activities(n, page, at, before=g.user.earliest_activity().timestamp()) + _activities(n, page, at, after=g.user.latest_activity().timestamp())
    return _activities(n, page, at)

