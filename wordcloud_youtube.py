import pandas as pd
import os
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from utils import clean_title
# from underthesea import pos_tag
from dotenv import load_dotenv
import re
from utils import word_cloud, tokenize_english
load_dotenv()
PATH = (os.environ.get('P'))


def name_word_cloud():
    df = pd.read_csv(PATH + '/data/vi_youtube_title_translated.csv')
    # df = df.head()
    df['title'] = df.title.apply(lambda x: clean_title(x))
    df['np_name'] = df.title.apply(lambda x: tokenize_english(x, 'PROPN'))
    df['tokenized_name'] = df.title.apply(lambda x: tokenize_english(x, 'NOUN'))
    # df.to_csv("output.csv", index=False)
    # Group and join name by year
    df['count'] = 1
    grouped_df = df.groupby(['publishedAt']).agg({'tokenized_name': ' '.join, 'np_name': ' '.join, 'count': 'sum'})
    grouped_df.head()
    word_cloud(grouped_df, "tokenized_name")
    word_cloud(grouped_df, "np_name")
    

    
name_word_cloud()