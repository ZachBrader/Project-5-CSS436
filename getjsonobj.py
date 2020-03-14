import requests
import json

def GetObjectByName(pokemon_id):
    if isinstance(pokemon_id, int):
        return GetObjectByID(pokemon_id)
    else:
        attempt_url = 'https://pokeapi.co/api/v2/pokemon/' + str(pokemon_id).lower() + '/'
        response = requests.get(attempt_url)
        if response.ok:
            obj = json.loads(response.content)
            return CreateJsonObj(obj)
        else:
            print('Pokemon not found')
            return {}


def GetObjectByID(pokemon_id):
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
