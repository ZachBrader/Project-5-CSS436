from app import app
from app import app, db
from app.models import User, Post
import uploaddb
import json

@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Post': Post}

###########################################
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
pokemon2 = Pokemon(2)


vars = {
	"UserName" : "user1",
	"TeamName" : "team1",
	"pokemon_1" : pokemon1.__dict__,
	"pokemon_2" : pokemon2.__dict__
}

to_json = json.dumps(vars)

uploaddb.upload("user1","team1",vars)

print("###################################################")
#print(to_json)

queryData = uploaddb.query("user1","team1")
print(queryData)
		

###########################################
if __name__ == '__main__':
    app.run()