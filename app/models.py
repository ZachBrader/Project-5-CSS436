import base64
import os

from app import db
from datetime import datetime, timedelta
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin
from flask import url_for


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    token = db.Column(db.String(32), index=True, unique=True)
    token_expiration = db.Column(db.DateTime)

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def to_dict(self):
        data = {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            '_links': {
                'self': url_for('api.get_user', id=self.id)
            }
        }
        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        if new_user and 'password' in data:
            self.set_password(data['password'])

    def get_token(self, expires_in=3600):
        # Set Time of token
        now = datetime.utcnow()
        # As long as token has time, let's keep using it
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        # Make a new token
        self.token = base64.b64encode(os.urandom(24)).decode('utf-8')
        # Reset the token
        self.token_expiration = now + timedelta(seconds=expires_in)
        # Record in database
        db.session.add(self)
        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user