from asyncio import format_helpers
from math import exp
from sqlalchemy import Column, Integer, String, DateTime, UnicodeText, Float
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship
from webapp.database import Base
import datetime as dt
from flask import current_app
import requests

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    name = Column(String(50), unique=True)
    email = Column(String(120), unique=True)
    password = Column(String(120), unique=True)
    color = Column(String(9))
    posts = relationship('Post', back_populates='author', cascade='all, delete-orphan')
    stravadetails = relationship('StravaDetails', back_populates='user', uselist=False)
    activities = relationship('Activity', back_populates='user', cascade='all, delete-orphan')
    efforts = relationship('Effort', back_populates='user', cascade='all, delete-orphan')
    

    def isauthenticated(self):
        if self.stravadetails:
            return True
        return False

    def __init__(self, name=None, email=None, password=None):
        self.name = name
        self.email = email
        self.password = password
        self.color = '#3009f480'

    def __repr__(self):
        return f'<User {self.name!r}>'

class Post(Base):
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    author_id = Column(Integer, ForeignKey("users.id"))
    created = Column(DateTime, default=dt.datetime.now)
    title = Column(String(100))
    body = Column(UnicodeText)
    author = relationship('User', back_populates="posts")

    def __init__(self, author, title, body):
        self.author = author
        self.title = title
        self.body = body

class StravaDetails(Base):
    __tablename__ = 'strava_auth'
    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id'))
    authorizationcode = Column(String(100))
    scope = Column(String(100))
    refresh_token = Column(String(100))
    access_token = Column(String(100))
    access_token_expiration_date = Column(DateTime)
    user = relationship('User', back_populates='stravadetails')
    

    def __init__(self, authcode, user, scope=None, reftoken=None, acctoken=None, expdate=None):
        self.authorizationcode = authcode
        self.user = user
        self.scope = scope
        self.refresh_token = reftoken
        self.access_token = acctoken
        self.access_token_expiration_date = expdate

    def athlete_info(self):
        pass

    def update_access_token(self, secret):
        url = f"https://www.strava.com/api/v3/oauth/token?client_id={self.id}&"\
            f"client_secret={secret}&grant_type=refresh_token&"\
            f"refresh_token={self.refresh_token}"
        response = requests.get(url).json()
        self.access_token=response['access_token']
        self.access_token_expiration_date=dt.datetime.fromtimestamp(response['expires_at'])
        self.refresh_token=response['refresh_token']
        return
        
    def get_access_token(self, secret):
        if dt.datetime.now() > self.access_token_expiration_date:
            self.update_access_token(secret)
        return self.access_token

class Activity(Base):
    __tablename__ = 'activities'
    id = Column(Integer, primary_key=True)
    name = Column(String(100))
    userid = Column(Integer, ForeignKey('users.id'))
    date = Column(DateTime)
    user = relationship('User', back_populates='activities')
    efforts = relationship('Effort', back_populates='activity', cascade='all, delete-orphan')
    distance = Column(Integer)
    movingtime = Column(Integer)

class Segment(Base):
    __tablename__ = 'segments'
    id = Column(Integer, primary_key=True)
    polyline = Column(String)
    name = Column(String)
    activityid = Column(Integer, ForeignKey('activities.id'))
    efforts = relationship('Effort', back_populates='segment', cascade='all, delete-orphan')
    distance = Column(Float)

    def fastest(self):
        times = [e.duration for e in self.efforts]
        best_efforts = [e for e in self.efforts if e.duration == min(times)]
        sorted_bests = sorted(best_efforts, key=lambda x: x.activity.date)
        return sorted_bests[0]

    def printpolyline(self):
        return self.polyline.__repr__()[1:-1]

class Effort(Base):
    __tablename__ = 'efforts'
    id = Column(Integer, primary_key=True)
    segment_id = Column(Integer, ForeignKey('segments.id'))
    segment = relationship('Segment', back_populates='efforts')
    userid = Column(Integer, ForeignKey('users.id'))
    user = relationship('User', back_populates='efforts')
    activity_id = Column(Integer, ForeignKey('activities.id'))
    activity = relationship('Activity', back_populates='efforts')
    duration = Column(Integer)

