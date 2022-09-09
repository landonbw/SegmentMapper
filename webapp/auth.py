from argparse import ArgumentError
from curses.ascii import US
import functools
from flask import Blueprint, flash, redirect
from flask import render_template, request, session
from flask import current_app, url_for, g

from werkzeug.security import check_password_hash, generate_password_hash

from webapp.models import User
from webapp.database import db_session

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = User.query.filter(User.id==user_id).first()


@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        error = None
        if not username:
            error = "Username is required"
        elif not password:
            error = "Password is required."
        if error is None:
            newuser = User(username, email, generate_password_hash(password))
            try:
                db_session.add(newuser)
                db_session.commit()
                error = "stored user"
            except Exception as e:
                error = f"User {username} is already registered"
                raise e
            else:
                return redirect(url_for("auth.login"))
        flash(error)
    return render_template(f'auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        error = None
        user = User.query.filter(User.name==username).first()
        if user is None:
            error = "Unknown username."
        elif not check_password_hash(user.password, password):
            error = "Incorrect password."
        if error is None:
            session.clear()
            session['user_id'] = user.id
            return redirect(url_for('blog.index'))
        
        flash(error)
    return render_template('auth/login.html')

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('blog.index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))
        return view(**kwargs)
    return wrapped_view

@bp.route('/strava')
def authorize_strava():
    authurl = f"http://www.strava.com/oauth/authorize?client_id={current_app.config['strava_client_id']}&response_type=code&redirect_uri=http://localhost/exchange_token&approval_prompt=force&scope=read_all,profile:read_all,activity:read_all"
    return redirect(authurl)