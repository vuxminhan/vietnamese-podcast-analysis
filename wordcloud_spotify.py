import pandas as pd
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from underthesea import pos_tag
from dotenv import load_dotenv
import re
from utils import word_cloud, tokenize_english
load_dotenv()
PATH = (os.environ.get('P'))

def extract_main_spotify_title(podcast_title):
    # Define a list of common patterns in Spotify podcast titles
    patterns = [
        r'\bEpisode \d+\b',  # Matches "Episode 123"
        r'S+\d+E\d+\b',     # Matches "S2E3" (Season 2, Episode 3)
        r'\bPart \d+\b',     # Matches "Part 2"
        r'\bS+\d+[ES]\d+\b',    # Matches "SS3E13" (Season SS3, Episode 13)
        r'^\d+|\d+$',        # Matches "123" or "123-456"
        r'\bTranscript\b',   # Matches "Transcript"
        r'Phần .+ Chương \d+', # Matches "Phần 1 Chương 1"
        r'Tập \d+', # Matches "Tập 1"
        r'Phần \d+', # Matches "Phần 1"
        r'Chương \d+', # Matches "Chương 1"
        r'Chương \d+ Phần \d+', # Matches "Chương 1 Phần 1"
        r'Mùa \d+', # Matches "Mùa 1"
        r'AEE \d*', # Matches "AEE 1"
        r'(?i)ep\s?\d+', # Matches "Ep 1"
    ]

    # Check for common patterns and remove them
    for pattern in patterns:
        podcast_title = re.sub(pattern, ' ', podcast_title)
    
    # Remove punctuation and standardize spacing
    podcast_title = re.sub(r'[^\w\s]', '', podcast_title)
    podcast_title = re.sub(r'\s+', ' ', podcast_title)

    # Remove trailing whitespace and return the cleaned title
    return podcast_title.strip()

df = pd.read_csv(PATH + '/modules/spotify/vi_spotify_name_translated.csv')
# df = df.head()
df['name'] = df.name.apply(lambda x: extract_main_spotify_title(x))
# df['np_name'] = df.name.apply(lambda x: tokenize_text_Np(x))
df['tokenized_name'] = df.name.apply(lambda x: tokenize_english(x, 'NOUN'))
# print(df)
word_cloud(df, 'tokenized_name')
df['tokenized_P_name'] = df.name.apply(lambda x: tokenize_english(x, 'PROPN'))
# print(df)
word_cloud(df, 'tokenized_P_name')
