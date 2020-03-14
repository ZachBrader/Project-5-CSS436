import os
import boto3
basedir = os.path.abspath(os.path.dirname(__file__))


# ------------------------------------------------------
# AWS Variables
# ------------------------------------------------------
try:
    AWS_ACCESS_KEY = os.environ['AWS_ACCESS_KEY']
    AWS_SECRET_KEY = os.environ['AWS_SECRET_KEY']
    AWS_REGION = 'us-west-2'
except Exception as e:
    AWS_ACCESS_KEY = ""
    AWS_SECRET_KEY = ""
    AWS_REGION = 'us-west-2'
    print("Error finding keys", e)
# You can set this if you want to access a different table ON YOUR AWS ACCOUNT. If not, leave it be
TABLE_NAME = os.environ.get('TABLE_NAME') or 'PokemonDB'

# Table must be set up before starting application
DYNAMODB = boto3.resource('dynamodb', aws_access_key_id=AWS_ACCESS_KEY, aws_secret_access_key=AWS_SECRET_KEY,
                          region_name=AWS_REGION)
TABLE = DYNAMODB.Table(TABLE_NAME)


class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    TEAMS_PER_PAGE = 2
