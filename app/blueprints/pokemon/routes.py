from flask import render_template, url_for, redirect, flash, request
from flask_login import current_user, login_required
from datetime import datetime

from app.blueprints.pokemon import poke
from app.blueprints.pokemon.pokeapi import create_pokemon, upload_team, query_team, validate_teamname, delete_team
from app.forms import PokemonTeamBuilder, PokemonTeamSearch, PokemonNew, EditTeam


@poke.route("/query", methods=["GET", "POST"])
def query():
    form = PokemonTeamSearch()
    if form.validate_on_submit():
        username_query = form.username_query.data
        teamname_query = form.teamname_query.data
        if username_query != "" and teamname_query != "":
            results = query_team(username=username_query, teamname=teamname_query)
        elif username_query != "" and teamname_query == "":
            results = query_team(username=username_query)
        elif username_query == "" and teamname_query != "":
            results = query_team(teamname=teamname_query)
        else:
            results = query_team()
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
                results['pokemon'].append(poke)
                results['count'] = len(results['pokemon'])
            else:
                flash(form.pokemon.data + " is not a valid pokemon! This data was not recorded.")
                redirect(url_for('poke.createteam', username=username, teamname=teamname))
            upload_team(results)
            return redirect(url_for('poke.teampage', username=username, teamname=teamname))
    return render_template('pokemon/addpokemon.html', form=form)


@poke.route("/createteam", methods=["GET", "POST"])
@login_required
def createteam():
    form = PokemonTeamBuilder()
    if form.validate_on_submit():
        if validate_teamname(current_user.username, form.teamname.data):
            poketeam = {"UserName": current_user.username, "TeamName": form.teamname.data, "TimeStamp": str(datetime.now())}
            pokemon = []
            # Scan the data in the forms and place inside a dictionary
            if form.pokemon1.data != "":
                poke, exists = create_pokemon(form.pokemon1.data, form.poke1level.data, form.pokemonHeldItem1.data)
                if exists:
                    pokemon.append(poke)
                else:
                    flash(form.pokemon1.data + " is not a valid pokemon! This data was not recorded.")

            if form.pokemon2.data != "":
                poke, exists = create_pokemon(form.pokemon2.data, form.poke2level.data, form.pokemonHeldItem2.data)
                if exists:
                    pokemon.append(poke)
                else:
                    flash(form.pokemon2.data + " is not a valid pokemon! This data was not recorded.")

            if form.pokemon3.data != "":
                poke, exists = create_pokemon(form.pokemon3.data, form.poke3level.data, form.pokemonHeldItem3.data)
                if exists:
                    pokemon.append(poke)
                else:
                    flash(form.pokemon3.data + " is not a valid pokemon! This data was not recorded.")

            if form.pokemon4.data != "":
                poke, exists = create_pokemon(form.pokemon4.data, form.poke4level.data, form.pokemonHeldItem4.data)
                if exists:
                    pokemon.append(poke)
                else:
                    flash(form.pokemon4.data + " is not a valid pokemon! This data was not recorded.")

            if form.pokemon5.data != "":
                poke, exists = create_pokemon(form.pokemon5.data, form.poke5level.data, form.pokemonHeldItem5.data)
                if exists:
                    pokemon.append(poke)
                else:
                    flash(form.pokemon5.data + " is not a valid pokemon! This data was not recorded.")

            if form.pokemon6.data != "":
                poke, exists = create_pokemon(form.pokemon6.data, form.poke6level.data, form.pokemonHeldItem6.data)
                if exists:
                    pokemon.append(poke)
                else:
                    flash(form.pokemon6.data + " is not a valid pokemon! This data was not recorded.")
            poketeam['count'] = len(pokemon)
            poketeam['pokemon'] = pokemon
            upload_team(poketeam)
            return redirect(url_for('poke.teampage', username=current_user.username, teamname=form.teamname.data))
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
        pokemon = []
        # Scan the data in the forms and place inside a dictionary
        if form.pokemon1.data != "":
            poke, exists = create_pokemon(form.pokemon1.data, form.poke1level.data, form.pokemonHeldItem1.data)
            if exists:
                pokemon.append(poke)
            else:
                flash(form.pokemon1.data + " is not a valid pokemon! This data was not recorded.")

        if form.pokemon2.data != "":
            poke, exists = create_pokemon(form.pokemon2.data, form.poke2level.data, form.pokemonHeldItem2.data)
            if exists:
                pokemon.append(poke)
            else:
                flash(form.pokemon2.data + " is not a valid pokemon! This data was not recorded.")

        if form.pokemon3.data != "":
            poke, exists = create_pokemon(form.pokemon3.data, form.poke3level.data, form.pokemonHeldItem3.data)
            if exists:
                pokemon.append(poke)
            else:
                flash(form.pokemon3.data + " is not a valid pokemon! This data was not recorded.")

        if form.pokemon4.data != "":
            poke, exists = create_pokemon(form.pokemon4.data, form.poke4level.data, form.pokemonHeldItem4.data)
            if exists:
                pokemon.append(poke)
            else:
                flash(form.pokemon4.data + " is not a valid pokemon! This data was not recorded.")

        if form.pokemon5.data != "":
            poke, exists = create_pokemon(form.pokemon5.data, form.poke5level.data, form.pokemonHeldItem5.data)
            if exists:
                pokemon.append(poke)
            else:
                flash(form.pokemon5.data + " is not a valid pokemon! This data was not recorded.")

        if form.pokemon6.data != "":
            poke, exists = create_pokemon(form.pokemon6.data, form.poke6level.data, form.pokemonHeldItem6.data)
            if exists:
                pokemon.append(poke)
            else:
                flash(form.pokemon6.data + " is not a valid pokemon! This data was not recorded.")
        poketeam['count'] = len(pokemon)
        poketeam['pokemon'] = pokemon
        upload_team(poketeam)
        return redirect(url_for("home.index"))
    elif request.method == 'GET':
        count = results['count']
        form.poke1level.data = results['pokemon'][0]['level'] if count > 0 else 1
        form.poke2level.data = results['pokemon'][1]['level'] if count > 1 else 1
        form.poke3level.data = results['pokemon'][2]['level'] if count > 2 else 1
        form.poke4level.data = results['pokemon'][3]['level'] if count > 3 else 1
        form.poke5level.data = results['pokemon'][4]['level'] if count > 4 else 1
        form.poke6level.data = results['pokemon'][5]['level'] if count > 5 else 1

        form.pokemonHeldItem1.data = results['pokemon'][0]['item'] if count > 0 else ""
        form.pokemonHeldItem2.data = results['pokemon'][1]['item'] if count > 1 else ""
        form.pokemonHeldItem3.data = results['pokemon'][2]['item'] if count > 2 else ""
        form.pokemonHeldItem4.data = results['pokemon'][3]['item'] if count > 3 else ""
        form.pokemonHeldItem5.data = results['pokemon'][4]['item'] if count > 4 else ""
        form.pokemonHeldItem6.data = results['pokemon'][5]['item'] if count > 5 else ""

        form.pokemon1.data = results['pokemon'][0]['name'] if count > 0 else ""
        form.pokemon2.data = results['pokemon'][1]['name'] if count > 1 else ""
        form.pokemon3.data = results['pokemon'][2]['name'] if count > 2 else ""
        form.pokemon4.data = results['pokemon'][3]['name'] if count > 3 else ""
        form.pokemon5.data = results['pokemon'][4]['name'] if count > 4 else ""
        form.pokemon6.data = results['pokemon'][5]['name'] if count > 5 else ""

    return render_template('pokemon/editteam.html', form=form)


@poke.route("/user/<username>/team/<teamname>/deletepokemon/<int:slot>", methods=["GET", "POST"])
@login_required
def deletepokemon(teamname, username, slot):
    if current_user.username == username:
        if 0 <= slot < 6:
            results = query_team(username, teamname)
            if len(results) != 0:
                try:
                    results = results[0]
                    ret = results['pokemon'].pop(slot)
                    flash("Removed " + str(ret) + " from " + teamname)
                    results['count'] = len(results['pokemon'])
                    upload_team(results)
                except:
                    flash("Unable to find pokemon at slot " + str(slot))
            else:
                flash("Unable to find team; It might have been moved!")
        else:
            flash("You need to enter in a valid position for a pokemon on the team!")
    else:
        flash("You do not have permissions to edit this team")
    return redirect(url_for('poke.teampage', username=username, teamname=teamname))


@poke.route("/user/<username>/team/<teamname>/editpokemon/<int:slot>", methods=["GET", "POST"])
@login_required
def editpokemon(teamname, username, slot):
    # Make sure we have a valid number
    if 0 <= slot < 6:
        form = PokemonNew()
        # Receive the json for this team
        results = query_team(username, teamname)[0]
        # Once user clicks submit
        if form.validate_on_submit():
            # This user is authorized to do this
            if current_user.username == username:
                # Try to update
                try:
                    poke, exists = create_pokemon(form.pokemon.data, form.level.data, form.item.data)
                    if exists:
                        # Pokemon is valid, let's update
                        results['pokemon'][slot] = poke
                        flash("Edited Pokemon " + str(slot) + " in " + teamname)
                        results['count'] = len(results['pokemon'])
                        upload_team(results)

                        # Show user the new team combination
                        return redirect(url_for('poke.teampage', username=username, teamname=teamname))
                    else:
                        flash("Unable to edit pokemon")
                        return redirect(url_for('poke.editpokemon', username=username, teamname=teamname, slot=slot))
                except Exception as E:
                    flash("Unable to find pokemon at slot " + str(slot))
            else:
                flash("You do not have permissions to edit this team")
                return redirect(url_for('poke.teampage', username=username, teamname=teamname))
        # Tell user current information about pokemon
        elif request.method == 'GET':
            # Total number of pokemon on this team
            count = results['count']
            print("DETAILS", slot, count)
            if slot >= count and count <= 5:
                return redirect(url_for('poke.addnewpokemon', username=username, teamname=teamname))
            elif slot >= count >= 6:
                flash('Unable to update that pokemon')
                return redirect(url_for('poke.teampage', username=username, teamname=teamname))
            form.pokemon.data = results['pokemon'][slot]['name']
            form.level.data = results['pokemon'][slot]['level']
            form.item.data = results['pokemon'][slot]['item']
        return render_template('pokemon/addpokemon.html', form=form)

    else:
        flash("You need to enter in a valid position for a pokemon on the team!")
        return redirect(url_for('poke.teampage', username=username, teamname=teamname))


@poke.route("/user/<username>/team/<teamname>/deleteteam", methods=["GET", "POST"])
@login_required
def deleteteam(teamname, username):
    if current_user.username == username:
        results = query_team(username, teamname)
        if len(results) != 0:
            ret = delete_team(username, teamname)
            if ret:
                flash(teamname + " deleted successfully!")
            else:
                flash(teamname + " was unable to be deleted")
                return redirect(url_for('poke.teampage', username=username, teamname=teamname))
    return redirect(url_for('home.user', username=username))