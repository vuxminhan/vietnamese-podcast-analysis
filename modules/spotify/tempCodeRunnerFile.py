import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
import dotenv
import pandas as pd
import json



def spotify_auth():
    dotenv.load_dotenv()
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
                                                                    client_secret=os.environ.get('SPOTIFY_CLIENT_SECRET')))
    return spotify

def get_show():
    spotify = spotify_auth()
    show = spotify.show_episodes(show_id='39GCuBVNprJymsZifdwmjg',limit=50,offset=500,market= 'vn')
    
    # with open('show.json', 'w') as f:
    #     json.dump(show, f)
    return show

if __name__ == '__main__':
    get_show()