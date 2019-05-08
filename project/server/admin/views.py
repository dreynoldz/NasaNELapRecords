# project/server/admin/views.py

import sys, datetime
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required, current_user
from project.server import bcrypt, db
from project.server.models import User, Car, CarRacer, RaceClass, Racer, RacerSponsor, Track, TrackEvent, \
Event, Sponsor, BestLap
from project.server.dataservices import DataServices, UIServices
from project.server.admin.forms import BestLapForm, CreateUserForm, UpdateUserForm, \
    passwordResetForm, TrackForm, EventForm

# Blueprints
admin_blueprint = Blueprint('admin', __name__,)

# Helper Functions
def get_modelName():
    return 'Overview'


# Route Handlers
# Main
@admin_blueprint.route('/overview')
@login_required
def overview():
    if current_user.is_admin():
        return render_template('admin/overview.html', modelName=get_modelName(), settings=UIServices.get_settings())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_blueprint.route('/<model_name>/')
@login_required
def main(model_name):
    if current_user.is_admin():
        return render_template('admin/main.html', data=DataServices.get_model(eval(model_name)), modelName=model_name, settings=UIServices.get_settings())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_blueprint.route('/<model_name>/create/', methods=['GET', 'POST'])
@login_required
def create(model_name):
    if current_user.is_admin():
        if model_name == 'User':
            form = CreateUserForm(request.form)
            form.racer.choices = DataServices.get_availableRacers("NONE")
        elif model_name == 'Track':
            form = TrackForm(request.form)
        elif model_name == 'Event':
            form = EventForm(request.form)
            form.tracks.choices = DataServices.get_trackChoices()
        elif model_name == 'Car':
            form = CarForm(request.form) 
        if model_name == 'BestLap':
            form = BestLapForm(request.form)
            form.racer.choices = DataServices.get_availableRacers("NONE")
            form.raceclass.choices = DataServices.get_modelChoices(RaceClass, 'name')
            form.event.choices = DataServices.get_modelChoices(Event, 'name')
       

        if form.validate_on_submit():
            if model_name == 'User':
                user = User(
                    email=form.email.data,
                    password=form.password.data,
                    admin=form.admin.data
                )
                if form.racer.data != 0:
                    racer = db.session.query(Racer).filter_by(id=form.racer.data).first()
                    user.racer = racer
                db.session.add(user)
                message = 'New user created.'
            elif model_name == 'Track':
                track = Track(
                name=form.name.data,
                short_name=form.short_name.data
                )
                db.session.add(track)
                message = 'New track created.'
            elif model_name == 'Event':
                event = Event(
                name=form.name.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data
                )
                for t in form.tracks.data:
                    if t != 0:
                        track = ataServices.get_filter(eval(model_name), 'id', t, True)
                        event.tracks.append(track)
                db.session.add(event)
                message = 'New event created.'
            elif model_name == 'Car':
                car = Car(
                    make=form.make.data,
                    model=form.model.data,
                    year=form.year.data,
                    color=form.color.data,
                    number=form.number.data
                )
                db.session.add(car)
                message = 'New car created.'
            elif model_name == 'BestLap':
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
                message = 'New best lap created.'

            db.session.commit() 
            flash(message, 'success')
            return redirect(url_for("admin.main", modelName=model_name, settings=UIServices.get_settings()))
        return render_template('admin/create.html', form=form, modelName=model_name, settings=UIServices.get_settings())
    else:
        flash('You are not an admin!', 'danger') 
        return redirect(url_for("user.members"))

@admin_blueprint.route('/<model_name>/update/<int:model_id>/', methods=['GET', 'POST'])
@login_required
def update(model_name, model_id):
    if current_user.is_admin():
        data =  DataServices.get_filter(eval(model_name), 'id', model_id, True)
        print(model_id)
        #print(data.name)
        if model_name == 'User':
            form = CreateUserForm(request.form)
            form.racer.choices = DataServices.get_availableRacers(data.email)

            if data:
                form.admin.data = data.admin
                if data.racer:
                    form.racer.data = data.racer.id
        
        elif model_name == 'Track':
            form = TrackForm(request.form)

            if data:
                form.name.data = data.name
                form.short_name.data = data.short_name
        
        elif model_name == 'Event':
            form = EventForm(request.form)
            form.tracks.choices = DataServices.get_modelChoices(Track, 'name')

            if data:
                form.name.data = data.name
                form.start_date.data = data.start_date
                form.end_date.data = data.end_date
        
        elif model_name == 'Car':
            data = Car.query.filter_by(id=car_id).first()
            form = CarForm(request.form)
            
            if data:
                form.make.data = data.make
                form.model.data = data.model
                form.year.data = data.year
                form.color.data = data.color
                form.number.data = data.number

        elif model_name == 'BestLap':
            data = DataServices.get_filter(eval(model_name), 'id', model_id, True)
            form = BestLapForm(request.form)
            form.racer.choices = DataServices.get_availableRacers("NONE")
            form.raceclass.choices = DataServices.get_modelChoices(RaceClass, 'name')
            form.event.choices = DataServices.get_modelChoices(Event, 'name')
            
            if data:
                data.name = " | ".join([data.racer.name, data.raceclass.name, data.event.name, str(data.time)])
                form.racer.data = data.racer.id
                form.raceclass.data = data.raceclass.id
                form.event.data = data.event.id
                form.time.data = data.time
                form.lap_date.data = data.lap_date
                form.is_best.data = data.is_best

        if form.validate_on_submit():
            if model_name == 'User':
                if form.admin.data == True:
                    user.admin=1
                else:
                    user.admin=0

                if form.racer.data != 0:
                    racer = db.session.query(Racer).filter(Racer.id == form.racer.data).first()
                    user.racer = racer
                else:
                    user.racer = None
                user.updated_date = datetime.datetime.now()
                db.session.commit()
                message = 'User updated!.'
            elif model_name == 'Track':
                track.name = form.name.data
                track.short_name = form.short_name.data
                track.updated_date = datetime.datetime.now()
                db.session.commit()
                message = 'Track Updated.'
            elif model_name == 'Event':
                event.name = form.name.data
                event.start_date = form.start_date.data
                event.end_date = form.end_date.data

                for t in form.tracks.data:
                    if t == 0:
                        remove_track_association(model_id)
                        tracks=[]
                    else:
                        track = DataServices.get_filter(eval('Track'), 'id', t, True)
                        event.tracks.append(track)
                event.updated_date = datetime.datetime.now()
                message = 'Event Updated.'
            elif model_name == 'Car':
                car.make = form.make.data
                car.model = form.model.data
                car.year = form.year.data
                car.color = form.color.data
                car.number = form.number.data
                car.updated_date = datetime.datetime.now()
                message = 'Car Updated.'
            elif model_name == 'BestLap':
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
                message = 'Best Lap Updated.'

            db.session.commit()
            flash(message, 'success')
            return redirect(url_for("admin.main", modelName=model_name, settings=UIServices.get_settings()))
        
        return render_template('admin/update.html', modelName=model_name, data=data, form=form, settings=UIServices.get_settings())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_blueprint.route('/<model_name>/delete/<int:model_id>/')
@login_required
def delete(model_name,model_id):
    if current_user.is_admin():
        row = DataServices.get_filter(eval(model_name), 'id', model_id, True)
        if model_name == 'User':
            row.racer = None
            message = 'The user was deleted.'
        elif model_name == 'Track':
            trackEvents = DataServices.get_filter(eval('TrackEvent'), 'trackId', model_id, False)
            for trackEvent in trackEvents:
                event =  DataServices.get_filter(eval('Event'), 'id', trackEvent.eventId, True)
                t.events.remove(event)
            message = 'The track was deleted.'
        elif model_name == 'Event':
            DataServices.remove_track_association(model_id)
            message = 'The event was deleted.'
        elif model_name == 'Car':
            row = DataServices.get_filter(eval(model_name), 'id', model_id, True)
            carRacers = DataServices.get_filter(CarRacer,'carId', model_id, False)
            for carRacer in carRacers:
                racer = DataServices.get_filter(Racer, 'id', carRacer.racerId, True)
                c.racers.remove(racer)
            message = 'The car was deleted.'
        else:
            row = DataServices.get_filter(eval(model_name), 'id', model_id, True)
            message = model_name + ':' + model_id + ' was deleted'
        
        row.delete()
        db.session.commit()
        flash(message, 'success')
        return redirect(url_for('admin.main', modelName=model_name, settings=UIServices.get_settings()))
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))