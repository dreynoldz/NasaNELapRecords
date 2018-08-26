# project/server/admin/views.py


from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from project.server import bcrypt, db
from project.server.models import User
from project.server.admin.forms import CreateUserForm, UpdateUserForm, passwordResetForm

# Blueprints
admin_blueprint = Blueprint('admin', __name__,)

# Helper Functions
def get_users():
    return db.session.query(User)

def check_admin(page):
    if current_user.is_authenticated:
        if current_user.is_admin():
            return render_template(page)
        else:
            flash('You are not an admin!', 'danger')
            return render_template('user/members.html')

# Route Handlers
@admin_blueprint.route('/overview')
@login_required
def overview():
    if current_user.is_admin():
        return render_template('admin/overview.html')
    else:
        flash('You are not an admin!', 'danger')
        return render_template('user/members.html')


@admin_blueprint.route('/users')
@login_required
def users():
    if current_user.is_admin():
        return render_template('admin/users.html', users=get_users())
    else:
        flash('You are not an admin!', 'danger')
        return render_template('user/members.html')

@admin_blueprint.route('/create_user', methods=['GET', 'POST'])
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

        return render_template('admin/create_user.html', form=form)
    else:
        flash('You are not an admin!', 'danger')
        return render_template('user/members.html')

@admin_blueprint.route('/update_user/<int:user_id>/', methods=['GET', 'POST'])
@login_required
def update_user(user_id):
    if current_user.is_admin():
        user = User.query.filter_by(id=user_id).first()
        if user:
            form = UpdateUserForm(request.form)
            form.email.data = user.email
            form.admin.data = user.admin

        if form.validate_on_submit():
            user = User(
                email=form.email.data,
                admin=form.admin.data
            )
            db.session.add(user)
            db.session.commit()

            flash('User updated!.', 'success')
            return redirect(url_for("admin.users"))
        
        return render_template('admin/update_user.html', user=user, form=form)
    else:
        flash('You are not an admin!', 'danger')
        return render_template('user/members.html')

@admin_blueprint.route('/delete_user/<int:user_id>/')
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
        return render_template('user/members.html')