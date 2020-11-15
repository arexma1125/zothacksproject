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
import urllib
from oauthlib.oauth2 import BackendApplicationClient
from requests.auth import HTTPBasicAuth
from requests_oauthlib import OAuth2Session

BASIC_URL = "https://accounts.spotify.com/api/token/"
SEARCH_URL = 'https://api.spotify.com/v1/search/?'
FEATURES_URL = 'https://api.spotify.com/v1/audio-features/'
client_id = "feb48f6bfe094749afc4f4c8af0d4c74"
client_secret = "140e93df2ab643b8a3ac6b8567c2696f"

client = BackendApplicationClient(client_id=client_id)
oauth = OAuth2Session(client=client)
token = oauth.fetch_token(token_url=BASIC_URL, client_id=client_id, client_secret=client_secret)

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

"""
def url_search_builder(name):
    query_parameters = [('q', 'f{name}')]
    encode_parameter = urllib.parse.urlencode(query_parameters)
    return f'{SEARCH_URL}&{encode_parameter}'
"""



def download_data(url):
    head = {"Authorization": "Bearer {}".format(token["access_token"])}
    response = requests.get(url, headers=head)
    try:
        json_text = response.json()
        return json_text
    except:
        raise



def spotify_id_request(name, track, limit):
    get_request_url = {"q": name, "type": track, "limit": limit}
    get_request_url_formatted = SEARCH_URL + urllib.parse.urlencode(get_request_url)
    song_list = download_data(get_request_url_formatted)
    songs = []
    for item in song_list["tracks"]["items"]:
        artist_name = item["album"]["artists"][0]["name"]
        song_name = item["name"]
        song_id = item["id"]
        songs.append((artist_name, song_name, song_id))
    return songs

def spotify_song_features(song_id):
    song_info = download_data(FEATURES_URL + song_id)
    song_tempo = song_info["tempo"]
    song_time_signature = song_info["time_signature"]
    return song_tempo, song_time_signature




# name, id, artists (name), 

if __name__ == "__main__":
    #app.run(debug=True, port=8080)
    print(spotify_id_request("athousandyears", "track", "5"))
    print(spotify_song_features("6lanRgr6wXibZr8KgzXxBl"))
    
#url_search_builder('heartless')