from flask import jsonify
from app.blueprints.api import api
from app.models import User

@api.route('/users', methods=['POST'])
def create_user():
    #data = request.get_json()
    return {}

@api.route('/users/<int:id>', methods=['GET'])
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())


@api.route('/users', methods=['GET'])
def get_users():
    return {}


@api.route('/teams', methods=['GET'])
def get_teams():
    return {}


@api.route('/teams/<int:id>', methods=['GET'])
def get_team(id):
    return {}

