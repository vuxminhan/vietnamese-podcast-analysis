import pandas as pd
import os
from dotenv import load_dotenv
load_dotenv()
PATH = (os.environ.get('P'))

#change dir to path 
os.chdir(PATH)
from utils import tokenize_vietnamese, tokenize_text_Np, is_vietnamese, tokenize_english, detect_language, translate_text

file_path = PATH + '/modules/spotify/spotify - episodes_details - 49055 records.csv'
df = pd.read_csv(file_path)

attributes = ['name', 'release_date', 'channel', 'show_name']
df = df[attributes]

df.release_date = pd.to_datetime(df.release_date)
df.release_date = df.release_date.dt.year
# df = df.head(20)
df['language'] = df['name'].apply(detect_language)

vi_df = df[df['language'] == 'vi']
en_df = df[df['language'] == 'en']

# Translate Vietnamese to English
vi_df['name'] = vi_df['name'].apply(translate_text)

# # Create summary df to save distribution of all languages in the dataset
# summary_df = pd.DataFrame(columns=['language', 'count'])
# summary_df['language'] = df['language'].unique()
# summary_df['count'] = [len(df[df['language'] == lang]) for lang in summary_df['language']]
# summary_df.to_csv(PATH + '/modules/spotify/summary.csv', index=False)

df.to_csv(PATH + '/modules/spotify/spotify_name_translated.csv', index=False)
vi_df.to_csv(PATH + '/modules/spotify/vi_spotify_name_translated.csv', index=False)
en_df.to_csv(PATH + '/modules/spotify/en_spotify_name.csv', index=False)


