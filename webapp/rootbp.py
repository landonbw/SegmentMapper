from argparse import ArgumentError
from curses.ascii import US
import functools
from flask import Blueprint, flash, redirect
from flask import render_template, request, session
from flask import current_app, url_for, g

from werkzeug.security import check_password_hash, generate_password_hash

from webapp.models import StravaDetails, Activity, Segment, Effort
from webapp.auth import login_required
from webapp.database import db_session
import requests
import datetime as dt
from webapp.strava.stravaqueries import user_activities, activity_lookup, segment_lookup, effort_lookup


bp = Blueprint('rootbp', __name__, url_prefix='')

@bp.route('/exchange_token')
@login_required
def exchange_token():
    token = request.args.get('code')
    scope = request.args.get('scope')
    if token and scope:
        details = StravaDetails(authcode=token, scope=scope, user=g.user)
        db_session.add(details)
        try:
            url = 'https://www.strava.com/oauth/token'
            params = {'client_id':current_app.config['strava_client_id'],
                    'client_secret':current_app.config['strava_secret'],
                    'code':token,
                    'grant_type':'authorization_code'}
            response = requests.post(url, params=params)
            code = response.json()
            details.refresh_token = code['refresh_token']
            details.access_token = code['access_token']
            details.access_token_expiration_date = dt.datetime.fromtimestamp(code['expires_at'])
            db_session.commit()
        except:
            pass
    return redirect(url_for('user.user_screen'))

@bp.route("/")
def index():
    if g.user:
        return redirect(url_for('user.user_screen'))
    return redirect(url_for('auth.register'))

