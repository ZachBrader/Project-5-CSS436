from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user, login_required
from datetime import datetime

from app.blueprints.pokemon import poke
from app.blueprints.pokemon.pokeapi import create_pokemon, upload_team, query_team, validate_teamname
from app.forms import PokemonTeamBuilder, PokemonTeamSearch, PokemonNew, EditTeam


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
        flash("Unable to find " + teamname + " by " + username + ".")
        return redirect(url_for("home.index"))


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
            poke, exists = create_pokemon(form.pokemon.data, form.level.data, form.item.data)
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
            pokemon = []
            # Scan the data in the forms and place inside a dictionary
            if form.pokemon1.data != "":
                poke, exists = create_pokemon(form.pokemon1.data, form.poke1level.data, form.pokemonHeldItem1.data)
                if exists:
                    pokemon.append(poke)
                    poke_count += 1
                else:
                    flash(form.pokemon1.data + " is not a valid pokemon! This data was not recorded.")

            if form.pokemon2.data != "":
                poke, exists = create_pokemon(form.pokemon2.data, form.poke2level.data, form.pokemonHeldItem2.data)
                if exists:
                    pokemon.append(poke)
                    poke_count += 1
                else:
                    flash(form.pokemon2.data + " is not a valid pokemon! This data was not recorded.")

            if form.pokemon3.data != "":
                poke, exists = create_pokemon(form.pokemon3.data, form.poke3level.data, form.pokemonHeldItem3.data)
                if exists:
                    pokemon.append(poke)
                    poke_count += 1
                else:
                    flash(form.pokemon3.data + " is not a valid pokemon! This data was not recorded.")

            if form.pokemon4.data != "":
                poke, exists = create_pokemon(form.pokemon4.data, form.poke4level.data, form.pokemonHeldItem4.data)
                if exists:
                    pokemon.append(poke)
                    poke_count += 1
                else:
                    flash(form.pokemon4.data + " is not a valid pokemon! This data was not recorded.")

            if form.pokemon5.data != "":
                poke, exists = create_pokemon(form.pokemon5.data, form.poke5level.data, form.pokemonHeldItem5.data)
                if exists:
                    pokemon.append(poke)
                    poke_count += 1
                else:
                    flash(form.pokemon5.data + " is not a valid pokemon! This data was not recorded.")

            if form.pokemon6.data != "":
                poke, exists = create_pokemon(form.pokemon6.data, form.poke6level.data, form.pokemonHeldItem6.data)
                if exists:
                    pokemon.append(poke)
                    poke_count += 1
                else:
                    flash(form.pokemon6.data + " is not a valid pokemon! This data was not recorded.")
            poketeam['count'] = poke_count
            poketeam['pokemon'] = pokemon
            upload_team(poketeam)
            return redirect(url_for("home.index"))
        else:
            flash("You already have a team called " + form.teamname.data + ". Please enter in a unique name!")
            return redirect(url_for('poke.createteam'))

    return render_template("pokemon/createteam.html", form=form)


@poke.route("/user/<username>/editteam/<teamname>", methods=["GET", "POST"])
@login_required
def editteam(teamname, username):
    form = EditTeam()
    results = query_team(current_user.username, teamname)
    if len(results) == 0 or current_user.username != username:
        flash("Unable to edit team " + teamname)
        redirect(url_for('home.user', username=username))
    else:
        results = results[0]
    if form.validate_on_submit():
        poketeam = {"UserName": username, "TeamName": teamname, "TimeStamp": str(datetime.now())}
        poke_count = 1
        # Scan the data in the forms and place inside a dictionary
        if form.pokemon1.data != "":
            poke, exists = create_pokemon(form.pokemon1.data, form.poke1level.data, form.pokemonHeldItem1.data)
            if exists:
                poketeam["poke" + str(poke_count)] = poke
                poke_count += 1
            else:
                flash(form.pokemon1.data + " is not a valid pokemon! This data was not recorded.")

        if form.pokemon2.data != "":
            poke, exists = create_pokemon(form.pokemon2.data, form.poke2level.data, form.pokemonHeldItem2.data)
            if exists:
                poketeam["poke" + str(poke_count)] = poke
                poke_count += 1
            else:
                flash(form.pokemon2.data + " is not a valid pokemon! This data was not recorded.")

        if form.pokemon3.data != "":
            poke, exists = create_pokemon(form.pokemon3.data, form.poke3level.data, form.pokemonHeldItem3.data)
            if exists:
                poketeam["poke" + str(poke_count)] = poke
                poke_count += 1
            else:
                flash(form.pokemon3.data + " is not a valid pokemon! This data was not recorded.")

        if form.pokemon4.data != "":
            poke, exists = create_pokemon(form.pokemon4.data, form.poke4level.data, form.pokemonHeldItem4.data)
            if exists:
                poketeam["poke" + str(poke_count)] = poke
                poke_count += 1
            else:
                flash(form.pokemon4.data + " is not a valid pokemon! This data was not recorded.")

        if form.pokemon5.data != "":
            poke, exists = create_pokemon(form.pokemon5.data, form.poke5level.data, form.pokemonHeldItem5.data)
            if exists:
                poketeam["poke" + str(poke_count)] = poke
                poke_count += 1
            else:
                flash(form.pokemon5.data + " is not a valid pokemon! This data was not recorded.")

        if form.pokemon6.data != "":
            poke, exists = create_pokemon(form.pokemon6.data, form.poke6level.data, form.pokemonHeldItem6.data)
            if exists:
                poketeam["poke" + str(poke_count)] = poke
                poke_count += 1
            else:
                flash(form.pokemon6.data + " is not a valid pokemon! This data was not recorded.")
        poketeam['count'] = poke_count

        upload_team(poketeam)
        return redirect(url_for("home.index"))
    elif request.method == 'GET':
        form.poke1level.data = results['poke1']['level']
        form.poke2level.data = results['poke2']['level']
        form.poke3level.data = results['poke3']['level']
        form.poke4level.data = results['poke4']['level']
        form.poke5level.data = results['poke5']['level']
        form.poke6level.data = results['poke6']['level']

        form.pokemonHeldItem1.data = results['poke1']['item']
        form.pokemonHeldItem2.data = results['poke2']['item']
        form.pokemonHeldItem3.data = results['poke3']['item']
        form.pokemonHeldItem4.data = results['poke4']['item']
        form.pokemonHeldItem5.data = results['poke5']['item']
        form.pokemonHeldItem6.data = results['poke6']['item']

        form.pokemon1.data = results['poke1']['name']
        form.pokemon2.data = results['poke2']['name']
        form.pokemon3.data = results['poke3']['name']
        form.pokemon4.data = results['poke4']['name']
        form.pokemon5.data = results['poke5']['name']
        form.pokemon6.data = results['poke6']['name']

    return render_template('pokemon/editteam.html', form=form)


@poke.route("/user/<username>/team/<teamname>/deletepokemon/<int:slot>", methods=["GET", "POST"])
@login_required
def deletepokemon(teamname, username, slot):
    if current_user.username == username:
        if 0 < slot < 7:
            results = query_team(username, teamname)
            if len(results) != 0:
                results = results[0]
                poke_num = "poke" + str(slot)
                if poke_num in results:
                    ret =results.pop(poke_num)
                    flash("Removed " + str(ret) + " from " + teamname)
                    upload_team(results)
    return redirect(url_for('poke.teampage', username=username, teamname=teamname))
