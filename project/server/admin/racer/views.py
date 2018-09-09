# project/server/admin/racer/views.py

import sys, datetime
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required, current_user

from project.server import bcrypt, db
from project.server.models import Racer, Car, CarRacer, Sponsor, RacerSponsor
from project.server.admin.racer.forms import RacerForm

# Blueprints
admin_racer_blueprint = Blueprint('admin_racer', __name__,)

# Helper Functions


def get_racers():
    return db.session.query(Racer)

def get_cars():
    return db.session.query(Car)

def get_sponsors():
    return db.session.query(Sponsor)

def get_carChoices():
    cars = get_cars()
    car_list = [(0, "---")]
    [car_list.append((c.id, c.number + ' ' + c.make + ' ' + c.model)) for c in cars.order_by(Car.number).all()]
    print("car_list")
    print(car_list)
    return car_list

def get_sponsorChoices():
    sponsors = get_sponsors()
    sponsor_list = [(0, "---")]
    [sponsor_list.append((s.id, s.name)) for s in sponsors.order_by(Sponsor.name).all()]
    print("sponsor_list")
    print(sponsor_list)
    return sponsor_list

def remove_car_association(racer_id):
    racer = db.session.query(Racer).filter_by(id=racer_id)
    r = racer.first()
    carRacers = db.session.query(CarRacer).filter_by(racerId=racer_id).all()
    for carRacer in carRacers:
        car = db.session.query(Car).filter_by(id=carRacer.carId).first()
        r.cars.remove(car)

def remove_sponsor_association(racer_id):
    racer = db.session.query(Racer).filter_by(id=racer_id)
    r = racer.first()
    racerSponsors = db.session.query(RacerSponsor).filter_by(racerId=racer_id).all()
    for racerSponsor in racerSponsors:
        sponsor = db.session.query(Sponsor).filter_by(id=racerSponsor.sponsorId).first()
        r.sponsors.remove(sponsor)

def get_pghead():
    return 'Racers'

# Route Handlers

# Racer
@admin_racer_blueprint.route('/racer/main')
@login_required
def main():
    if current_user.is_admin():
        return render_template('admin/racer/main.html', racers=get_racers(), pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_racer_blueprint.route('/racer/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.is_admin():
        form = RacerForm(request.form)
        form.cars.choices = get_carChoices()
        form.sponsors.choices = get_sponsorChoices()

        if form.validate_on_submit():
            racer = Racer(
                email=form.email.data,
                name=form.name.data,
                city=form.city.data,
                state=form.state.data,
                points=form.points.data,
            )
            for c in form.cars.data:
                if c != 0:
                    car = db.session.query(Car).filter_by(id=c).first()
                    racer.cars.append(car)
            
            for s in form.sponsors.data:
                if s != 0:
                    sponsor = db.session.query(Sponsor).filter_by(id=s).first()
                    racer.sponsors.append(sponsor)

            db.session.add(racer)
            db.session.commit()

            flash('New racer created.', 'success')
            return redirect(url_for("admin_racer.main", pghead=get_pghead()))
        return render_template('admin/racer/create.html', form=form, pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger') 
        return redirect(url_for("user.members"))

@admin_racer_blueprint.route('/racer/update/<int:racer_id>/', methods=['GET', 'POST'])
@login_required
def update(racer_id):
    if current_user.is_admin():
        racer = Racer.query.filter_by(id=racer_id).first()
        form = RacerForm(request.form)
        form.cars.choices = get_carChoices()
        form.sponsors.choices = get_sponsorChoices()
        
        if form.validate_on_submit():
            racer.email = form.email.data
            racer.name = form.name.data
            racer.city = form.city.data
            racer.state = form.state.data
            racer.points = form.points.data

            for c in form.cars.data:
                if c != 0:
                    car = db.session.query(Car).filter_by(id=c).first()
                    racer.cars.append(car)
                else:
                    remove_car_association(racer_id)
                    cars=[]
            
            for s in form.sponsors.data:
                if s != 0:
                    sponsor = db.session.query(Sponsor).filter_by(id=s).first()
                    racer.sponsors.append(sponsor)
                else:
                    remove_sponsor_association(racer_id)
                    sponsors=[]
            racer.updated_date = datetime.datetime.now()
            db.session.commit()

            flash('Racer Updated.', 'success')
            return redirect(url_for("admin_racer.main", pghead=get_pghead()))
        
        if racer:
            form.email.data = racer.email
            form.name.data = racer.name
            form.city.data = racer.city
            form.state.data = racer.state
            form.points.data = racer.points

        return render_template('admin/racer/update.html', racer=racer, form=form, pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_racer_blueprint.route('/racer/delete/<int:racer_id>/')
@login_required
def delete(racer_id):
    if current_user.is_admin():
        racer = db.session.query(Racer).filter_by(id=racer_id)
        remove_car_association(racer_id)
        remove_sponsor_association(racer_id)
        racer.delete()
        db.session.commit()
        flash('The racer was deleted.', 'success')
        return redirect(url_for('admin_racer.main', pghead=get_pghead()))
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))