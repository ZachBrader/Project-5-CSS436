import os
from decimal import Decimal
import json

from config import TABLE
from boto3.dynamodb.conditions import Key, Attr

class Pokemon():
    def __init__(self, pokemon_id=1):
        self.pokemon_id = pokemon_id
        self.name = "Bulbasaur"
        self.level = 100
        self.gender = "Random"
        self.shiny = "No"
        self.item = None
        self.ability = "Overgrow"
        self.moves = {
            "move_1": "Tackle", "move_2": None,
            "move_3": None, "move_4": None
        }
        self.stat = {
            "pokemon_nature": "Serious",
            "pokemon_hp": 294,
            "pokemon_attack": 104,
            "pokemon_defense": 197,
            "pokemon_SpAtk": 166,
            "pokemon_spDef": 166,
            "pokemon_speed": 126,
        }


def create_pokemon(name, level):
    """
    Formats pokemon details into a dictionary

    :param name: String object representing a pokemon's name
    :param level: Integer object representing a pokemon's level
    :return: A formatted dictionary
    """
    poke = {}
    poke['name'] = name
    if level != "":
        poke['level'] = level
    return poke


def upload_team(poketeam):
    """
    Uploads a pokemon to our dynamoDB table

    :param poketeam: A dictionary object with a teamname, and 0-6 pokemon
    :return:
    """
    print(TABLE.put_item(Item=poketeam))
    return True


def query_team(username=None, teamname=None):
    """
    Query our DynamoDb for this parameter
    :param username: Query parameter to check all usernames for
    :param teamname: Query parameter to check all teamnames for
    :return:
    """
    totalItems = []
    if (username is not None and username != "") and (teamname is not None and teamname != ""):
        response = TABLE.scan(
            FilterExpression=Attr('UserName').contains(username) & Attr('TeamName').contains(teamname))
        totalItems += response['Items']
    elif (username is not None and username != "") and (teamname is None or teamname == ""):
        response = TABLE.scan(FilterExpression=Attr('UserName').contains(username))
        totalItems += response['Items']
    elif (username is None or username == "") and (teamname is not None and teamname != ""):
        response = TABLE.scan(FilterExpression=Attr('TeamName').contains(teamname))
        totalItems += response['Items']
    else:
        response = TABLE.scan()
        totalItems += response['Items']
    return totalItems


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)