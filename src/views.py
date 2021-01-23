from app import app
from flask import render_template, request, session, redirect
import spotipy
from src.config import *
from spotipy.oauth2 import SpotifyOAuth
import requests
import base64
import json
from datetime import timedelta

SAVED_ID = '4ijw7vShIIarBXHrmslNbe'
DAILY_MIX_ID = '37i9dQZF1E38bNvW8cIxrb'
USERNAME = 'svirl3jiigsae2f476alnlfgm'
global spotify_auth

class spotify_authorization():
    def __init__(self, access_token = None, refresh_token = None):
        self.access_token = access_token
        self.refresh_token = refresh_token
    
    def authorize(self, code):
        base64encoded = base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode())
        data = {
            'grant_type':'authorization_code',
            'code':str(code),
            'redirect_uri':REDIRECT_URI
        }
        headers = {
            'Authorization':"Basic {}".format(base64encoded.decode())
        }
        response =  requests.post('https://accounts.spotify.com/api/token', data=data,
                                                                headers=headers)
        if response.status_code != 200:
            return json.dumps({'error': response.reason}), response.status_code
        else:
            response = response.json()
            self.access_token = response['access_token']
            self.refresh_token = response['refresh_token']
            return json.dumps({'success':'recieved access token', 'response': response}), 200

@app.before_request
def make_session_permanent():
    app.secret_key = APP_SECRET_KEY
    session.permanent = True
    app.permanent_session_lifetime = timedelta(days=30)
    spotify_auth = spotify_authorization()

@app.route('/signin')
def home():
    scope = ['playlist-read-private', 'playlist-modify-public']
    return redirect(SpotifyOAuth(scope=scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI, username=USERNAME).get_authorize_url())

@app.route('/callback/')
def success():
    global spotify_auth
    code = request.args.get('code')
    return spotify_auth.authorize(code)
    
  


