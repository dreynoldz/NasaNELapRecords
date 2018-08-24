# project/server/admin/views.py


from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_user, logout_user, login_required

from project.server import bcrypt, db
from project.server.models import User
from project.server.user.forms import LoginForm, RegisterForm

# Blueprints
admin_blueprint = Blueprint('admin', __name__,)

# Helper Functions
def get_users():
    return db.session.query(User)

# Route Handlers
@admin_blueprint.route('/dashboard')
@login_required
def dashboard():
    return render_template('admin/dashboard.html')

@admin_blueprint.route('/users')
@login_required
def users():
    return render_template(
        'admin/users.html',
        users=get_users()
        )
