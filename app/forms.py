from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, IntegerField, SelectField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
from app import pokemonList, heldItemList


mychoices = pokemonList.pokemon_list
mychoicesHeldItem = heldItemList.heldItem_list

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Please use a different username.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Please use a different email address.')


class PokemonTeamBuilder(FlaskForm):
    teamname = StringField('Team Name', validators=[DataRequired()])
    
    #pokemon1 = StringField('Pokemon #1 Name', default="Magikarp", validators=[])
    pokemon1 = SelectField('Pokemon #1', choices=mychoices)
    poke1level = IntegerField("Pokemon #1 Level", default=1, validators=[])
    pokemonHeldItem1 = SelectField('Pokemon #1 Held Item', choices=mychoicesHeldItem)
    
    #pokemon2 = StringField('Pokemon #2 Name', validators=[])
    pokemon2 = SelectField('Pokemon #2', choices=mychoices)
    poke2level = IntegerField("Pokemon #2 Level", default=1, validators=[])
    pokemonHeldItem2 = SelectField('Pokemon #2 Held Item', choices=mychoicesHeldItem)
    
    #pokemon3 = StringField('Pokemon #3 Name', validators=[])
    pokemon3 = SelectField('Pokemon #3', choices=mychoices)
    poke3level = IntegerField("Pokemon #3 Level", default=1, validators=[])
    pokemonHeldItem3 = SelectField('Pokemon #3 Held Item', choices=mychoicesHeldItem)
    
    #pokemon4 = StringField('Pokemon #4 Name', validators=[])
    pokemon4 = SelectField('Pokemon #4', choices=mychoices)
    poke4level = IntegerField("Pokemon #4 Level", default=1, validators=[])
    pokemonHeldItem4 = SelectField('Pokemon #4 Held Item', choices=mychoicesHeldItem)
    
    #pokemon5 = StringField('Pokemon #5 Name', validators=[])
    pokemon5 = SelectField('Pokemon #5', choices=mychoices)
    poke5level = IntegerField("Pokemon #5 Level", default=1, validators=[])
    pokemonHeldItem5 = SelectField('Pokemon #5 Held Item', choices=mychoicesHeldItem)
    
    #pokemon6 = StringField('Pokemon #6 Name', validators=[])
    pokemon6 = SelectField('Pokemon #6', choices=mychoices)
    poke6level = IntegerField("Pokemon #6 Level", default=1, validators=[])
    pokemonHeldItem6 = SelectField('Pokemon #6 Held Item', choices=mychoicesHeldItem)
    
    submit = SubmitField('Create Team')
    

class PokemonTeamSearch(FlaskForm):
    username_query = StringField("Search Users", validators=[])
    teamname_query = StringField("Search Teams", validators=[])
    submit = SubmitField('Search')


class PokemonNew(FlaskForm):
    pokemon = SelectField('Pokemon', choices=mychoices, validators=[DataRequired()])
    level = IntegerField("Pokemon Level", default=1, validators=[])
    item = SelectField('Pokemon Held Item', choices=mychoicesHeldItem)
    submit = SubmitField('Update')


class PokemonEdit(FlaskForm):
    
    level = IntegerField("Pokemon Level", default=1, validators=[])
    item = SelectField('Pokemon Held Item', choices=mychoicesHeldItem)
    
    move1 = SelectField('Pokemon Move #1')
    move2 = SelectField('Pokemon Move #2')
    move3 = SelectField('Pokemon Move #3')
    move4 = SelectField('Pokemon Move #4')
    
    submit = SubmitField('Update')


class EditTeam(FlaskForm):
    pokemon1 = SelectField('Pokemon #1', choices=mychoices)
    poke1level = IntegerField("Pokemon #1 Level", default=1, validators=[])
    pokemonHeldItem1 = SelectField('Pokemon #1 Held Item', choices=mychoicesHeldItem)

    pokemon2 = SelectField('Pokemon #2', choices=mychoices)
    poke2level = IntegerField("Pokemon #2 Level", default=1, validators=[])
    pokemonHeldItem2 = SelectField('Pokemon #2 Held Item', choices=mychoicesHeldItem)

    pokemon3 = SelectField('Pokemon #3', choices=mychoices)
    poke3level = IntegerField("Pokemon #3 Level", default=1, validators=[])
    pokemonHeldItem3 = SelectField('Pokemon #3 Held Item', choices=mychoicesHeldItem)

    pokemon4 = SelectField('Pokemon #4', choices=mychoices)
    poke4level = IntegerField("Pokemon #4 Level", default=1, validators=[])
    pokemonHeldItem4 = SelectField('Pokemon #4 Held Item', choices=mychoicesHeldItem)

    pokemon5 = SelectField('Pokemon #5', choices=mychoices)
    poke5level = IntegerField("Pokemon #5 Level", default=1, validators=[])
    pokemonHeldItem5 = SelectField('Pokemon #5 Held Item', choices=mychoicesHeldItem)

    pokemon6 = SelectField('Pokemon #6', choices=mychoices)
    poke6level = IntegerField("Pokemon #6 Level", default=1, validators=[])
    pokemonHeldItem6 = SelectField('Pokemon #6 Held Item', choices=mychoicesHeldItem)

    submit = SubmitField('Update Team')
