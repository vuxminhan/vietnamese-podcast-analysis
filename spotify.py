import pandas as pd
import os
from dotenv import load_dotenv
import ast
from matplotlib import pyplot as plt
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


# Function to create a full mapping of countries
def create_full_country_mapping(df):
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

    language_count = {}
 
    # Extract unique countries from the 'language' column
    unique_countries = set()
    for codes in df['language']:
        if codes.startswith('[') and codes.endswith(']'):
            codes = ast.literal_eval(codes)
            for code in codes:
                country = country_code_to_name.get(code.lower(), 'Unknown')
                language_count.update({country: language_count.get(country, 0) + 1})
        else:
            country = country_code_to_name.get(codes.lower(), 'Unknown')
            language_count.update({country: language_count.get(country, 0) + 1})


    return language_count

    
# episode_description_translated(df)
categorized_df = pd.read_csv(PATH + '/data/spotify_name_language_detected.csv')
data = create_full_country_mapping(categorized_df)

total_count = sum(data.values())

# Define the threshold for languages below 1%
threshold = total_count * 0.01

# Create a new dictionary to store the combined data
combined_data = {}

# Iterate through the data and combine languages below the threshold
for language, count in data.items():
    if count >= threshold:
        combined_data[language] = count
    else:
        combined_data['Other'] = combined_data.get('Other', 0) + count


labels = combined_data.keys()
sizes = combined_data.values()

# Create a pie chart
plt.figure(figsize=(10, 8))
plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

# Set the title
plt.title("Distribution of Country Names")

# Show the pie chart
plt.savefig('plot_output/language_distribution.png')
