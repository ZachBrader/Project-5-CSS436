from flask_login import login_required
from flask import render_template

from app.blueprints.home import home
from app.models import User

@home.route('/')
@home.route('/index')
def index():
    pokeList = [{
            'username': 'Zach',
            'pokemon': ['Pichu', 'Pichu', 'Pichu']
        },
        {
            'username': 'Andrei',
            'pokemon': ['Magikarp']
        },
        {
            'username': 'Thom',
            'pokemon': ['Charizard']
        }
    ]
    return render_template("home/index.html", pokeList=pokeList)


@home.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    pokeList = [{
        'username': 'Zach',
        'pokemon': ['Pichu', 'Pichu', 'Pichu']
    },
        {
            'username': 'Andrei',
            'pokemon': ['Magikarp']
        },
        {
            'username': 'Thom',
            'pokemon': ['Charizard']
        }
    ]
    return render_template('home/user.html', user=user, pokeList=pokeList)