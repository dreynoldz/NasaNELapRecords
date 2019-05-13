# project/server/models.py


import datetime

from flask import current_app

from project.server import db, bcrypt
from sqlalchemy.inspection import inspect

TrackEvent = db.Table('TrackEvent',
    db.Column('trackId', db.Integer, db.ForeignKey('tracks.id')),
    db.Column('eventId', db.Integer, db.ForeignKey('events.id'))
)

RacerSponsor = db.Table('RacerSponsor',
    db.Column('racerId', db.Integer, db.ForeignKey('racers.id')),
    db.Column('sponsorId', db.Integer, db.ForeignKey('sponsors.id'))
)

CarRacer = db.Table('CarRacer',
    db.Column('carId', db.Integer, db.ForeignKey('cars.id')),
    db.Column('racerId', db.Integer, db.ForeignKey('racers.id'))
)

class ModelMixin:
    """Provide dict-like interface to db.Model subclasses."""

    def __getitem__(self, key):
        """Expose object attributes like dict values."""
        return getattr(self, key)

    def keys(self):
        """Identify what db columns we have."""
        return inspect(self).attrs.keys()

class Setting(db.Model, ModelMixin):

    __tablename__ = 'settings'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    value = db.Column(db.String(255), nullable=False)

class User(db.Model, ModelMixin):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    last_login = db.Column(db.DateTime, nullable=True)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    racer = db.relationship("Racer", uselist=False, backref='user')
    updated_date = db.Column(db.DateTime, nullable=True)


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
        return '{0}'.format(self.email)

class Track(db.Model, ModelMixin):

    __tablename__ = 'tracks'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    short_name = db.Column(db.String(255), nullable=False)
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)
    updated_date = db.Column(db.DateTime, nullable=True)
    #lap_distance = db.Column(db.Float)

    def __init__(self, name, short_name):
        self.name = name
        self.short_name = short_name
        self.created_date = datetime.datetime.now()
    
    def __repr__(self):
        return '{0}'.format(self.name)

class Event(db.Model, ModelMixin):
    
    __tablename__ = 'events'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    start_date = db.Column(db.Date, nullable=False)
    end_date = db.Column(db.Date, nullable=False)
    tracks = db.relationship('Track', secondary=TrackEvent, backref='events')
    laps = db.relationship('BestLap', backref='event')
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)
    updated_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, name, start_date, end_date):
        self.name = name
        self.start_date = start_date
        self.end_date = end_date
        self.created_date = datetime.datetime.now()
    
    def __repr__(self):
        return '{0}'.format(self.name)

class Sponsor(db.Model, ModelMixin):

    __tablename__ = 'sponsors'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255))
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)
    updated_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, name):
        self.name = name
        self.created_date = datetime.datetime.now()
    
    def __repr__(self):
        return '{0}'.format(self.name)

class RaceClass(db.Model, ModelMixin):

    __tablename__ = 'raceclasses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    short_name = db.Column(db.String(255), nullable=False)
    laps = db.relationship('BestLap', backref='raceclass')
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)
    updated_date = db.Column(db.DateTime, nullable=True)

    def __init__(self, name, short_name):
        self.name = name
        self.short_name = short_name
        self.created_date = datetime.datetime.now()
        
    
    def __repr__(self):
        return '{0}'.format(self.name)
    
class Car(db.Model, ModelMixin):

    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    make = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(255), nullable=False)
    racers = db.relationship('Racer', secondary=CarRacer, back_populates='cars')
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)
    updated_date = db.Column(db.DateTime, nullable=True)
    #racer_id = db.Column(db.Integer, ForeignKey('racers.id'))

    def __init__(self, make=None, model=None, year=None, color=None, number=None):
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.number = number
        self.created_date = datetime.datetime.now()
    
    def __repr__(self):
        return "#%s:%s_%s" % (self.number, self.make, self.model)
    
class Racer(db.Model, ModelMixin):

    __tablename__ = 'racers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    points = db.Column(db.Integer)
    cars = db.relationship('Car', secondary=CarRacer, back_populates='racers')
    sponsors = db.relationship('Sponsor', secondary=RacerSponsor, backref='racers')
    laps = db.relationship('BestLap', backref='racer')
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False)
    updated_date = db.Column(db.DateTime, nullable=True)
    #Picture

    def __init__(self, email, name, city, state, points):
        self.email = email
        self.name = name
        self.city = city
        self.state = state
        self.points = points
        self.created_date = datetime.datetime.now()
    
    def __repr__(self):
        return '{0}'.format(self.name)

class BestLap(db.Model, ModelMixin):

    __tablename__ = 'bestlaps'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, key='#')
    racer_id = db.Column(db.Integer, db.ForeignKey('racers.id'), nullable=False, key='Racer')
    raceclass_id = db.Column(db.Integer, db.ForeignKey('raceclasses.id'), nullable=False, key='Race Class')
    event_id = db.Column(db.Integer, db.ForeignKey('events.id'), nullable=False, key='Event')
    time = db.Column(db.Float, key='Lap Time')
    lap_date = db.Column(db.DateTime, nullable=True, key='Lap Date')
    best = db.Column(db.Boolean, nullable=False, default=False, key='Is Best?')
    created_date = db.Column(db.DateTime, default=datetime.datetime.utcnow(), nullable=False, key='Create Date')
    updated_date = db.Column(db.DateTime, nullable=True, key='Update Date')

    def __init__(self, racer_id, raceclass_id, event_id, time, lap_date, best=False):
        self.racer_id = racer_id
        self.raceclass_id = raceclass_id
        self.event_id = event_id
        self.time = time
        self.lap_date = lap_date
        self.best = best
        self.created_date = datetime.datetime.now()
    
    def get_id(self):
        return self.id
    
    def is_best(self):
        return self.best
    
    def __repr__(self):
        return "<BestLap(racer='%s', raceclass='%s', event='%s', time='%s')>" % (self.racer, self.raceclass, self.event, self.time)