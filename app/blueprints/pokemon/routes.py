from flask import render_template, url_for, redirect
from flask_login import current_user, login_required

from app.blueprints.pokemon import poke
from app.forms import PokemonTeamBuilder


@poke.route("/createteam")
@login_required
def createteam():
    form = PokemonTeamBuilder()
    if form.validate_on_submit():
        pass
    return render_template("pokemon/createteam.html")