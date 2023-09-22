import pandas as pd
import os
from dotenv import load_dotenv
import ast
from matplotlib import pyplot as plt
from utils import create_full_country_mapping
load_dotenv()
PATH = (os.environ.get('P'))

#change dir to path 
os.chdir(PATH)
from utils import tokenize_vietnamese, tokenize_text_Np, is_vietnamese, tokenize_english, detect_language, translate_text

file_path = PATH + '/data/spotify - episodes_details - 49055 records.csv'
df = pd.read_csv(file_path)

def episode_name_translated(df):
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

    df.to_csv(PATH + '/data/spotify_name_language_detected.csv', index=False)
    vi_df.to_csv(PATH + '/data/vi_spotify_name_translated.csv', index=False)
    en_df.to_csv(PATH + '/data/en_spotify_name.csv', index=False)

def episode_description_translated(df):
    categorized_df = pd.read_csv(PATH + '/data/spotify_name_language_detected.csv')
    df = df.merge(categorized_df, on='name', suffixes=('', '_y'))
    attributes = ['description', 'release_date', 'channel', 'show_name', 'language']
    df = df[attributes]
    df.release_date = pd.to_datetime(df.release_date)
    df.release_date = df.release_date.dt.year
    vi_df = df[df['language'] == 'vi']
    en_df = df[df['language'] == 'en']

    # Translate Vietnamese to English
    vi_df['description'] = vi_df['description'].apply(translate_text)
    vi_df.to_csv(PATH + '/data/vi_spotify_description_translated.csv', index=False)
    en_df.to_csv(PATH + '/data/en_spotify_description.csv', index=False)


# episode_description_translated(df)



if __name__ == '__main__':
    # episode_description_translated(df)
    categorized_df = pd.read_csv(PATH + '/data/podcast_list - chartable - channel_id_language_distribution.csv')
    # use group by to create a unique list of channel and its language
    grouped_df = categorized_df.groupby('language').size().reset_index(name='count')
       # if the channel has more than 1 language, we will use the language that has the most count and make sure each channel appears only once
    grouped_df = grouped_df.sort_values('count', ascending=False)

    country_code_to_name = {
                'af': 'afrikaans',
                'sq': 'albanian',
                'am': 'amharic',
                'ar': 'arabic',
                'hy': 'armenian',
                'az': 'azerbaijani',
                'eu': 'basque',
                'be': 'belarusian',
                'bn': 'bengali',
                'bs': 'bosnian',
                'bg': 'bulgarian',
                'ca': 'catalan',
                'ceb': 'cebuano',
                'ny': 'chichewa',
                'zh-cn': 'chinese (simplified)',
                'zh-tw': 'chinese (traditional)',
                'co': 'corsican',
                'hr': 'croatian',
                'cs': 'czech',
                'da': 'danish',
                'nl': 'dutch',
                'en': 'english',
                'eo': 'esperanto',
                'et': 'estonian',
                'tl': 'filipino',
                'fi': 'finnish',
                'fr': 'french',
                'fy': 'frisian',
                'gl': 'galician',
                'ka': 'georgian',
                'de': 'german',
                'el': 'greek',
                'gu': 'gujarati',
                'ht': 'haitian creole',
                'ha': 'hausa',
                'haw': 'hawaiian',
                'iw': 'hebrew',
                'he': 'hebrew',
                'hi': 'hindi',
                'hmn': 'hmong',
                'hu': 'hungarian',
                'is': 'icelandic',
                'ig': 'igbo',
                'id': 'indonesian',
                'ga': 'irish',
                'it': 'italian',
                'ja': 'japanese',
                'jw': 'javanese',
                'kn': 'kannada',
                'kk': 'kazakh',
                'km': 'khmer',
                'ko': 'korean',
                'ku': 'kurdish (kurmanji)',
                'ky': 'kyrgyz',
                'lo': 'lao',
                'la': 'latin',
                'lv': 'latvian',
                'lt': 'lithuanian',
                'lb': 'luxembourgish',
                'mk': 'macedonian',
                'mg': 'malagasy',
                'ms': 'malay',
                'ml': 'malayalam',
                'mt': 'maltese',
                'mi': 'maori',
                'mr': 'marathi',
                'mn': 'mongolian',
                'my': 'myanmar (burmese)',
                'ne': 'nepali',
                'no': 'norwegian',
                'or': 'odia',
                'ps': 'pashto',
                'fa': 'persian',
                'pl': 'polish',
                'pt': 'portuguese',
                'pa': 'punjabi',
                'ro': 'romanian',
                'ru': 'russian',
                'sm': 'samoan',
                'gd': 'scots gaelic',
                'sr': 'serbian',
                'st': 'sesotho',
                'sn': 'shona',
                'sd': 'sindhi',
                'si': 'sinhala',
                'sk': 'slovak',
                'sl': 'slovenian',
                'so': 'somali',
                'es': 'spanish',
                'su': 'sundanese',
                'sw': 'swahili',
                'sv': 'swedish',
                'tg': 'tajik',
                'ta': 'tamil',
                'te': 'telugu',
                'th': 'thai',
                'tr': 'turkish',
                'uk': 'ukrainian',
                'ur': 'urdu',
                'ug': 'uyghur',
                'uz': 'uzbek',
                'vi': 'vietnamese',
                'cy': 'welsh',
                'xh': 'xhosa',
                'yi': 'yiddish',
                'yo': 'yoruba',
                'zu': 'zulu'}


    labels = grouped_df['language'].tolist()
    for i in range(len(labels)):
        labels[i] = country_code_to_name[labels[i]]
    sizes = grouped_df['count'].tolist()

    # Create a pie chart
    plt.figure(figsize=(10, 8))
    plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

    # Set the title
    plt.title("Distribution of languages in the channels dataset")

    # Show the pie chart
    plt.savefig('plot_output/channel_language_distribution.png')
