from flask import jsonify, request, url_for
from app.blueprints.api import api
from app.models import User
from app import db
from app.blueprints.api.errors import bad_request



@api.route('/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    if 'username' not in data or 'email' not in data or 'password' not in data:
        return bad_request('Must include username, email, and password fields!')
    if User.query.filter_by(username=data['username']).first():
        return bad_request('Please use a different username; Already in use')
    if User.query.filter_by(username=data['email']).first():
        return bad_request('Please use a different email; Already in use')

    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()
    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)
    return response

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

