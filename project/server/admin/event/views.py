# project/server/admin/event/views.py

import sys
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required, current_user

from project.server import bcrypt, db
from project.server.models import Event, Track, TrackEvent
from project.server.admin.forms import EventForm, TrackForm

# Blueprints
admin_event_blueprint = Blueprint('admin_event', __name__,)

# Helper Functions


def get_events():
    return db.session.query(Event)

def get_tracks():
    return db.session.query(Track)

def get_trackChoices():
    tracks = get_tracks()
    track_list = [(0, "---")]
    [track_list.append((t.id, t.name)) for t in tracks.order_by(Track.name).all()]
    return track_list

def remove_track_association(event_id):
    event = db.session.query(Event).filter_by(id=event_id)
    e = event.first()
    trackEvents = db.session.query(TrackEvent).filter_by(eventId=event_id).all()
    for trackEvent in trackEvents:
        track = db.session.query(Track).filter_by(id=trackEvent.trackId).first()
        e.tracks.remove(track)

def get_pghead():
    return 'Events'

# Route Handlers

# Event
@admin_event_blueprint.route('/event/main')
@login_required
def main():
    if current_user.is_admin():
        return render_template('admin/event/main.html', events=get_events(), pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_event_blueprint.route('/event/create', methods=['GET', 'POST'])
@login_required
def create():
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
                if t != 0:
                    track = db.session.query(Track).filter_by(id=t).first()
                    event.tracks.append(track)

            db.session.add(event)
            db.session.commit()

            flash('New event created.', 'success')
            return redirect(url_for("admin_event.main", pghead=get_pghead()))
        return render_template('admin/event/create.html', form=form, pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger') 
        return redirect(url_for("user.members"))

@admin_event_blueprint.route('/event/update/<int:event_id>/', methods=['GET', 'POST'])
@login_required
def update(event_id):
    if current_user.is_admin():
        event = Event.query.filter_by(id=event_id).first()
        form = EventForm(request.form)
        form.tracks.choices = get_trackChoices()
        
        if form.validate_on_submit():
            event.name = form.name.data
            event.start_date = form.start_date.data
            event.end_date = form.end_date.data

            for t in form.tracks.data:
                if t == 0:
                    remove_track_association(event_id)
                    tracks=[]
                else:
                    track = db.session.query(Track).filter_by(id=t).first()
                    event.tracks.append(track)
            
            db.session.commit()

            flash('Event Updated.', 'success')
            return redirect(url_for("admin_event.main", pghead=get_pghead()))
        
        if event:
            form.name.data = event.name
            form.start_date.data = event.start_date
            form.end_date.data = event.end_date

        return render_template('admin/event/update.html', event=event, form=form, pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_event_blueprint.route('/event/delete/<int:event_id>/')
@login_required
def delete(event_id):
    if current_user.is_admin():
        event = db.session.query(Event).filter_by(id=event_id)
        remove_track_association(event_id)
        event.delete()
        db.session.commit()
        flash('The event was deleted.', 'success')
        return redirect(url_for('admin_event.main', pghead=get_pghead()))
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))