# project/server/admin/views.py

import sys
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required, current_user

from project.server import bcrypt, db
from project.server.models import User
from project.server.admin.forms import CreateUserForm, UpdateUserForm, \
    passwordResetForm

# Blueprints
admin_user_blueprint = Blueprint('admin_user', __name__,)

# Helper Functions
def get_users():
    return db.session.query(User)

# Route Handlers

#Users
@admin_user_blueprint.route('/user/main')
@login_required
def main():
    if current_user.is_admin():
        return render_template('admin/user/main.html', users=get_users())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_user_blueprint.route('/user/create', methods=['GET', 'POST'])
@login_required
def create():
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
            return redirect(url_for("admin_user.main"))
        return render_template('admin/user/create.html', form=form)
    else:
        flash('You are not an admin!', 'danger') 
        return redirect(url_for("user.members"))

@admin_user_blueprint.route('/user/update/<int:user_id>/', methods=['GET', 'POST'])
@login_required
def update(user_id):
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
            return redirect(url_for("admin_user.main"))
        
        if user:
            form.admin.data = user.admin

        return render_template('admin/user/update.html', user=user, form=form)
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_user_blueprint.route('/user/delete/<int:user_id>/')
@login_required
def delete(user_id):
    if current_user.is_admin():
        user = db.session.query(User).filter_by(id=user_id)
        user.delete()
        db.session.commit()
        flash('The user was deleted.', 'success')
        return redirect(url_for('admin_user.main'))
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))
