import json
from flask_lambda import FlaskLambda
from app import app

lambda_app = FlaskLambda(app)

def handler(event, context):
    return lambda_app(event, context)
