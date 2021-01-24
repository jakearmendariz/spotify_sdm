from app import app
from flask import render_template, request, session, redirect
import spotipy
from src.config import *
from spotipy.oauth2 import SpotifyOAuth
import requests
import base64
import json
from datetime import timedelta
from src.auth import spotify_authorization

SAVED_ID = '4ijw7vShIIarBXHrmslNbe'
DAILY_MIX = '37i9dQZF1E38bNvW8cIxrb'
USERNAME = 'svirl3jiigsae2f476alnlfgm'
SCOPE = 'playlist-read-private playlist-modify-public playlist-read-collaborative playlist-modify-private'

DANNY = 'sewcb0rqq10yisy7c4e8v3ajh'
DANNY_DAILY = '37i9dQZF1E39FDiPemdR4F'
DANNY_SAVE = '3d07iaqjCWRfxw5tSHGyZm'

global spotify

@app.before_request
def make_session_permanent():
    app.secret_key = APP_SECRET_KEY
    global spotify
    spotify = spotify_authorization()

@app.route('/signin')
def home():
    scope = SCOPE
    return redirect(SpotifyOAuth(scope=scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, 
        redirect_uri=REDIRECT_URI, username=USERNAME).get_authorize_url())

@app.route('/callback/')
def success():
    code = request.args.get('code')
    response = spotify.authorize(code)
    download_daily_mix()
    if response[1] != 200:
        return json.dumps({'error': response.reason}), response.status_code
    else:
        return json.dumps({'success':f'login to user{USERNAME}'})
    

@app.route('/read_daily/')
def download_daily_mix():
    print('headers', spotify.access_token_headers())
    response = requests.get(f'https://api.spotify.com/v1/playlists/{DAILY_MIX}/tracks', 
        headers = spotify.access_token_headers())
    if response.status_code != 200:
        return json.dumps({'error': response.reason}), response.status_code
    else:
        response = response.json()
    uris = []
    for item in response['items']:
        uris.append('spotify:track:' + str(item['track']['id']))
    res = requests.post(f'https://api.spotify.com/v1/playlists/{SAVED_ID}/tracks', 
        json = {'uris':uris},
        headers = spotify.access_token_headers())
    if res.status_code != 201:
        return json.dumps({'error adding songs': res.reason}), res.status_code
    else:
        return json.dumps({'success':'read daily mix', 'response': res}, indent=2), 200
