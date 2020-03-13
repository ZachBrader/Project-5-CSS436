from flask import Blueprint

poke = Blueprint('poke', __name__)

from app.blueprints.pokemon import routes