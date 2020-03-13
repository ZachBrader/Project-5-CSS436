from flask import render_template, url_for, redirect
from flask_login import current_user, login_required

from app.blueprints.pokemon import poke
from app.blueprints.pokemon.pokeapi import Pokemon, create_pokemon, upload_team, query_team
from app.forms import PokemonTeamBuilder, PokemonTeamSearch


@poke.route("/query", methods=["GET", "POST"])
def query():
    form = PokemonTeamSearch()
    if form.validate_on_submit():
        if form.user_query.data != "":
            results = query_team(form.user_query.data)
        else:
            results = ""
        return render_template("pokemon/queryteams.html", form=form, results=results)
    return render_template("pokemon/queryteams.html", form=form, results="")


@poke.route("/createteam", methods=["GET", "POST"])
@login_required
def createteam():
    form = PokemonTeamBuilder()
    if form.validate_on_submit():
        poketeam = {"teamname": form.teamname.data}
        poke_count = 1
        # Scan the data in the forms and place inside a dictionary
        if form.pokemon1.data != "":
            poketeam["poke" + str(poke_count)] = create_pokemon(form.pokemon1.data, form.poke1level.data)
            poke_count += 1

        if form.pokemon2.data != "":
            poketeam["poke" + str(poke_count)] = create_pokemon(form.pokemon2.data, form.poke2level.data)
            poke_count += 1

        if form.pokemon3.data != "":
            poketeam["poke" + str(poke_count)] = create_pokemon(form.pokemon3.data, form.poke3level.data)
            poke_count += 1

        if form.pokemon4.data != "":
            poketeam["poke" + str(poke_count)] = create_pokemon(form.pokemon4.data, form.poke4level.data)
            poke_count += 1

        if form.pokemon5.data != "":
            poketeam["poke" + str(poke_count)] = create_pokemon(form.pokemon5.data, form.poke5level.data)
            poke_count += 1

        if form.pokemon6.data != "":
            poketeam["poke" + str(poke_count)] = create_pokemon(form.pokemon6.data, form.poke6level.data)
            poke_count += 1

        upload_team(poketeam)
        return redirect(url_for("home.index"))

    return render_template("pokemon/createteam.html", form=form)
