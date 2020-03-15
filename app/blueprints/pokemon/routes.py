from flask import render_template, url_for, redirect, flash
from flask_login import current_user, login_required
from datetime import datetime

from app.blueprints.pokemon import poke
from app.blueprints.pokemon.pokeapi import create_pokemon, upload_team, query_team, validate_teamname
from app.forms import PokemonTeamBuilder, PokemonTeamSearch, PokemonNew


@poke.route("/query", methods=["GET", "POST"])
def query():
    form = PokemonTeamSearch()
    if form.validate_on_submit():
        if form.user_query.data != "":
            results = query_team(form.user_query.data)
        else:
            results = ""
        print(results)
        return render_template("pokemon/queryteams.html", form=form, results=results)
    return render_template("pokemon/queryteams.html", form=form, results="")


@poke.route("/user/<username>/team/<teamname>")
def teampage(username, teamname):
    results = query_team(username, teamname)
    if len(results) == 1:
        return render_template("pokemon/teampage.html", results=results)
    else:
        redirect("error/404.html")


@poke.route("/user/<username>/team/<teamname>/addpokemon", methods=['GET', 'POST'])
def addnewpokemon(username, teamname):
    results = query_team(username, teamname)[0]
    form = PokemonNew()
    # Check if we are already at cap
    if int(results['count']) > 6:
        flash("You can't add anymore pokemon to this team!")
        redirect(url_for("poke.teampage", username=username, teamname=teamname))
    if current_user.username != username:
        flash("You aren't able to modify this team!")
        redirect(url_for("poke.teampage", username=username, teamname=teamname))
    if form.validate_on_submit():
        if form.pokemon.data != "":
            poke, exists = create_pokemon(form.pokemon.data, form.level.data)
            if exists:
                results["poke" + str(results['count'])] = poke
                results['count'] += 1
            else:
                flash(form.pokemon.data + " is not a valid pokemon! This data was not recorded.")
                redirect(url_for('poke.createteam', username=username, teamname=teamname))
            upload_team(results)
            return redirect(url_for("home.index"))
    return render_template('pokemon/addpokemon.html', form=form)


@poke.route("/createteam", methods=["GET", "POST"])
@login_required
def createteam():
    form = PokemonTeamBuilder()
    if form.validate_on_submit():
        if validate_teamname(current_user.username, form.teamname.data):

            poketeam = {"UserName": current_user.username, "TeamName": form.teamname.data, "TimeStamp": str(datetime.now())}
            poke_count = 1
            # Scan the data in the forms and place inside a dictionary
            if form.pokemon1.data != "":
                poke, exists = create_pokemon(form.pokemon1.data, form.poke1level.data)
                if exists:
                    poketeam["poke" + str(poke_count)] = poke
                    poke_count += 1
                else:
                    flash(form.pokemon1.data + " is not a valid pokemon! This data was not recorded.")

            if form.pokemon2.data != "":
                poke, exists = create_pokemon(form.pokemon2.data, form.poke2level.data)
                if exists:
                    poketeam["poke" + str(poke_count)] = poke
                    poke_count += 1
                else:
                    flash(form.pokemon2.data + " is not a valid pokemon! This data was not recorded.")

            if form.pokemon3.data != "":
                poke, exists = create_pokemon(form.pokemon3.data, form.poke3level.data)
                if exists:
                    poketeam["poke" + str(poke_count)] = poke
                    poke_count += 1
                else:
                    flash(form.pokemon3.data + " is not a valid pokemon! This data was not recorded.")

            if form.pokemon4.data != "":
                poke, exists = create_pokemon(form.pokemon4.data, form.poke4level.data)
                if exists:
                    poketeam["poke" + str(poke_count)] = poke
                    poke_count += 1
                else:
                    flash(form.pokemon4.data + " is not a valid pokemon! This data was not recorded.")

            if form.pokemon5.data != "":
                poke, exists = create_pokemon(form.pokemon5.data, form.poke5level.data)
                if exists:
                    poketeam["poke" + str(poke_count)] = poke
                    poke_count += 1
                else:
                    flash(form.pokemon5.data + " is not a valid pokemon! This data was not recorded.")

            if form.pokemon6.data != "":
                poke, exists = create_pokemon(form.pokemon6.data, form.poke6level.data)
                if exists:
                    poketeam["poke" + str(poke_count)] = poke
                    poke_count += 1
                else:
                    flash(form.pokemon6.data + " is not a valid pokemon! This data was not recorded.")
            poketeam['count'] = poke_count

            upload_team(poketeam)
            return redirect(url_for("home.index"))
        else:
            flash("You already have a team called " + form.teamname.data + ". Please enter in a unique name!")
            return redirect(url_for('poke.createteam'))

    return render_template("pokemon/createteam.html", form=form)
