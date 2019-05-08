# project/server/admin/bestlap/views.py

import sys, datetime
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request, jsonify
from flask_login import login_required, current_user

from project.server import bcrypt, db
from project.server.models import BestLap, RaceClass, Event
from project.server.dataservices import DataServices, UIServices
from project.server.admin.bestlap.forms import BestLapForm

# Blueprints
admin_bestlap_blueprint = Blueprint('admin_bestlap', __name__,)

# Helper Functions


def get_pghead():
    return 'Best Lap'

# Route Handlers

# Best Lap
@admin_bestlap_blueprint.route('/bestlap/main')
@login_required
def main():
    if current_user.is_admin():
        return render_template('admin/bestlap/main.html', data=DataServices.get_model(BestLap), pghead=get_pghead(), settings=UIServices.get_settings())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_bestlap_blueprint.route('/bestlap/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.is_admin():
        form = BestLapForm(request.form)
        form.racer.choices = DataServices.get_availableRacers("NONE")
        form.raceclass.choices = DataServices.get_modelChoices(RaceClass, 'name')
        form.event.choices = DataServices.get_modelChoices(Event, 'name')

        if form.validate_on_submit():
            bestlap = BestLap(
                time=form.time.data,
                lap_date=form.lap_date.data
            )
            if form.is_best.data == True:
                bestlap.is_best=1
            else:
                bestlap.is_best=0

            bestlap.racer_id = form.racer.data
            bestlap.raceclass_id = form.raceclass.data
            bestlap.event_id = form.event.data
            db.session.add(bestlap)
            db.session.commit()

            flash('New best lap created.', 'success')
            return redirect(url_for("admin_bestlap.main", pghead=get_pghead(), settings=UIServices.get_settings()))
        return render_template('admin/create.html', form=form, pghead=get_pghead(), settings=UIServices.get_settings())
    else:
        flash('You are not an admin!', 'danger') 
        return redirect(url_for("user.members"))

@admin_bestlap_blueprint.route('/bestlap/update/<int:bestlap_id>/', methods=['GET', 'POST'])
@login_required
def update(bestlap_id):
    if current_user.is_admin():
        bestlap = DataServices.get_filter(BestLap, 'id', bestlap_id, True)
        form = BestLapForm(request.form)
        form.racer.choices = DataServices.get_availableRacers("NONE")
        form.raceclass.choices = DataServices.get_modelChoices(RaceClass, 'name')
        form.event.choices = DataServices.get_modelChoices(Event, 'name')

        
        if form.validate_on_submit():
            bestlap.racer_id = form.racer.data
            bestlap.raceclass_id = form.raceclass.data
            bestlap.event_id = form.event.data
            bestlap.time = form.time.data
            bestlap.lap_date = form.lap_date.data
            if form.is_best.data == True:
                bestlap.is_best=1
            else:
                bestlap.is_best=0

            bestlap.updated_date = datetime.datetime.now()
            db.session.commit()

            flash('Best Lap Updated.', 'success')
            return redirect(url_for("admin_bestlap.main", pghead=get_pghead(), settings=UIServices.get_settings()))
        
        if bestlap:
            form.racer.data = bestlap.racer.id
            form.raceclass.data = bestlap.raceclass.id
            form.event.data = bestlap.event.id
            form.time.data = bestlap.time
            form.lap_date.data = bestlap.lap_date
            form.is_best.data = bestlap.is_best

        return render_template('admin/update.html', bestlap=bestlap, form=form, pghead=get_pghead(), settings=UIServices.get_settings())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_bestlap_blueprint.route('/bestlap/delete/<int:bestlap_id>/')
@login_required
def delete(bestlap_id):
    if current_user.is_admin():
        bestlap = DataServices.get_filter(BestLap, 'id', bestlap_id, True)
        bestlap.delete()
        db.session.commit()
        flash('The best lap was deleted.', 'success')
        return redirect(url_for('admin_bestlap.main', pghead=get_pghead(), settings=UIServices.get_settings()))
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))