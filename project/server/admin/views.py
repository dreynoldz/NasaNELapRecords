# project/server/admin/views.py

import sys
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import current_user

from project.server import bcrypt, db
from project.server.models import User
from project.server.admin.forms import CreateUserForm, UpdateUserForm, passwordResetForm

# Blueprints
admin_blueprint = Blueprint('admin', __name__,)

# Helper Functions
def get_users():
    return db.session.query(User)

def get_events():
    return db.session.query(Event)

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
        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            form = UpdateUserForm(request.form)
            #form.admin.data = user.admin

        if form.validate_on_submit():
            print(form.admin.data, file=sys.stderr)
            if form.admin.data == True:
                print("Admin", file=sys.stderr)
                ad=1
            else:
                print("Not Admin", file=sys.stderr)
                ad=0

            data = {'admin': ad}
            user = User.query.filter_by(email=form.email.data).first()
            user.update(data, synchronize_session='evaluate')
            db.session.commit()

            flash('User updated!.', 'success')
            return redirect(url_for("admin.users"))
        
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
        form = CreateEventForm(request.form)
        if form.validate_on_submit():
            event = Event(
                email=form.email.data,
                password=form.password.data,
                admin=form.admin.data
            )
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
        
        if event:
            form = UpdateEventForm(request.form)
            #form.admin.data = user.admin

        if form.validate_on_submit():
            print(form.admin.data, file=sys.stderr)
            if form.admin.data == True:
                print("Admin", file=sys.stderr)
                ad=1
            else:
                print("Not Admin", file=sys.stderr)
                ad=0

            data = {'admin': ad}
            event = db.session.query(Event).filter(Event.id==event_id)
            event.update(data, synchronize_session='evaluate')
            db.session.commit()

            flash('Event updated!.', 'success')
            return redirect(url_for("admin.events"))
        
        return render_template('admin/event/update.html', event=event, form=form)
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_blueprint.route('/event/delete/<int:event_id>/')
@login_required
def delete_event(event_id):
    if current_user.is_admin():
        event = db.session.query(Event).filter_by(id=event_id)
        event.delete()
        db.session.commit()
        flash('The event was deleted.', 'success')
        return redirect(url_for('admin.events'))
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))