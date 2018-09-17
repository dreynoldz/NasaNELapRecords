# project/server/main/views.py


import datetime
from flask import render_template, Blueprint, url_for, \
    redirect, flash, request
from flask_login import login_user, logout_user, login_required

from project.server import db
from project.server.models import BestLap


main_blueprint = Blueprint('main', __name__,)

# Helper Functions
def get_bestlaps():
    return db.session.query(BestLap)

@main_blueprint.route('/')
def home():
    return render_template('main/home.html', bestlaps=get_bestlaps())


@main_blueprint.route("/about/")
def about():
    return render_template("main/about.html")
