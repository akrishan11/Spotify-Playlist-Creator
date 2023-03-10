import requests
import json
import spotipy.util as util
from dotenv import load_dotenv
import os
import base64
from requests import post, get

load_dotenv()

client_id = os.getenv("CLIENT_ID")
client_secret = os.getenv("CLIENT_SECRET")
scope = 'playlist-modify-private'
user_id = "31mndkzbwdvymh3nptcnff7bmol4"
redirect_uri = "http://localhost:8888/callback"


auth_token = util.prompt_for_user_token(user_id, scope, client_id=client_id, client_secret=client_secret, redirect_uri=redirect_uri)



def get_token():
    auth_string = client_id + ":" + client_secret
    auth_bytes = auth_string.encode("utf-8")
    auth_base64 = str(base64.b64encode(auth_bytes), "utf-8")

    url = "https://accounts.spotify.com/api/token"
    headers = {
        "Authorization": "Basic " + auth_base64,
        "Content-Type": "application/x-www-form-urlencoded"
    }
    data = {"grant_type": "client_credentials"}
    result = post(url, headers=headers, data=data)
    json_result = json.loads(result.content)
    token = json_result["access_token"]
    return token


token = get_token()


def get_auth_header(token):
    return {"Authorization": "Bearer " + token}


def create_playlist_on_spotify(name, public):
    url = f'https://api.spotify.com/v1/users/{user_id}/playlists'
    headers = {"Authorization": f"Bearer {auth_token}"}
    data = {"name": name, "public": public}
    response = requests.post(url, headers=headers, json=data)

    json_resp = response.json()
    return json_resp



playlist_name= input("Playlist name: ")

playlist = create_playlist_on_spotify(playlist_name, False)

playlist_id = playlist['id']


def search_for_artist(token, artist_name):
    url = "https://api.spotify.com/v1/search"
    headers = get_auth_header(token)
    query = f"?q={artist_name}&type=artist&limit=1"

    query_url = url + query
    result = get(query_url, headers=headers)
    json_result = json.loads(result.content)["artists"]["items"]
    if len(json_result) == 0:
        print("No artist with this name exists...")
        return None
    return json_result[0]


def get_songs_by_artist(token, artist_id):
    url = f"https://api.spotify.com/v1/artists/{artist_id}/top-tracks?country=US"
    headers = get_auth_header(token)
    result = get(url, headers=headers)
    json_result = json.loads(result.content)["tracks"]
    return json_result


def add_songs_to_playlist():
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks'
    headers = {"Authorization": "Bearer " + auth_token, 'Content-Type': 'application/json'}
    uris = song_uris
    json = {"uris": uris, "position": 0}
    result = post(url, headers=headers, json=json)
    json_result = result.json()
    return json_result

x = True
while True:
    artist_name = input('Select an artist(Enter "done" when complete):\n')
    if artist_name == 'done':
        False
        break
    result = search_for_artist(token, artist_name)
    artist_id = result["id"]
    songs = get_songs_by_artist(token, artist_id)
    song_uris = []
    for idx, song in enumerate(songs):
        song_uris.append(song['uri'])
    add_songs_to_playlist()
