from app import app
from flask import render_template, request, session, redirect
import spotipy
from src.config import *
from spotipy.oauth2 import SpotifyOAuth
import requests
import base64
import json
from datetime import timedelta

class spotify_authorization():
    def __init__(self, access_token = None, refresh_token = None):
        self.access_token = access_token
        self.refresh_token = refresh_token
    
    def key_headers(self):
        base64encoded = base64.b64encode(("{}:{}".format(CLIENT_ID, CLIENT_SECRET)).encode())
        return {
            'Authorization':"Basic {}".format(base64encoded.decode())
        }
    
    def access_token_headers(self):
        return {
            'Authorization':"Bearer {}".format(self.access_token)
        }
    
    def authorize(self, code):
        data = {
            'grant_type':'authorization_code',
            'code':str(code),
            'redirect_uri':REDIRECT_URI
        }
        response = requests.post('https://accounts.spotify.com/api/token', data=data,
                                                                headers=self.key_headers())
        if response.status_code != 200:
            return json.dumps({'error': response.reason}), response.status_code
        else:
            response = response.json()
            self.access_token = response['access_token']
            self.refresh_token = response['refresh_token']
            return json.dumps({'success':'recieved access token', 'response': response}), 200

    def renew_access_token(self):
        data = {
            'grant_type':'refresh_token',
            'refresh_token':self.refresh_token
        }
        response = requests.post('https://accounts.spotify.com/api/token', data=data,
                                                                headers=self.key_headers())
        if response.status_code != 200:
            return json.dumps({'error': response.reason}), response.status_code
        else:
            response = response.json()
            self.access_token = response['access_token']
            return json.dumps({'success':'recieved access token', 'response': response}), 200
