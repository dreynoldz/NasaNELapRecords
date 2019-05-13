# project/server/admin/views.py

import sys, datetime
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required, current_user
from project.server import bcrypt, db
from project.server.models import User, Car, CarRacer, RaceClass, Racer, RacerSponsor, Track, TrackEvent, \
Event, Sponsor, BestLap, Setting
from project.server.dataservices import DataServices, UIServices
from project.server.admin.forms import BestLapForm, CreateUserForm, UpdateUserForm, \
    passwordResetForm, NameSNForm, EventForm, CarForm,RacerForm,SponsorForm

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
        models = DataServices.get_modelList()
        data = {}
        current_time = datetime.datetime.utcnow()
        timedelta = DataServices.get_filterBy(Setting, 'name', 'TIMEDELTA', True)
        if timedelta:
            td = timedelta
        else:
            td = 30
    
        date_delta = current_time - datetime.timedelta(days=td)
        for model in models:
            if model == 'User':
                col1 = 'registered_on'
            else:
                col1 = 'created_date'
            col2 = 'updated_date'
            att1 = getattr(eval(model), col1)
            att2 = getattr(eval(model), col2)
            dm = DataServices.get_model(eval(model)).filter((att1 > date_delta) | (att2 > date_delta))
            orderedData = DataServices.get_modelOrder(dm, model, 'desc')
            data[model]=[]
            data[model].append(orderedData)
            data[model].append(DataServices.get_columns(orderedData))
        return render_template('admin/overview.html', data=data, model_name=get_modelName(), settings=UIServices.get_settings())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_blueprint.route('/settings', methods=['GET', 'POST'])
@login_required
def settings(model_name):
    if current_user.is_admin():
        data =  DataServices.get_model(eval(model_name))
        form = SettingsForm(request.form)

        if form.validate_on_submit():
            data.title = form.title.data
            data.description = form.description.data
            data.home = form.home.data
            data.author = form.author.data
            data.email = form.email.data
            data.copyright = form.copyright.data
            data.timedelta = form.timedelta.data
            db.session.commit()
            flash('Track Updated.', 'success')
            return redirect(url_for("admin.overview", model_name=get_modelName()))
        
        if data:
            form.title.data = data.title
            form.description.data = data.description
            form.home.data = data.home
            form.author.data = data.author
            form.email.data = data.email
            form.copyright.data = data.copyright
            form.timedelta.data = data.timedelta
            
        return render_template('admin/settings.html', data=data, model_name='Setting', settings=UIServices.get_settings())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_blueprint.route('/<model_name>/')
@login_required
def main(model_name):
    if current_user.is_admin():
        data = DataServices.get_model(eval(model_name))
        orderedData = DataServices.get_modelOrder(data, model_name, 'desc')
        cols = DataServices.get_columns(orderedData)
        return render_template('admin/main.html',data=orderedData, columns=cols, model_name=model_name, settings=UIServices.get_settings())
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
        elif model_name == 'Track' or model_name == 'RaceClass':
            form = NameSNForm(request.form)
        elif model_name == 'Event':
            form = EventForm(request.form)
            form.tracks.choices = DataServices.get_modelChoices(Track, 'name')
        elif model_name == 'Sponsor':
            form = SponsorForm(request.form)
        elif model_name == 'Car':
            form = CarForm(request.form)
        elif model_name == 'Racer':
            form = RacerForm(request.form)
            form.cars.choices = DataServices.get_carChoices()
            form.sponsors.choices = DataServices.get_modelChoices(Sponsor, 'name')
        if model_name == 'BestLap':
            form = BestLapForm(request.form)
            form.racer.choices = DataServices.get_availableRacers("NONE")
            form.raceclass.choices = DataServices.get_modelChoices(RaceClass, 'name')
            form.event.choices = DataServices.get_modelChoices(Event, 'name')

        if form.validate_on_submit():
            if model_name == 'User':
                row = User(
                    email=form.email.data,
                    password=form.password.data,
                    admin=form.admin.data
                )
                if form.racer.data != 0:
                    racer = DataServices.get_filterBy(Racer, 'id', form.racer.data, True)
                    row.racer = racer
                message = 'New user created.'
            elif model_name == 'Track':
                row = Track(
                name=form.name.data,
                short_name=form.short_name.data
                )
                message = 'New track created.'
            elif model_name == 'Event':
                row = Event(
                name=form.name.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data
                )
                for t in form.tracks.data:
                    if t != 0:
                        track = DataServices.get_filterBy(eval(model_name), 'id', t, True)
                        row.tracks.append(track)
                message = 'New event created.'
            elif model_name == 'RaceClass':
                row = RaceClass(
                name=form.name.data,
                short_name=form.short_name.data
                )
                message = 'New raceclass created.'
            elif model_name == 'Sponsor':
                row = Sponsor(
                name=form.name.data
                )
                message = 'New sponsor created.'
            elif model_name == 'Car':
                row = Car(
                    make=form.make.data,
                    model=form.model.data,
                    year=form.year.data,
                    color=form.color.data,
                    number=form.number.data
                )
                message = 'New car created.'
            elif model_name == 'Racer':
                row = Racer(
                    email=form.email.data,
                    name=form.name.data,
                    city=form.city.data,
                    state=form.state.data,
                    points=form.points.data,
                )

                for c in form.cars.data:
                    if c != 0:
                        car = DataServices.get_filterBy(Car, 'id', c, True)
                        row.cars.append(car)
                
                for s in form.sponsors.data:
                    if s != 0:
                        sponsor = DataServices.get_filterBy(Sponsor, 'id', s, True)
                        row.sponsors.append(sponsor)
                        
                message = 'New racer created.'
            elif model_name == 'BestLap':
                row = BestLap(
                    time=form.time.data,
                    lap_date=form.lap_date.data
                )
                if form.is_best.data == True:
                    row.is_best=1
                else:
                    row.is_best=0

                row.racer_id = form.racer.data
                row.raceclass_id = form.raceclass.data
                row.event_id = form.event.data
                message = 'New best lap created.'
                
            db.session.add(row)
            db.session.commit() 
            flash(message, 'success')
            return redirect(url_for("admin.main", model_name=model_name))
        return render_template('admin/create.html', form=form, model_name=model_name, settings=UIServices.get_settings())
    else:
        flash('You are not an admin!', 'danger') 
        return redirect(url_for("user.members"))

@admin_blueprint.route('/<model_name>/update/<int:model_id>/', methods=['GET', 'POST'])
@login_required
def update(model_name, model_id):
    if current_user.is_admin():
        data =  DataServices.get_filterBy(eval(model_name), 'id', model_id, True)
        if model_name == 'User':
            form = UpdateUserForm(request.form)
            form.racer.choices = DataServices.get_availableRacers(data.email)
            print(data.email)
        elif model_name == 'Track' or model_name == 'RaceClass':
            form = NameSNForm(request.form)
        elif model_name == 'Event':
            form = EventForm(request.form)
            form.tracks.choices = DataServices.get_modelChoices(Track, 'name')
        elif model_name == 'Sponsor':
            form = SponsorForm(request.form)
        elif model_name == 'Car':
            form = CarForm(request.form)
        elif model_name == 'Racer':
            form = RacerForm(request.form)
            form.cars.choices = DataServices.get_carChoices()
            form.sponsors.choices = DataServices.get_sponsorChoices()
        elif model_name == 'BestLap':
            form = BestLapForm(request.form)
            form.racer.choices = DataServices.get_availableRacers("NONE")
            form.raceclass.choices = DataServices.get_modelChoices(RaceClass, 'name')
            form.event.choices = DataServices.get_modelChoices(Event, 'name')

        if form.validate_on_submit():
            if model_name == 'User':
                if form.admin.data == True:
                    data.admin=1
                else:
                    data.admin=0

                if form.racer.data != 0:
                    racer = DataServices.get_filterBy(Racer, 'id', form.racer.data, True)
                    data.racer = racer
                else:
                    data.racer = None
                data.updated_date = datetime.datetime.now()
                message = 'User updated!.'
            elif model_name == 'Track' or model_name == 'RaceClass':
                data.name = form.name.data
                data.short_name = form.short_name.data
                data.updated_date = datetime.datetime.now()
                message = model_name + ' Updated.'
            elif model_name == 'Event':
                data.name = form.name.data
                data.start_date = form.start_date.data
                data.end_date = form.end_date.data

                for t in form.tracks.data:
                    if t == 0:
                        remove_track_association(model_id)
                        tracks=[]
                    else:
                        track = DataServices.get_filterBy(eval('Track'), 'id', t, True)
                        data.tracks.append(track)
                data.updated_date = datetime.datetime.now()
                message = 'Event Updated.'
            elif model_name == 'Sponsor':
                data.name = form.name.data
                message = 'Sponsor Updated.'
            elif model_name == 'Car':
                data.make = form.make.data
                data.model = form.model.data
                data.year = form.year.data
                data.color = form.color.data
                data.number = form.number.data
                data.updated_date = datetime.datetime.now()
                message = 'Car Updated.'
            elif model_name == 'Racer':
                data.email = form.email.data
                data.name = form.name.data
                data.city = form.city.data
                data.state = form.state.data
                data.points = form.points.data

                for c in form.cars.data:
                    if c != 0:
                        car = DataServices.get_filterBy(eval('Car'), 'id', c, True)
                        data.cars.append(car)
                    else:
                        DataServices.remove_car_association(model_id)
                        cars=[]
                
                for s in form.sponsors.data:
                    if s != 0:
                        sponsor = DataServices.get_filterBy(eval('Sponsor'), 'id', s, True)
                        data.sponsors.append(sponsor)
                    else:
                        DataServices.remove_sponsor_association(model_id)
                        sponsors=[]
                data.updated_date = datetime.datetime.now()
                message = 'Racer Updated.'
            elif model_name == 'BestLap':
                data.racer_id = form.racer.data
                data.raceclass_id = form.raceclass.data
                data.event_id = form.event.data
                data.time = form.time.data
                data.lap_date = form.lap_date.data
                if form.is_best.data == True:
                    data.is_best=1
                else:
                    data.is_best=0

                data.updated_date = datetime.datetime.now()
                message = 'Best Lap Updated.'

            db.session.commit()
            flash(message, 'success')
            return redirect(url_for("admin.main", model_name=model_name))

        if data:
            if model_name == 'User':
                form.admin.data = data.admin
                if data.racer:
                    form.racer = data.racer.id
                    print(data.racer.id)
            elif model_name == 'Track' or model_name == 'RaceClass':
                form.name.data = data.name
                form.short_name.data = data.short_name
            elif model_name == 'Event':
                form.name.data = data.name
                form.start_date.data = data.start_date
                form.end_date.data = data.end_date
            elif model_name == 'Sponsor':
                form.name.data = data.name
            elif model_name == 'Car':
                form.make.data = data.make
                form.model.data = data.model
                form.year.data = data.year
                form.color.data = data.color
                form.number.data = data.number
            elif model_name == 'Racer':
                form.email.data = data.email
                form.name.data = data.name
                form.city.data = data.city
                form.state.data = data.state
                form.points.data = data.points
            elif model_name == 'BestLap':
                data.name = " | ".join([data.racer.name, data.raceclass.name, data.event.name, str(data.time)])
                form.racer.data = data.racer.id
                form.raceclass.data = data.raceclass.id
                form.event.data = data.event.id
                form.time.data = data.time
                form.lap_date.data = data.lap_date
                form.is_best.data = data.is_best
        return render_template('admin/update.html', model_name=model_name, data=data, form=form, settings=UIServices.get_settings())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_blueprint.route('/<model_name>/delete/<int:model_id>/')
@login_required
def delete(model_name,model_id):
    if current_user.is_admin():
        row = DataServices.get_filterBy(eval(model_name), 'id', model_id, True)
        if model_name == 'User':
            row.racer = None
            message = 'The user was deleted.'
        elif model_name == 'Track':
            trackEvents = DataServices.get_filterBy(eval('TrackEvent'), 'trackId', model_id, False)
            for trackEvent in trackEvents:
                event =  DataServices.get_filterBy(eval('Event'), 'id', trackEvent.eventId, True)
                row.events.remove(event)
            message = 'The track was deleted.'
        elif model_name == 'Event':
            DataServices.remove_track_association(model_id)
            message = 'The event was deleted.'
        elif model_name == 'RaceClass':
            #Cake is a Lie
            message = 'The track was deleted.'
        elif model_name == 'Car':
            carRacers = DataServices.get_filterBy(CarRacer,'carId', model_id, False)
            for carRacer in carRacers:
                racer = DataServices.get_filterBy(Racer, 'id', carRacer.racerId, True)
                row.racers.remove(racer)
            message = 'The car was deleted.'
        elif model_name == 'Racer':
            DataServices.remove_car_association(model_id)
            DataServices.remove_sponsor_association(model_id)
            message = 'The racer was deleted.'
        else:
            message = model_name + ':' + model_id + ' was deleted'
        
        db.session.delete(row)
        db.session.commit()
        flash(message, 'success')
        return redirect(url_for('admin.main', model_name=model_name, settings=UIServices.get_settings()))
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))