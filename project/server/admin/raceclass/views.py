# project/server/admin/raceclass/views.py

import sys, datetime
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required, current_user

from project.server import bcrypt, db
from project.server.models import RaceClass
from project.server.admin.raceclass.forms import RaceClassForm
from project.server.dataservices import DataServices, UIServices

# Blueprints
admin_raceclass_blueprint = Blueprint('admin_raceclass', __name__,)

# Helper Functions
def get_raceclasses():
    return db.session.query(RaceClass)

def get_pghead():
    return 'Race Classes'
# Route Handlers

# Track
@admin_raceclass_blueprint.route('/raceclass/main')
@login_required
def main():
    if current_user.is_admin():
        return render_template('admin/raceclass/main.html', raceclasses=get_raceclasses(), pghead=get_pghead(), settings=UIServices.get_settings())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_raceclass_blueprint.route('/raceclass/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.is_admin():
        form = RaceClassForm(request.form)

        if form.validate_on_submit():
            raceclass = RaceClass(
                name=form.name.data,
                short_name=form.short_name.data
            )
            db.session.add(raceclass)
            db.session.commit()

            flash('New raceclass created.', 'success')
            return redirect(url_for("admin_raceclass.main", pghead=get_pghead(), settings=UIServices.get_settings()))
        return render_template('admin/raceclass/create.html', form=form, pghead=get_pghead(), settings=UIServices.get_settings())
    else:
        flash('You are not an admin!', 'danger') 
        return redirect(url_for("user.members"))

@admin_raceclass_blueprint.route('/raceclass/update/<int:raceclass_id>/', methods=['GET', 'POST'])
@login_required
def update(raceclass_id):
    if current_user.is_admin():
        raceclass = RaceClass.query.filter_by(id=raceclass_id).first()
        form = RaceClassForm(request.form)

        if form.validate_on_submit():
            raceclass.name = form.name.data
            raceclass.short_name = form.short_name.data
            raceclass.updated_date = datetime.datetime.now()
            db.session.commit()

            flash('RaceClass Updated.', 'success')
            return redirect(url_for("admin_raceclass.main", pghead=get_pghead(), settings=UIServices.get_settings()))
        
        if raceclass:
            form.name.data = raceclass.name
            form.short_name.data = raceclass.short_name

        return render_template('admin/raceclass/update.html', raceclass=raceclass, form=form, pghead=get_pghead(), settings=UIServices.get_settings())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_raceclass_blueprint.route('/raceclass/delete/<int:raceclass_id>/')
@login_required
def delete(raceclass_id):
    if current_user.is_admin():
        raceclass = db.session.query(RaceClass).filter_by(id=raceclass_id)
        raceclass.delete()
        db.session.commit()
        flash('The raceclass was deleted.', 'success')
        return redirect(url_for('admin_raceclass.main', pghead=get_pghead(), settings=UIServices.get_settings()))
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))