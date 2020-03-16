import requests
from decimal import Decimal
import json

from config import TABLE
from boto3.dynamodb.conditions import Key, Attr


def create_pokemon(name, level, item=""):
    """
    Formats pokemon details into a dictionary

    :param name: String object representing a pokemon's name
    :param level: Integer object representing a pokemon's level
    :return: A formatted dictionary
    """
    exists, pokemon_details = GetObjectByName(name)
    poke = {}
    if exists:
        poke['name'] = name
        poke['id'] = pokemon_details['id']
        poke['hidden_abilities'] = pokemon_details['hidden_abilities']
        poke['picture'] = FindByID(poke['id'])
        if level != "":
            poke['level'] = level
        if item != "":
            poke['item'] = item
        return poke, True
    else:
        return poke, False


def upload_team(poketeam):
    """
    Uploads a pokemon to our dynamoDB table

    :param poketeam: A dictionary object with a teamname, and 0-6 pokemon
    :return:
    """
    print(TABLE.put_item(Item=poketeam))
    return True

# Get a list of pokemon move from given pokemon name
def GetPokemonMove(pokemon_name):
    content = json.dumps(GetObjectByName(pokemon_name)[1])
    data = json.loads(content)
    return data['moves']

# Create a given pokemon move list for wtform select
def CreatePokemonMoveSelectList(moveList):
    pokemonMove_list = []
    temp = ('None', 'None')
    pokemonMove_list.append(temp)
    for move in moveList:
        tup = (move.strip(), move.strip())
        pokemonMove_list.append(tup)
    return pokemonMove_list

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

def delete_team(username, teamname):
    try:
        TABLE.delete_item(Key={'UserName': username, 'TeamName': teamname})
        return True
    except:
        print('Unable to delete ' + username + '\'s team ' + teamname)
        return False


def validate_teamname(username, teamname):
    response = TABLE.scan(
        FilterExpression=Attr('UserName').eq(username) & Attr('TeamName').eq(teamname))
    print(response)
    if len(response['Items']) == 0:
        return True
    else:
        print("Team name: " + teamname + " already exists!")
        return False


# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)


def GetObjectByName(pokemon_id):
    try:
        if isinstance(pokemon_id, int):
            return GetObjectByID(pokemon_id)
        else:
            attempt_url = 'https://pokeapi.co/api/v2/pokemon/' + str(pokemon_id).lower() + '/'
            response = requests.get(attempt_url)
            print(response)
            if response.ok and response.status_code == 200:
                obj = json.loads(response.content)
                return True, CreateJsonObj(obj)
            else:
                print('Pokemon not found')
                return False, {}
    except Exception as e:
        print("Pokemon not found, received: ", e)
        return False, {}


def GetObjectByID(pokemon_id):
    try:
        if not isinstance(pokemon_id, int):
            GetObjectByName(pokemon_id)

        request_url = 'https://pokeapi.co/api/v2/pokemon/' + str(pokemon_id) + '/'
        response = requests.get(request_url)
        if response.ok:
            obj = json.loads(response.content)
            return CreateJsonObj(obj)
        else:
            print('Image not found')
            return {}
    except Exception as e:
        print("Image not found, received: ", e)
        return {}


# Do not call this function! Call GetObjectByID or GetObjectByName
def CreateJsonObj(obj):
    # Get name
    name = obj['name']

    # Get ID
    id = obj['id']

    # Get Types
    list_types = []
    index = 0
    while index < len(obj['types']):
        list_types.append(obj['types'][index]['type']['name'])
        index += 1

    # Get Abilities
    # Get Hidden Abilities
    abilities = []
    hidden_abilities = []

    index = 0
    while index < len(obj['abilities']):
        if obj['abilities'][index]['is_hidden']:
            hidden_abilities.append(obj['abilities'][index]['ability']['name'])
        else:
            abilities.append(obj['abilities'][index]['ability']['name'])
        index += 1

    # Get List of Moves
    list_moves = []
    index = 0
    while index < len(obj['moves']):
        list_moves.append(obj['moves'][index]['move']['name'])
        index += 1

    json_obj = {
        "name": name,
        "id": id,
        "abilities": abilities,
        "hidden_abilities": hidden_abilities,
        "moves": list_moves
    }
    return json_obj


def FindByID(pokemon_id):
    if pokemon_id < 10:
        str_for_input = '00' + str(pokemon_id)
    elif pokemon_id < 100:
        str_for_input = '0' + str(pokemon_id)
    else:
        str_for_input = str(pokemon_id)

    image_url = 'https://pokemonimagescss436.s3-us-west-2.amazonaws.com/' + str_for_input + '.png'
    response = requests.get(image_url)
    if response.ok:
        print('Image found! ' + image_url)
    else:
        print('Image not found')
    print(response.status_code)
    return image_url
