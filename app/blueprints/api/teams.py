from app.blueprints.api import api


@api.route('/user', methods=['POST'])
def create_user():
    return {}

@api.route('/users/<id>', methods=['GET'])
def get_user(id):
    return {}


@api.route('/users', methods=['GET'])
def get_users():
    return {}


@api.route('/teams', methods=['GET'])
def get_teams():
    return {}


@api.route('/teams/<int:id>', methods=['GET'])
def get_team(id):
    return {}

