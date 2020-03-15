from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
import logging
from logging.handlers import RotatingFileHandler
import os
from flask_bootstrap import Bootstrap

login = LoginManager()
bootstrap = Bootstrap()
# Connect to database
db = SQLAlchemy()
# Update database
migrate = Migrate()

def create_app():
    # Initiate Flask
    app = Flask(__name__)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    bootstrap.init_app(app)

    # Write environment variables to Flask for use
    app.config.from_object(Config)

    from app.blueprints.auth import auth
    from app.blueprints.home import home
    from app.blueprints.errors import error
    from app.blueprints.pokemon import poke
    from app.blueprints.api import api

    app.register_blueprint(api, url_prefix='/api')
    app.register_blueprint(poke)
    app.register_blueprint(error)
    app.register_blueprint(home)
    app.register_blueprint(auth)

    login.login_view = "auth.login"

    if not app.debug:
        if not os.path.exists('logs'):
            os.mkdir('logs')
        file_handler = RotatingFileHandler('logs/pokelog.log', maxBytes=10240, backupCount=10)
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info('Program startup')

    return app