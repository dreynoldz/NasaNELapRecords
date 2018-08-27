# project/server/admin/views.py

import sys
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required, current_user

from project.server import bcrypt, db
from project.server.models import User, Event, Track, TrackEvent
from project.server.admin.forms import CreateUserForm, UpdateUserForm, \
    passwordResetForm, EventForm, TrackForm

# Blueprints
admin_blueprint = Blueprint('admin', __name__,)

# Helper Functions
def get_users():
    return db.session.query(User)

def get_events():
    return db.session.query(Event)

def get_tracks():
    return db.session.query(Track)

def get_trackChoices():
    tracks = get_tracks()
    track_list = [(t.id, t.name) for t in tracks.order_by(Track.name).all()]
    return track_list

def remove_track_association(event_id):
    event = db.session.query(Event).filter_by(id=event_id)
    e = event.first()
    trackEvents = db.session.query(TrackEvent).filter_by(eventId=event_id).all()
    for trackEvent in trackEvents:
        track = db.session.query(Track).filter_by(id=trackEvent.trackId).first()
        e.tracks.remove(track)

def check_admin(page):
    if current_user.is_authenticated:
        if current_user.is_admin():
            return render_template(page)
        else:
            flash('You are not an admin!', 'danger')
            return redirect(url_for("user.members"))


# Route Handlers
# Main
@admin_blueprint.route('/overview')
@login_required
def overview():
    if current_user.is_admin():
        return render_template('admin/overview.html')
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

#Users
@admin_blueprint.route('/user/main')
@login_required
def users():
    if current_user.is_admin():
        return render_template('admin/user/main.html', users=get_users())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_blueprint.route('/user/create', methods=['GET', 'POST'])
@login_required
def create_user():
    if current_user.is_admin():
        form = CreateUserForm(request.form)
        if form.validate_on_submit():
            user = User(
                email=form.email.data,
                password=form.password.data,
                admin=form.admin.data
            )
            db.session.add(user)
            db.session.commit()

            flash('New user created.', 'success')
            return redirect(url_for("admin.users"))
        return render_template('admin/user/create.html', form=form)
    else:
        flash('You are not an admin!', 'danger') 
        return redirect(url_for("user.members"))

@admin_blueprint.route('/user/update/<int:user_id>/', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    if current_user.is_admin():
        form = UpdateUserForm(request.form)
        user = User.query.filter_by(id=user_id).first()
        

        if form.validate_on_submit():
            if form.admin.data == True:
                user.admin=1
            else:
                user.admin=0

            db.session.commit()
            flash('User updated!.', 'success')
            return redirect(url_for("admin.users"))
        
        if user:
            form.admin.data = user.admin

        return render_template('admin/user/update.html', user=user, form=form)
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_blueprint.route('/user/delete/<int:user_id>/')
@login_required
def delete_user(user_id):
    if current_user.is_admin():
        user = db.session.query(User).filter_by(id=user_id)
        user.delete()
        db.session.commit()
        flash('The user was deleted.', 'success')
        return redirect(url_for('admin.users'))
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

# Event
@admin_blueprint.route('/event/main')
@login_required
def events():
    if current_user.is_admin():
        return render_template('admin/event/main.html', events=get_events())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_blueprint.route('/event/create', methods=['GET', 'POST'])
@login_required
def create_event():
    if current_user.is_admin():
        form = EventForm(request.form)
        form.tracks.choices = get_trackChoices()

        if form.validate_on_submit():
            event = Event(
                name=form.name.data,
                start_date=form.start_date.data,
                end_date=form.end_date.data
            )
            for t in form.tracks.data:
                track = db.session.query(Track).filter_by(id=t).first()
                event.tracks.append(track)

            db.session.add(event)
            db.session.commit()

            flash('New event created.', 'success')
            return redirect(url_for("admin.events"))
        return render_template('admin/event/create.html', form=form)
    else:
        flash('You are not an admin!', 'danger') 
        return redirect(url_for("user.members"))

@admin_blueprint.route('/event/update/<int:event_id>/', methods=['GET', 'POST'])
@login_required
def update_event(event_id):
    if current_user.is_admin():
        event = Event.query.filter_by(id=event_id).first()
        form = EventForm(request.form)
        form.tracks.choices = get_trackChoices()
        
        if form.validate_on_submit():
            event.name = form.name.data
            event.start_date = form.start_date.data
            event.end_date = form.end_date.data
            remove_track_association(event_id)
            tracks=[]

            for t in form.tracks.data:
                track = db.session.query(Track).filter_by(id=t).first()
                event.tracks.append(track)
            
            db.session.commit()

            flash('Event Updated.', 'success')
            return redirect(url_for("admin.events"))
        
        if event:
            form.name.data = event.name
            form.start_date.data = event.start_date
            form.end_date.data = event.end_date

        return render_template('admin/event/update.html', event=event, form=form)
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_blueprint.route('/event/delete/<int:event_id>/')
@login_required
def delete_event(event_id):
    if current_user.is_admin():
        event = db.session.query(Event).filter_by(id=event_id)
        remove_track_association(event_id)
        event.delete()
        db.session.commit()
        flash('The event was deleted.', 'success')
        return redirect(url_for('admin.events'))
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

# Track
@admin_blueprint.route('/track/main')
@login_required
def tracks():
    if current_user.is_admin():
        return render_template('admin/track/main.html', tracks=get_tracks())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_blueprint.route('/track/create', methods=['GET', 'POST'])
@login_required
def create_track():
    if current_user.is_admin():
        form = TrackForm(request.form)

        if form.validate_on_submit():
            track = Track(
                name=form.name.data,
                short_name=form.short_name.data
            )
            db.session.add(track)
            db.session.commit()

            flash('New track created.', 'success')
            return redirect(url_for("admin.tracks"))
        return render_template('admin/track/create.html', form=form)
    else:
        flash('You are not an admin!', 'danger') 
        return redirect(url_for("user.members"))

@admin_blueprint.route('/track/update/<int:track_id>/', methods=['GET', 'POST'])
@login_required
def update_track(track_id):
    if current_user.is_admin():
        track = Track.query.filter_by(id=track_id).first()
        form = TrackForm(request.form)

        if form.validate_on_submit():
            print(form.name.data, file=sys.stderr)
            print(form.short_name.data, file=sys.stderr)
            track.name = form.name.data
            track.short_name = form.short_name.data

            db.session.commit()

            flash('Track Updated.', 'success')
            return redirect(url_for("admin.tracks"))
        
        if track:
            form.name.data = track.name
            form.short_name.data = track.short_name

        return render_template('admin/track/update.html', track=track, form=form)
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_blueprint.route('/track/delete/<int:track_id>/')
@login_required
def delete_track(track_id):
    if current_user.is_admin():
        track = db.session.query(Track).filter_by(id=track_id)
        t = track.first()
        trackEvents = db.session.query(TrackEvent).filter_by(trackId=track_id).all()
        for trackEvent in trackEvents:
            event = db.session.query(Event).filter_by(id=trackEvent.eventId).first()
            t.events.remove(event)
        track.delete()
        db.session.commit()
        flash('The track was deleted.', 'success')
        return redirect(url_for('admin.tracks'))
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))