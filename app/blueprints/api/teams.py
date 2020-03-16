from flask import jsonify, request, url_for
import json
from dynamodb_json import json_util
from app.blueprints.api import api
from app.models import User
from app import db
from app.blueprints.api.errors import bad_request
from app.blueprints.api.auth import token_auth
from app.blueprints.pokemon.pokeapi import query_team

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
@token_auth.login_required
def get_users():
    return {}


@api.route('/teams', methods=['GET'])
@token_auth.login_required
def get_teams():
    teams = json_util.loads(query_team())
    num_teams = len(teams)
    return jsonify({'_meta': {'total_teams': num_teams}, "teams": teams})


@api.route('/teams/<teamname>', methods=['GET'])
@token_auth.login_required
def get_team_by_teamnames(teamname):
    teams = json_util.loads(query_team(teamname=teamname))
    num_teams = len(teams)
    return jsonify({'_meta': {'total_teams': num_teams}, "teams": teams})


@api.route('/user/<username>/teams/<teamname>', methods=['GET'])
@token_auth.login_required
def get_team(username, teamname):
    teams = json_util.loads(query_team(username=username, teamname=teamname))
    num_teams = len(teams)
    return jsonify({'_meta': {'total_teams': num_teams}, "teams": teams})


