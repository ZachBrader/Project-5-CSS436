from flask import jsonify, g
from app import db
from app.blueprints.api import api
from app.blueprints.api.auth import basic_auth


@api.route('/token', methods=['POST'])
@basic_auth.login_required
def get_token():
    token = g.current_user.get_token()
    db.session.commit()
    return jsonify({'token': token})


def revoke_token():
    pass
