import pandas as pd
import os
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

load_dotenv()
PATH = os.environ.get('P')

# Change dir to path
os.chdir(PATH)
from utils import detect_language

file_path = PATH + '/modules/spotify/spotify - episodes_details - 49055 records.csv'
df = pd.read_csv(file_path)

attributes = ['name', 'release_date', 'channel', 'show_name']
df = df[attributes]

df.release_date = pd.to_datetime(df.release_date)
df.release_date = df.release_date.dt.year

# Function to detect language in parallel
def detect_language_parallel(text):
    return detect_language(text)

# Multithreading for language detection
with ThreadPoolExecutor() as executor:
    df['language'] = list(executor.map(detect_language_parallel, df['name']))

df.to_csv(PATH + '/modules/spotify/spotify_name_language_detected.csv', index=False)
