import boto3
import re
from boto3.dynamodb.conditions import Key, Attr
import json
from json2html import *

dynamodb = boto3.resource('dynamodb', aws_access_key_id='AKIASYAKXZPN5RCSUKMG', aws_secret_access_key='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', region_name='us-west-2')
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
		print("PutItem succeeded:")
		print(json.dumps(response2, indent=4, cls=DecimalEncoder))
		
		
def query(UserName, TeamName):
	response = table.scan(FilterExpression=Attr('UserName').contains(UserName) & Attr('TeamName').contains(TeamName))
	return (response['Items'])
