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
    
def channel_word_cloud():
    df = pd.read_csv(PATH + '/data/vi_youtube_title_translated.csv')
    # df = df.head()
    df['channelTitle'] = df.channelTitle.apply(lambda x: clean_title(x))
    # df.to_csv("output.csv", index=False)
    # Group and join name by year
    df['count'] = 1
    grouped_df = df.groupby(['publishedAt']).agg({'channelTitle': ' '.join, 'count': 'sum'})
    grouped_df.head()
    word_cloud(grouped_df, "channelTitle")

def weighted_channel_wordcloud():
    df = pd.read_csv(PATH + '/data/youtube_channel_stat.csv')
    channel_views_dict = dict(zip(df['channelTitle'], df['viewCount']))
    output_folder = "plot_output/weighted_youtube_channel_name"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(channel_views_dict)
    
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Add title
    ax.set_title("Youtube channel name weighted by total view count", fontdict={"fontsize": 12})

    # Display the word cloud on the axis
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')  # Turn off axis labels and ticks
    image_path = os.path.join(output_folder, "weighted_youtube_channel_name.png")
    # wordcloud.to_file(image_path)
    plt.savefig(image_path, bbox_inches='tight')
    plt.close()

def weighted_channel_wordcloud_average():
    df = pd.read_csv(PATH + '/data/youtube_channel_stat.csv')
    channel_views_dict = dict(zip(df['channelTitle'], df['averageViewCount']))
    output_folder = "plot_output/weighted_youtube_channel_name"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(channel_views_dict)
    
    fig, ax = plt.subplots(figsize=(8, 4))
    
    # Add title
    ax.set_title("Youtube channel name weighted by total view count per video", fontdict={"fontsize": 12})

    # Display the word cloud on the axis
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis('off')  # Turn off axis labels and ticks
    image_path = os.path.join(output_folder, "weighted_youtube_channel_name_average.png")
    # wordcloud.to_file(image_path)
    plt.savefig(image_path, bbox_inches='tight')
    plt.close()

weighted_channel_wordcloud_average()