import os
import util
# import db
from flask import Flask, json
from flask_cors import CORS
# from flask_restful import Api
# from resources.user import User
from dotenv import load_dotenv
import urllib.parse
import json 
import requests

SEARCH_URL = 'https://api.spotify.com/v1/search'
FEATURES_URL = 'https://api.spotify.com/v1/audio-features'


# Load Environment variables
load_dotenv()

app = Flask(__name__)
# Allow cross domain apps to access API
CORS(app)




# Provide Mongo Atlas URI, stored in config file
# app.config["MONGO_URI"] = os.getenv("MONGO_URI_MASTER")
# Set custom JSON Encoder for Mongo Object
# app.json_encoder = util.MongoEncoder
# db.mongo.init_app(app)
# api = Api(app)

# api.add_resource(User, "/user")

if __name__ == "__main__":
    app.run(debug=True, port=8080)


# Vanilla Flask route
@app.route("/", methods=["GET"])
def index():
    return "Welcome to my ZotHacks 2020 project!"


# Handles validation errors and returns JSON Object
@app.errorhandler(422)
@app.errorhandler(400)
def handle_error(err):
    messages = err.data.get("messages", ["Invalid request."])
    #return json.jsonify({"errors": messages}, err.code)

def url_search_builder(name):
    query_parameters = [('q', 'f{name}')]
    encode_parameter = urllib.parse.urlencode(query_parameters)
    return f'{SEARCH_URL}&{encode_parameter}'

def download_data(url):
    response = requests.get(url)
    try:
        json_text = response.json()
        return json_text
    except:
        raise
        

def spotify_id_request(name):
    url = url_search_builder(name)
    song_details = download_data(url)


#url_search_builder('heartless')