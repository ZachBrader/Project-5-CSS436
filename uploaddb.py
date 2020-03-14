import boto3
import re
from boto3.dynamodb.conditions import Key, Attr
import json
from json2html import *
import decimal

dynamodb = boto3.resource('dynamodb', aws_access_key_id= TOM_AWS_ACCESS_KEY_ID, aws_secret_access_key= TOM_AWS_SECRET_ACCESS_KEY, region_name='us-west-2')
table = dynamodb.Table('PokemonDB')

# Helper class to convert a DynamoDB item to JSON.
class DecimalEncoder(json.JSONEncoder):
    def default(self, o):
        if isinstance(o, decimal.Decimal):
            if abs(o) % 1 > 0:
                return float(o)
            else:
                return int(o)
        return super(DecimalEncoder, self).default(o)
		

def upload(UserName, TeamName, vars):
	#response = table.scan(FilterExpression=Attr('UserName').contains(UserName) & Attr('TeamName').contains(TeamName)))
	#if(response['Count']==1):
	#	a = "b"
	#else:	
		response2 = table.put_item(Item=vars)
        #Check if item put success
		#print("PutItem succeeded:")
		#print(json.dumps(response2, indent=4, cls=DecimalEncoder))
        #return (json.dumps(response2, cls=DecimalEncoder))
		
		
def query(UserName, TeamName):
	response = table.scan(FilterExpression=Attr('UserName').contains(UserName) & Attr('TeamName').contains(TeamName))
	return (json.dumps(response['Items'], cls=DecimalEncoder))

##################################################################################################
import requests

def GetImage(pokemon_id):
    if isinstance(pokemon_id, int):
        return FindByID(pokemon_id)
    else:
        attempt_url = 'https://pokeapi.co/api/v2/pokemon/' + str(pokemon_id).lower() + '/'
        response = requests.get(attempt_url)
        if response.ok:
            print('Pokemon found! ' + attempt_url)
            obj = json.loads(response.content)
            print(obj['id'])
            return FindByID(obj['id'])
        else:
            print('Pokemon not found')

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


