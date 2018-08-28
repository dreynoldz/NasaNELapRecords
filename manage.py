# manage.py


import unittest

import coverage
from flask.cli import FlaskGroup

from project.server import create_app, db
from project.server.models import User, Track, Event, Sponsor
from datetime import date


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
    

    e1.tracks.append(t1)
    e2.tracks.append(t2)
    e3.tracks.append(t1)
    db.session.add_all([t1,t2])
    db.session.add_all([e1, e2, e3])
    db.session.add(s1)
    db.session.commit()
    print(e1.name)
    print(e1.tracks)
    print(e2.tracks)
    #pass


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



if __name__ == '__main__':
    cli()
