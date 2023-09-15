import pandas as pd
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from underthesea import pos_tag
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
df = df.head(20)
df['language'] = df['name'].apply(detect_language)
vi_df = df[df['language'] == 'vi']
en_df = df[df['language'] == 'en']

# Translate Vietnamese to English
vi_df['name'] = vi_df['name'].apply(translate_text)

print(df)
print(vi_df)
print(en_df)    
