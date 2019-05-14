# project/server/__init__.py


import os, datetime

from flask import Flask, render_template
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from flask_debugtoolbar import DebugToolbarExtension
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache


# instantiate the extensions
login_manager = LoginManager()
bcrypt = Bcrypt()
toolbar = DebugToolbarExtension()
bootstrap = Bootstrap()
db = SQLAlchemy()
migrate = Migrate()
cache = Cache()

def create_app(script_info=None):

    # instantiate the app
    app = Flask(
        __name__,
        template_folder='../client/templates',
        static_folder='../client/static'
    )

    # set config
    app_settings = os.getenv(
        'APP_SETTINGS', 'project.server.config.DevelopmentConfig')
    app.config.from_object(app_settings)

    # set up extensions
    login_manager.init_app(app)
    bcrypt.init_app(app)
    toolbar.init_app(app)
    bootstrap.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    cache.init_app(app)
    

    # register blueprints
    from project.server.user.views import user_blueprint
    from project.server.main.views import main_blueprint
    from project.server.admin.views import admin_blueprint
    app.register_blueprint(user_blueprint)
    app.register_blueprint(main_blueprint)
    app.register_blueprint(admin_blueprint)


    # create custom filter
    @app.template_filter()
    def datetime_filter(dttm):
        return dttm.strftime("%Y-%m-%d %H:%M:%S")

    # flask login
    from project.server.models import User
    login_manager.login_view = 'user.login'
    login_manager.login_message_category = 'danger'

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.filter(User.id == int(user_id)).first()
    
        #return app
    from project.server.dataservices import UIServices

    # error handlers
    @app.errorhandler(401)
    def unauthorized_page(error):
        return render_template('errors/401.html', settings=UIServices.get_settings()), 401

    @app.errorhandler(403)
    def forbidden_page(error):
        return render_template('errors/403.html', settings=UIServices.get_settings()), 403

    @app.errorhandler(404)
    def page_not_found(error):
        return render_template('errors/404.html', settings=UIServices.get_settings()), 404

    @app.errorhandler(500)
    def server_error_page(error):
        return render_template('errors/500.html', settings=UIServices.get_settings()), 500

    # shell context for flask cli
    app.shell_context_processor({'app': app, 'db': db})

    return app
