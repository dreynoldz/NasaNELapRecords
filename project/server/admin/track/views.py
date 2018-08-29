# project/server/admin/track/views.py

import sys
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required, current_user

from project.server import bcrypt, db
from project.server.models import Track, TrackEvent, Event
from project.server.admin.track.forms import TrackForm

# Blueprints
admin_track_blueprint = Blueprint('admin_track', __name__,)

# Helper Functions
def get_tracks():
    return db.session.query(Track)

def get_pghead():
    return 'Tracks'

# Route Handlers

# Track
@admin_track_blueprint.route('/track/main')
@login_required
def main():
    if current_user.is_admin():
        return render_template('admin/track/main.html', tracks=get_tracks(), pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_track_blueprint.route('/track/create', methods=['GET', 'POST'])
@login_required
def create():
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
            return redirect(url_for("admin_track.main", pghead=get_pghead()))
        return render_template('admin/track/create.html', form=form, pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger') 
        return redirect(url_for("user.members"))

@admin_track_blueprint.route('/track/update/<int:track_id>/', methods=['GET', 'POST'])
@login_required
def update(track_id):
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
            return redirect(url_for("admin_track.main", pghead=get_pghead()))
        
        if track:
            form.name.data = track.name
            form.short_name.data = track.short_name

        return render_template('admin/track/update.html', track=track, form=form, pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_track_blueprint.route('/track/delete/<int:track_id>/')
@login_required
def delete(track_id):
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
        return redirect(url_for('admin_track.main', pghead=get_pghead()))
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))