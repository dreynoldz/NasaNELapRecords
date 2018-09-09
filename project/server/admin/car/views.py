# project/server/admin/car/views.py

import sys, datetime
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required, current_user

from project.server import bcrypt, db
from project.server.models import Car, CarRacer, Racer
from project.server.admin.car.forms import CarForm

# Blueprints
admin_car_blueprint = Blueprint('admin_car', __name__,)

# Helper Functions
def get_cars():
    return db.session.query(Car)

def get_pghead():
    return 'Cars'

# Route Handlers

# Car
@admin_car_blueprint.route('/car/main')
@login_required
def main():
    if current_user.is_admin():
        return render_template('admin/car/main.html', cars=get_cars(), pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_car_blueprint.route('/car/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.is_admin():
        form = CarForm(request.form)

        if form.validate_on_submit():
            car = Car(
                make=form.make.data,
                model=form.model.data,
                year=form.year.data,
                color=form.color.data,
                number=form.number.data
            )
            db.session.add(car)
            db.session.commit()

            flash('New car created.', 'success')
            return redirect(url_for("admin_car.main", pghead=get_pghead()))
        return render_template('admin/car/create.html', form=form, pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger') 
        return redirect(url_for("user.members"))

@admin_car_blueprint.route('/car/update/<int:car_id>/', methods=['GET', 'POST'])
@login_required
def update(car_id):
    if current_user.is_admin():
        car = Car.query.filter_by(id=car_id).first()
        form = CarForm(request.form)

        if form.validate_on_submit():
            car.make = form.make.data
            car.model = form.model.data
            car.year = form.year.data
            car.color = form.color.data
            car.number = form.number.data
            car.updated_date = datetime.datetime.now()
            db.session.commit()

            flash('Car Updated.', 'success')
            return redirect(url_for("admin_car.main", pghead=get_pghead()))
        
        if car:
            form.make.data = car.make
            form.model.data = car.model
            form.year.data = car.year
            form.color.data = car.color
            form.number.data = car.number

        return render_template('admin/car/update.html', car=car, form=form, pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_car_blueprint.route('/car/delete/<int:car_id>/')
@login_required
def delete(car_id):
    if current_user.is_admin():
        car = db.session.query(Car).filter_by(id=car_id)
        c = car.first()
        carRacers = db.session.query(CarRacer).filter_by(carId=car_id).all()
        for carRacer in carRacers:
            racer = db.session.query(Racer).filter_by(id=carRacer.racerId).first()
            t.racers.remove(racer)
        track.delete()
        db.session.commit()
        flash('The car was deleted.', 'success')
        return redirect(url_for('admin_car.main', pghead=get_pghead()))
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))