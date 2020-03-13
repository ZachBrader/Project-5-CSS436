import uploaddb
import json

# Testing Area
class Pokemon:
	def __init__(self, pokemon_id = 1):
		self.pokemon_id = pokemon_id
		self.name = "Bulbasaur"
		self.level = 100
		self.gender = "Random"
		self.shiny = "No"
		self.item = None
		self.ability = "Overgrow"
		self.moves = {
			"move_1" : "Tackle", "move_2" : None,
			"move_3" : None, "move_4" : None
			}
		self.stat = {
			"pokemon_nature" : "Serious",
			"pokemon_hp" : 294,
			"pokemon_attack" : 104,
			"pokemon_defense" : 197,
			"pokemon_SpAtk" : 166,
			"pokemon_spDef" : 166,
			"pokemon_speed" : 126,
		}


pokemon1 = Pokemon(1)
pokemon1.level = 45
pokemon2 = Pokemon(2)
pokemon2.shiny = "Yes"
pokemon3 = Pokemon(3)
pokemon4 = Pokemon(4)
pokemon5 = Pokemon(5)
pokemon6 = Pokemon(6)


vars = {
	"UserName" : "user1",
	"TeamName" : "team1",
	"pokemon_1" : pokemon1.__dict__,
	"pokemon_2" : pokemon2.__dict__,
    "pokemon_3" : pokemon3.__dict__,
    "pokemon_4" : pokemon4.__dict__,
    "pokemon_5" : pokemon5.__dict__,
    "pokemon_6" : pokemon6.__dict__
}

to_json = json.dumps(vars)

uploaddb.upload("user1","team1",vars)

print("###################################################")
#print(to_json)

queryData = uploaddb.query("user1","team1")
print(queryData)