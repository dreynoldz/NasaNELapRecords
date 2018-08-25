# project/server/admin/views.py


from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_user, logout_user, login_required, current_user

from project.server import bcrypt, db
from project.server.models import User
from project.server.user.forms import LoginForm, RegisterForm

# Blueprints
admin_blueprint = Blueprint('admin', __name__,)

# Helper Functions
def check_admin(page):
    if current_user.is_authenticated:
        if current_user.is_admin():
            return render_template(page)
        else:
            flash('You are not an admin!', 'danger')
            return render_template('user/members.html')

def get_users():
    return db.session.query(User)

# Route Handlers
@admin_blueprint.route('/dashboard')
@login_required
def dashboard():
    if current_user.is_admin():
        return render_template('admin/dashboard.html')
    else:
        flash('You are not an admin!', 'danger')
        return render_template('user/members.html')


@admin_blueprint.route('/users')
@login_required
#@admin_required(ad_req='True')
def users():
    if current_user.is_admin():
        return render_template('admin/users.html', users=get_users())
    else:
        flash('You are not an admin!', 'danger')
        return render_template('user/members.html')