from flask import Blueprint

error = Blueprint('error', __name__)

from app.blueprints.errors import routes