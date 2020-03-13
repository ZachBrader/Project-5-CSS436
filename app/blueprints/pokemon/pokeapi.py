# Stolen from Thom's code. I'll let you guys plug this in how you want
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
    print(poketeam)
    return True


def query_team(user_query):
    """
    Query our DynamoDb for this parameter
    :param user_query:
    :return:
    """
    print(user_query)
    return "Implement something cool here!"