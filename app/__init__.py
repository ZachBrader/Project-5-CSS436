from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager



# Initiate Flask
app = Flask(__name__)
# Connect to database
db = SQLAlchemy(app)
# Update database
migrate = Migrate(app, db)

# Write environment variables to Flask for use
app.config.from_object(Config)

login = LoginManager(app)
login.login_view = "login"

from app.blueprints.auth import auth
from app.blueprints.home import home

app.register_blueprint(home)
app.register_blueprint(auth)