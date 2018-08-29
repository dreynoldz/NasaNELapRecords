# project/server/admin/views.py

import sys
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required, current_user

from project.server import bcrypt, db

# Blueprints
admin_blueprint = Blueprint('admin', __name__,)

# Helper Functions
def get_pghead():
    return 'Overview'


# Route Handlers
# Main
@admin_blueprint.route('/overview')
@login_required
def overview():
    if current_user.is_admin():
        return render_template('admin/overview.html', pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))
