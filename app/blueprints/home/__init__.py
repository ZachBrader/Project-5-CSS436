from flask import Blueprint

home = Blueprint('home', __name__)

from app.blueprints.home import routes