# project/server/models.py


import datetime

from flask import current_app

from project.server import db, bcrypt


class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)

    def __init__(self, email, password, admin=False):
        self.email = email
        self.password = bcrypt.generate_password_hash(
            password, current_app.config.get('BCRYPT_LOG_ROUNDS')
        ).decode('utf-8')
        self.registered_on = datetime.datetime.now()
        self.admin = admin

    def is_authenticated(self):
        return True

    def is_active(self):
        return True

    def is_anonymous(self):
        return False

    def get_id(self):
        return self.id
    
    def is_admin(self):
        return self.admin

    def __repr__(self):
        return '<User {0}>'.format(self.email)

TrackEvent = db.Table('TrackEvent',
    db.Column('trackId', db.Integer, db.ForeignKey('tracks.id')),
    db.Column('eventId', db.Integer, db.ForeignKey('events.id'))
)

class Track(db.Model):

    __tablename__ = 'tracks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    short_name = db.Column(db.String(255), nullable=False)
    #lap_distance = db.Column(db.Float)

    def __init__(self, name, short_name):
        self.name = name
        self.short_name = short_name
    
    def __repr__(self):
        return '<Track {0}>'.format(self.name)

class Event(db.Model):
    
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    tracks = db.relationship('Track', secondary=TrackEvent, backref='events')

    def __init__(self, name, start_date, end_date):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
    
    def __repr__(self):
        return '<Event {0}>'.format(self.name)

class Sponsor(db.Model):

    __tablename__ = 'sponsors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name
    
    def __repr__(self):
        return '<Sponsor {0}>'.format(self.name)