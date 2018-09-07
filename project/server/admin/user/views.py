# project/server/admin/user/views.py

import sys
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required, current_user

from project.server import bcrypt, db
from project.server.models import User, Racer
from project.server.admin.user.forms import CreateUserForm, UpdateUserForm, \
    passwordResetForm

# Blueprints
admin_user_blueprint = Blueprint('admin_user', __name__,)

# Helper Functions
def get_users():
    return db.session.query(User)

def get_availableRacers(email):
    availracers_list = [(0, "---")]
    print(availracers_list)
    if email == 'NONE':
        availRacers = db.session.query(Racer).filter(Racer.user_id == None)
        print(availRacers)
        [availracers_list.append((a.id, a.name)) for a in availRacers.order_by(Racer.name).all()]
        print(availracers_list)
        return availracers_list
    else:
        availRacer = db.session.query(Racer).filter(Racer.email == email).first()
        if availRacer:
            [availracers_list.append((availRacer.id, availRacer.name))]
            print(availracers_list)
            return availracers_list
        else:
            availRacers = db.session.query(Racer).filter(Racer.user_id == None)
            [availracers_list.append((a.id, a.name)) for a in availRacers.order_by(Racer.name).all()]
            print(availracers_list)
            return availracers_list


def get_pghead():
    return 'Users'

# Route Handlers

#Users
@admin_user_blueprint.route('/user/main')
@login_required
def main():
    if current_user.is_admin():
        return render_template('admin/user/main.html', users=get_users(), pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_user_blueprint.route('/user/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.is_admin():
        form = CreateUserForm(request.form)
        form.racer.choices = get_availableRacers('NONE')

        if form.validate_on_submit():
            user = User(
                email=form.email.data,
                password=form.password.data,
                admin=form.admin.data
            )
            if form.racer.data != 0:
                racer = db.session.query(Racer).filter_by(id=form.racer.data).first()
                user.racer.append(racer)

            db.session.add(user)
            db.session.commit()

            flash('New user created.', 'success')
            return redirect(url_for("admin_user.main", pghead=get_pghead()))
        return render_template('admin/user/create.html', form=form, pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger') 
        return redirect(url_for("user.members"))

@admin_user_blueprint.route('/user/update/<int:user_id>/', methods=['GET', 'POST'])
@login_required
def update(user_id):
    if current_user.is_admin():
        form = UpdateUserForm(request.form)
        user = User.query.filter_by(id=user_id).first()
        form.racer.choices = get_availableRacers(user.email)
        

        if form.validate_on_submit():
            if form.admin.data == True:
                user.admin=1
            else:
                user.admin=0

            if form.racer.data != 0:
                racer = db.session.query(Racer).filter(Racer.id == form.racer.data).first()
                user.racer = racer
            else:
                user.racer = None

            db.session.commit()
            flash('User updated!.', 'success')
            return redirect(url_for("admin_user.main", pghead=get_pghead()))
        
        if user:
            form.admin.data = user.admin
            if user.racer:
                form.racer.data = user.racer.id

        return render_template('admin/user/update.html', user=user, form=form, pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_user_blueprint.route('/user/delete/<int:user_id>/')
@login_required
def delete(user_id):
    if current_user.is_admin():
        user = db.session.query(User).filter_by(id=user_id)
        u = user.first()
        u.racer = None
        user.delete()
        db.session.commit()
        flash('The user was deleted.', 'success')
        return redirect(url_for('admin_user.main', pghead=get_pghead()))
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members", pghead=get_pghead()))
