from app import app
from flask import render_template, request, session, redirect
import spotipy
from src.config import *
from spotipy.oauth2 import SpotifyOAuth
import requests
import base64
import json
# from time import timedelta

SAVED_ID = '4ijw7vShIIarBXHrmslNbe'
DAILY_MIX_ID = '37i9dQZF1E38bNvW8cIxrb'

# @app.before_request
# def make_session_permanent():
#     app.secret_key = '4asdf644'
#     session.permanent = True
    # app.permanent_session_lifetime = timedelta(days=30)
USERNAME = 'svirl3jiigsae2f476alnlfgm'
@app.route('/')
def home():
    scope = "playlist-read-private"
    return redirect(SpotifyOAuth(scope=scope, client_id=CLIENT_ID, client_secret=CLIENT_SECRET, redirect_uri=REDIRECT_URI).get_authorize_url())
    # print(auth.get_authorize_url())
    # # print('sp', sp)
    # # daily_mix_playlist = sp.playlist(DAILY_MIX_ID)
    # # print('daily mix playlist', daily_mix_playlist)
    # return render_template('index.html')

@app.route('/callback/')
def success():
    code = request.args.get('code')
    print(code)
    # access_token = SpotifyOAuth.get_access_token(code)
    
    # headers = {"Authorization": "Basic {}".format(base64encoded.decode())}
    response = authorize(code)
    
    if response.status_code != 200:
        return json.dumps({'error': response.reason}), response.status_code
    else:
        response = response.json()
        print(response)
        return json.dumps({'success':'recieved access token', 'response': response}), 200

def authorize(code):
    base64encoded = base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode())
    data = {
        'grant_type':'authorization_code',
        'code':str(code),
        'redirect_uri':REDIRECT_URI
    }
    headers = {
        'Authorization':"Basic {}".format(base64encoded.decode())
    }
    return requests.post('https://accounts.spotify.com/api/token', data=data,
                                                                headers=headers)
