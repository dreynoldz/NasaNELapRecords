# manage.py


import unittest

import coverage
from flask.cli import FlaskGroup

from project.server import create_app, db
from project.server.config import SiteSetting
from project.server.models import Setting, User, Track, Event, Sponsor, RaceClass, Car, Racer, BestLap
from project.server.dataservices import DataServices, UIServices
from datetime import date
from sqlalchemy.ext.serializer import loads, dumps


app = create_app()
cli = FlaskGroup(create_app=create_app)

# code coverage
COV = coverage.coverage(
    branch=True,
    include='project/*',
    omit=[
        'project/tests/*',
        'project/server/config.py',
        'project/server/*/__init__.py'
    ]
)
COV.start()

@cli.command()
def create_db():
    db.drop_all()
    db.create_all()
    db.session.commit()


@cli.command()
def drop_db():
    """Drops the db tables."""
    db.drop_all()


@cli.command()
def create_admin():
    """Creates the admin user."""
    db.session.add(User(email='ad@min.com', password='nyc2000nyc', admin=True))
    db.session.commit()


@cli.command()
def create_data():
    """Creates sample data."""    
    t1 = Track(name='Watkins Glen International', short_name='WGI')
    t2 = Track(name='Pocono South-East', short_name="POCSE")
    
    e1 = Event(name='Summer Sizzle 2018', start_date = date(2018, 8, 27), end_date=date(2018, 8, 28))
    e2 = Event(name='MPACT', start_date = date(2018, 8, 11), end_date=date(2018, 8, 11))
    e3 = Event(name='Thunder at the Glen', start_date = date(2018, 9, 28), end_date=date(2018, 9, 30))

    s1 = Sponsor(name='AVB Design')
    rc1 = RaceClass(name='Honda Challenge 1', short_name='Honda Chal 1')
    c1 = Car(make='Volkswagen', model='Cabriolet', year='1992', color='Inca Blue', number='724')
    r1 = Racer(email='Aaron@van-blar.com', name='AVB', city='Bayonne', state='NJ', points=100)
    
    
    e1.tracks.append(t1)
    e2.tracks.append(t2)
    e3.tracks.append(t1)
    r1.cars.append(c1)
    r1.sponsors.append(s1)    
    db.session.add_all([t1,t2])
    db.session.add_all([e1, e2, e3])
    db.session.add(s1)
    db.session.add(rc1)
    db.session.add(c1)
    db.session.add(r1)
    db.session.commit()
    bl = BestLap(racer_id=r1.id, raceclass_id=rc1.id, event_id=e3.id, time=60.0, best=True, lap_date = date(2018, 10, 14))
    db.session.add(bl)
    db.session.commit()
    print(e1.name)
    print(e1.tracks)
    print(e2.tracks)
    print(r1.cars)
    print(bl.racer.cars)
    #pass

@cli.command()
def create_settings():
    """Creates site settings."""
    settings = SiteSetting()
    for setting in dir(settings):
        if not setting.startswith('__') and not callable(getattr(settings,setting)):
            db.session.add(Setting(name=setting, value=getattr(settings,setting)))
            print(setting,"=",getattr(settings,setting))
    db.session.commit()
    
@cli.command()
def test():
    """Runs the unit tests without test coverage."""
    tests = unittest.TestLoader().discover('project/tests', pattern='test*.py')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        return 0
    return 1


@cli.command()
def cov():
    """Runs the unit tests with coverage."""
    tests = unittest.TestLoader().discover('project/tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if result.wasSuccessful():
        COV.stop()
        COV.save()
        print('Coverage Summary:')
        COV.report()
        COV.html_report()
        COV.erase()
        return 0
    return 1

@cli.command()
def get_test():
    model_name = 'Track'
    d = DataServices.get_filter(eval(model_name),'id', 2, True)
    print(d)
    return 0


if __name__ == '__main__':
    cli()
