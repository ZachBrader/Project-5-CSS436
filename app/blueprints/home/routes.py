from flask_login import login_required
from flask import render_template

from app.blueprints.home import home
from app.models import User

@home.route('/')
@home.route('/index')
def index():
    return render_template("home/index.html")


@home.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('home/user.html', user=user)