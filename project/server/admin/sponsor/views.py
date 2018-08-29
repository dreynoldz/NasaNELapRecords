# project/server/admin/sponsor/views.py

import sys
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_required, current_user

from project.server import bcrypt, db
from project.server.models import Sponsor
from project.server.admin.sponsor.forms import SponsorForm

# Blueprints
admin_sponsor_blueprint = Blueprint('admin_sponsor', __name__,)

# Helper Functions
def get_sponsors():
    return db.session.query(Sponsor)

def get_pghead():
    return 'Sponsors'
# Route Handlers

# Track
@admin_sponsor_blueprint.route('/sponsor/main')
@login_required
def main():
    if current_user.is_admin():
        return render_template('admin/sponsor/main.html', sponsors=get_sponsors(), pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_sponsor_blueprint.route('/sponsor/create', methods=['GET', 'POST'])
@login_required
def create():
    if current_user.is_admin():
        form = SponsorForm(request.form)

        if form.validate_on_submit():
            sponsor = Sponsor(
                name=form.name.data
            )
            db.session.add(sponsor)
            db.session.commit()

            flash('New sponsor created.', 'success')
            return redirect(url_for("admin_sponsor.main", pghead=get_pghead()))
        return render_template('admin/sponsor/create.html', form=form, pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger') 
        return redirect(url_for("user.members"))

@admin_sponsor_blueprint.route('/sponsor/update/<int:sponsor_id>/', methods=['GET', 'POST'])
@login_required
def update(sponsor_id):
    if current_user.is_admin():
        sponsor = Sponsor.query.filter_by(id=sponsor_id).first()
        form = SponsorForm(request.form)

        if form.validate_on_submit():
            sponsor.name = form.name.data

            db.session.commit()

            flash('Sponsor Updated.', 'success')
            return redirect(url_for("admin_sponsor.main", pghead=get_pghead()))
        
        if sponsor:
            form.name.data = sponsor.name

        return render_template('admin/sponsor/update.html', sponsor=sponsor, form=form, pghead=get_pghead())
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))

@admin_sponsor_blueprint.route('/sponsor/delete/<int:sponsor_id>/')
@login_required
def delete(sponsor_id):
    if current_user.is_admin():
        sponsor = db.session.query(Sponsor).filter_by(id=sponsor_id)
        sponsor.delete()
        db.session.commit()
        flash('The sponsor was deleted.', 'success')
        return redirect(url_for('admin_sponsor.main', pghead=get_pghead()))
    else:
        flash('You are not an admin!', 'danger')
        return redirect(url_for("user.members"))