from flask_login import login_required
from flask import render_template

from app.blueprints.home import home
from app.models import User
from app.blueprints.pokemon.pokeapi import query_team

@home.route('/')
@home.route('/index')
def index():
    pokeList = query_team()
    return render_template("home/index.html", pokeList=pokeList)


@home.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    pokeList = query_team(username=username)
    return render_template('home/user.html', user=user, pokeList=pokeList)