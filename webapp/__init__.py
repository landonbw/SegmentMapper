from mimetypes import init
import os

from flask import Flask, request, g
import requests

def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )
    app.config['strava_client_id'] = os.environ['strava_client_id']
    app.config['strava_secret'] = os.environ['strava_secret']
    from webapp.database import init_db
    from webapp import auth
    from webapp import blog
    from webapp import rootbp
    from webapp import user
    from webapp import map
    init_db()
    app.register_blueprint(auth.bp)
    app.register_blueprint(blog.bp)
    app.register_blueprint(rootbp.bp)
    app.register_blueprint(user.bp)
    app.register_blueprint(map.bp)

    return app