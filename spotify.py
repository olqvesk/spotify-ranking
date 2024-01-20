import json
import requests
import sys
from pymongo import MongoClient
import certifi
from datetime import datetime

with open('config.json', 'r') as f:
    config = json.load(f)

mongo_srv = config["MONGO_SRV"]

ca = certifi.where()
client = MongoClient(mongo_srv, tlsCAFile=ca)
db = client.rgorithm

sys.stdout.reconfigure(encoding='utf-8')

url = "https://api.spotify.com/v1/playlists/37i9dQZEVXbNG2KDcFcKOF"

headers = {
    "Authorization": config["SPOTIFY_AUTH"]
}

response = requests.get(url, headers=headers)

json_result = response.json()


song_infos = []
for i in range(50):

    date = datetime.now().strftime("%m/%d/%Y, %H:%M:%S")
    artist = json_result["tracks"]["items"][i]["track"]['album']['artists'][0]['name']
    title = json_result["tracks"]["items"][i]["track"]['name']
    album = json_result["tracks"]["items"][i]["track"]['album']['name']
    images = json_result["tracks"]["items"][i]["track"]['album']['images']
    song_info = {'rank': i + 1, 'date': date, 'artist': artist, 'title': title, 'album': album, 'images': images}
    db.songs.insert_one(song_info)
    song_infos.append(song_info)
