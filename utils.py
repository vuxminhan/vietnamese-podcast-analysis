import regex as re
import numpy as np
import pandas as pd
from underthesea import pos_tag
import os
from dotenv import load_dotenv
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import ast
# from collections import Counter
# from unidecode import unidecode
import sys
from googletrans import Translator
import spacy
import ast
nlp = spacy.load('en_core_web_lg')
# Load the English language model
font_path = "/usr/share/fonts/truetype/liberation/LiberationMono-BoldItalic.ttf"
load_dotenv()
PATH = (os.environ.get('P'))
with open(PATH + '/data/vietnamese-stopwords-dash.txt', 'r', encoding='utf-8') as f:
    vietnamese_stopwords = list(f.read().splitlines())

vietnamese_stopwords.extend(['best', 'cut', 'tập', 'podcast', "episode", "short", "shorts", "ep","aee","sách", "night", "extra"])


def standardize_whitespace(input_string, replacement=' '):
    # Replace consecutive spaces with a single space
    standardized_string = re.sub(r'\s+', replacement, input_string)

    return standardized_string

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
        r'Cấy nền',
        r'\b[l|-]\b',
        r'\bshorts\b'
        
    ]

    # Check for common patterns and remove them
    for pattern in patterns:
        podcast_title = re.sub(pattern, ' ', podcast_title)
    
    # Remove punctuation and standardize spacing
    podcast_title = re.sub(r'[^\w\s]', '', podcast_title)
    podcast_title = re.sub(r'\s+', ' ', podcast_title)

    # Remove trailing whitespace and return the cleaned title
    return podcast_title.strip()

# Remove special characters in Vietnamese sentences
def replace_special_characters(input_text):
    # Define a regular expression pattern to match special characters (excluding Vietnamese characters and spaces)
    pattern = r'[^a-zA-Z0-9À-Ỹà-ỹĂăÂâĐđÊêÔôƠơƯư\s]+'

    # Use re.sub to replace matched special characters with an empty string
    cleaned_text = re.sub(pattern, ' ', input_text).strip()
    cleaned_text = standardize_whitespace(cleaned_text)

    return cleaned_text


def process_tags(input_str):
    try:
        # Convert the string to a list
        tags_list = ast.literal_eval(input_str)

        # Process the list to replace spaces with underscores and join elements
        result_str = ' '.join([word.replace(' ', '_').lower() for word in tags_list])

        return result_str
    except:
        # Return missing value for NaN tags
        return ' '

def remove_hashtag(input_string):
    if '#' in input_string:
        return input_string.split('#')[0]
    else:
        return input_string
    
def process_title(input_string):
    if '|' in input_string:
        output_string = ''.join(input_string.split('|')[:-1])
        return remove_hashtag(output_string)
    else:
        return remove_hashtag(input_string)


# Choose words that are nouns, proper nouns, borrowed words, 
# abbreviated nouns, abbreviated borrowed nouns, and foreign words
def tokenize_vietnamese(input_string, word_type=None):
    if word_type is None:
        word_type = ['N', 'Nb', 'Ny', 'Nby', 'FW']
    # vietnamese_stopwords = []

    try:
        input_string = replace_special_characters(input_string)
        words = pos_tag(input_string, format="text")
        words = [word[0] for word in words if word[0].lower() not in vietnamese_stopwords and word[1] in word_type]
        return process_tags(str(words)) + ' '
    except:
        return ' '
    
def tokenize_text_Np(input_string, word_type=None):
    if word_type is None:
        word_type = ['Np']
    # vietnamese_stopwords = []

    try:
        input_string = replace_special_characters(input_string)
        words = pos_tag(input_string, format="text")
        words = [word[0] for word in words if word[0].lower() not in vietnamese_stopwords and word[1] in word_type]
        return process_tags(str(words)) + ' '
    except:
        return ' '

def detect_language(sentence):
    try:
        return Translator().detect(sentence).lang
    except Exception as e:
        print(e)
        return 'Unknown'

def translate_text(sentence, dest='en'):
    print("translated")
    return Translator().translate(sentence, dest=dest).text
    
def is_vietnamese(sentence):
    transliterated_sentence = sentence

    # Define a set of Vietnamese diacritics characters
    vietnamese_diacritics = set("áàạãảòóõọỏẽéẹèẻĩịíỉìăắằẳẵặâấầẩẫậđêếềểễệôốồổỗộơớờởỡợùúủũụưứừửữựỳỹỷý")

    # Check if the transliterated sentence contains any Vietnamese diacritics characters
    return any(char in vietnamese_diacritics for char in transliterated_sentence)



def pos_tag_english_sentence(sentence):
    # Process the sentence using spaCy
    doc = nlp(sentence)
    
    # Extract tokens and their POS tags
    tagged_words = [(token.text, token.pos_) for token in doc]

    return tagged_words

def tokenize_english(input_string, word_type=None):
    if word_type is None:
        word_type = ['NOUN', 'PROPN']
    # vietnamese_stopwords = []

    try:
        input_string = replace_special_characters(input_string)
        words = pos_tag_english_sentence(input_string)
        words = [word[0] for word in words if word[1] in word_type]
        return process_tags(str(words)) + ' '
    except Exception as e:
        print(e)
        return ' '


def word_cloud(df, column):
    wordclouds = {}

    # Create the output folder if it doesn't exist
    output_folder = "plot_output/spotify_channel_name"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through each year and extract the top words for each year
    for year in df.index:
        text = df.loc[year, column]
        try:
            wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
            wordclouds[year] = wordcloud
            # Add legends and title to saved image
            # Save the word cloud as an image
                        # Create a figure and axis for the word cloud
            fig, ax = plt.subplots(figsize=(8, 4))
            
            # Add title
            ax.set_title(f"Year = {year}, n = {df.loc[year, 'count']}", fontdict={"fontsize": 12})

            # Display the word cloud on the axis
            ax.imshow(wordcloud, interpolation='bilinear')
            ax.axis('off')  # Turn off axis labels and ticks
            image_path = os.path.join(output_folder, f"vi_spotify_channel_title{column}_{year}.png")
            # wordcloud.to_file(image_path)
            plt.savefig(image_path, bbox_inches='tight')
            plt.close()
            
        except Exception as e:
            print(e)

def clean_title(podcast_title):
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
        r'\baudio.*book\b',
        r'\bdownload\b',
        r'\bl\b',
        r'\b(?i)chapter\b',
        r'\b(?i)chapters\b',
        r'\b(?i)volume\b',
        r'\b(?i)ep\b',
        r'\b(?i)implantation\b',
        r'\b(?i)part\b',
        r'\b(?i)parts\b',
        r'\b(?i)number\b',
        r'\b(?i)voizvndownload\b',
        r'\b(?i)years\b',
        r'\b(?i)episode\b',
        r'\b(?i)shorts\b',
        r'\b(?i)verse\b',
        r'\b(?i)verses\b',
        r'\b(?i)entire\b',
        r'\b(?i)voizvn\b'
    ]

    # Check for common patterns and remove them
    for pattern in patterns:
        podcast_title = re.sub(pattern, ' ', podcast_title)
    
    # Remove punctuation and standardize spacing
    podcast_title = re.sub(r'[^\w\s]', '', podcast_title)
    podcast_title = re.sub(r'\s+', ' ', podcast_title)

    # Remove trailing whitespace and return the cleaned title
    return podcast_title.strip()


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




if __name__ == '__main__':
    # print(sys.path)
    # test function token english
    text = 'Học Python miễn phí tại freetuts.net. This is English, would you be able to detect it'
    text = 'Học Python miễn phí tại freetuts.net. This is English, would you be able to detect it'
    translator = Translator()
    dt = translator.detect(text)
    df = translator.translate(text, dest='en')
    print(dt, df.text)

# def word_cloud(df, column):
    # font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    # wordclouds = {}

    # output_folder = "plot_output"
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)
    # print(df)
    # # Loop through each year and extract the top words for each year
    # for year in df.index:
    #     text = df.loc[year, column]
    #     wordclouds[year] = text
    #     # wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(text)
    #     # wordclouds[year] = wordcloud

    #     # # Save the word cloud as an image
    #     # image_path = os.path.join(output_folder, f"wordcloud_{year}.png")
    #     # wordcloud.to_file(image_path)
    # print(wordclouds)


    # Remove the code for displaying the plots
