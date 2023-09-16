import pandas as pd
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from utils import extract_main_spotify_title
# from underthesea import pos_tag
from dotenv import load_dotenv
import re
from utils import word_cloud, tokenize_english
load_dotenv()
PATH = (os.environ.get('P'))


def name_word_cloud():
    df = pd.read_csv(PATH + '/data/vi_spotify_name_translated.csv')
    # df = df.head()
    df['name'] = df.name.apply(lambda x: extract_main_spotify_title(x))
    df['np_name'] = df.name.apply(lambda x: tokenize_english(x, 'PROPN'))
    df['tokenized_name'] = df.name.apply(lambda x: tokenize_english(x, 'NOUN'))
    # df.to_csv("output.csv", index=False)
    # Group and join name by year
    df['count'] = 1
    grouped_df = df.groupby(['release_date']).agg({'tokenized_name': ' '.join, 'np_name': ' '.join, 'count': 'sum'})

    word_cloud(grouped_df, "tokenized_name")
    word_cloud(grouped_df, "np_name")
    
def description_word_cloud():
    df = pd.read_csv(PATH + '/data/vi_spotify_description_translated.csv')
    # df = df.head()
    df['description'] = df.description.apply(lambda x: extract_main_spotify_title(x))
    df['np_name'] = df.description.apply(lambda x: tokenize_english(x, 'PROPN'))
    df['tokenized_name'] = df.description.apply(lambda x: tokenize_english(x, 'NOUN'))
    # print(df)
    df.to_csv("output.csv", index=False)
    # Group and join name by year
    df['count'] = 1
    grouped_df = df.groupby(['release_date']).agg({'tokenized_name': ' '.join, 'np_name': ' '.join, 'count': 'sum'})

    word_cloud(grouped_df, "tokenized_name")
    word_cloud(grouped_df, "np_name")
    
description_word_cloud()