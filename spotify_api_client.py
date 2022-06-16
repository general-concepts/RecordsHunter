# std
import os
from os import environ as env

import sys
import logging
import json

# 3rd party
from dotenv import load_dotenv

import spotipy
from spotipy.oauth2 import SpotifyOAuth

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

formatter = logging.Formatter('%(asctime)s:%(name)s:%(levelname)s:%(message)s')

stream_handler = logging.StreamHandler(sys.stdout)
stream_handler.setLevel(logging.INFO)
stream_handler.setFormatter(formatter)

logger.addHandler(stream_handler)

file_handler = logging.FileHandler('api.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(formatter)

logger.addHandler(file_handler)

project = os.getcwd()
dirname = ''
filename = '.env'


def get_path(project: str, dirname: str, filename: str) -> str:
    return os.path.join(project, dirname, filename)


print(get_path(project, dirname, filename))
load_dotenv(get_path(project, dirname, filename))


if __name__ == '__main__':
    # Base authentication credentials
    CLIENT_ID = env['CLIENT_ID']
    CLIENT_SECRET = env['CLIENT_SECRET']
    REDIRECT_URI = env['REDIRECT_URI']
    SCOPE = env['SCOPE']

    spotify = spotipy.Spotify(auth_manager=SpotifyOAuth(
        client_id=CLIENT_ID,
        client_secret=CLIENT_SECRET,
        redirect_uri=REDIRECT_URI,
        scope=SCOPE,
        username='DUMMY_USER4'
    ))

    results = spotify.current_user_saved_tracks()
    tracks = []

    for idx, item in enumerate(results['items']):
        track_info = {}
        track = item['track']
        track_info['name'] = track['name']
        track_info['artist'] = track['artists'][0]['name']
        tracks.append(track_info)

    user = spotify.me()
    logger.info(tracks)

    with open('tracks.json', 'w') as tracks_file:
        json_obj = json.dumps(tracks)
        tracks_file.write(json_obj)