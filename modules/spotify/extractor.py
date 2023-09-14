import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os
from dotenv import load_dotenv
import pandas as pd
import json


def spotify_auth():
    load_dotenv()
    spotify = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=os.environ.get('SPOTIFY_CLIENT_ID'),
                                                                    client_secret=os.environ.get(
                                                                        'SPOTIFY_CLIENT_SECRET')))
    return spotify


def get_show_ep_details(show_id, youtube, chartable):
    spotify = spotify_auth()
    all_episodes = []
    offset = 0
    total_ep = 0
    data = spotify.show_episodes(show_id=show_id, limit=50, offset=offset, market='vn')
    if 'items' in data and len(data.get("items")) > 0:
        episodes = data.get("items")
        total_ep = data.get('total')
        for episode in episodes:
            res = {
                'show': chartable,
                'episode_id': episode.get('id'),
                'name': episode.get('name'),
                'duration_ms': episode.get('duration_ms'),
                'release_date': episode.get('release_date'),
                'language': episode.get('language'),
                'description': episode.get('description'),
                'spotify': show_id,
                'youtube': youtube
            }
            all_episodes.append(res)
    while len(all_episodes) < int(total_ep):
        offset += 50
        data = spotify.show_episodes(show_id=show_id, limit=50, offset=offset, market='vn')
        if 'items' in data and len(data.get("items")) > 0:
            episodes = data.get("items")
            for episode in episodes:
                res = {
                    'show': chartable,
                    'episode_id': episode.get('id'),
                    'name': episode.get('name'),
                    'duration_ms': episode.get('duration_ms'),
                    'release_date': episode.get('release_date'),
                    'description': episode.get('description'),
                    'language': episode.get('language'),
                    'spotify': show_id,
                    'youtube': youtube
                }
                all_episodes.append(res)
        else:
            break

    return all_episodes



if __name__ == '__main__':
    load_dotenv()
    PATH = os.environ.get('P')
    
    df = pd.read_csv(PATH + "/data/podcast_list - chartable.csv")
    res = []
    for index, row in df.iterrows():
        show = row['spotify']
        youtube = row['youtube']
        chartable = row['chartable']
        if show:
            try:
                episodes = get_show_ep_details(show, youtube, chartable)
                res.extend(episodes)
            except Exception as e:
                print(e)
                continue
    df_ep = pd.DataFrame(res)
    df_ep[['channel', 'show_name']] = df_ep['show'].str.split('\n', expand=True)
    
    # Drop the original 'chartable' column as it's no longer needed
    df_ep.drop('show', axis=1, inplace=True)
    df_ep.to_csv(PATH + "/data/spotify episodes_details_language_added.csv", index=False)
