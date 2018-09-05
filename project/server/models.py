# project/server/models.py


import datetime

from flask import current_app

from project.server import db, bcrypt

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

class User(db.Model):

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    registered_on = db.Column(db.DateTime, nullable=False)
    admin = db.Column(db.Boolean, nullable=False, default=False)
    racer = db.relationship("Racer", back_populates='user')


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

class RaceClass(db.Model):

    __tablename__ = 'raceclasses'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(255), nullable=False)
    short_name = db.Column(db.String(255), nullable=False)

    def __init__(self, name, short_name):
        self.name = name
        self.short_name = short_name
    
    def __repr__(self):
        return '<RaceClass {0}>'.format(self.name)
    
class Car(db.Model):

    __tablename__ = 'cars'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    make = db.Column(db.String(255), nullable=False)
    model = db.Column(db.String(255), nullable=False)
    year = db.Column(db.String(255), nullable=False)
    color = db.Column(db.String(255), nullable=False)
    number = db.Column(db.String(255), nullable=False)
    racers = db.relationship('Racer', secondary=CarRacer, back_populates='cars')
    #racer_id = db.Column(db.Integer, ForeignKey('racers.id'))

    def __init__(self, make=None, model=None, year=None, color=None, number=None):
        self.make = make
        self.model = model
        self.year = year
        self.color = color
        self.number = number
    
    def __repr__(self):
        return "<Car(make='%s', model='%s', number='%s')>" % (self.make, self.model, self.number)
    
class Racer(db.Model):

    __tablename__ = 'racers'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(255), unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    user = db.relationship("User", uselist=False, back_populates="racer")
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    points = db.Column(db.Integer)
    cars = db.relationship('Car', secondary=CarRacer, back_populates='racers')
    sponsors = db.relationship('Sponsor', secondary=RacerSponsor, backref='racers')
    #Picture

    def __init__(self, email, name, city, state, points):
        self.email = email
        self.name = name
        self.city = city
        self.state = state
        self.points = points
    
    def __repr__(self):
        return '<Racer {0}>'.format(self.name)
