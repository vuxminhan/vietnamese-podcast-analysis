import regex as re
import numpy as np
import pandas as pd
from underthesea import pos_tag
import os
from dotenv import load_dotenv
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import ast
from collections import Counter
from unidecode import unidecode
import sys
from googletrans import Translator
import spacy
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
    print("detected language")
    return Translator().detect(sentence).lang

def translate_text(sentence, dest='en'):
    print("transplated")
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


if __name__ == '__main__':
    # print(sys.path)
    # test function token english
    text = 'Học Python miễn phí tại freetuts.net. This is English, would you be able to detect it'
    translator = Translator()
    dt = translator.detect(text)
    df = translator.translate(text, dest='en')
    print(dt, df.text)

def word_cloud(df, column):
    font_path = "/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf"
    wordclouds = {}

    output_folder = "plot_output"
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    # Loop through each year and extract the top words for each year
    for year in df.index:
        text = df.loc[year, column]
        wordcloud = WordCloud(width=800, height=400, background_color='white', font_path=font_path).generate(text)
        wordclouds[year] = wordcloud

        # Save the word cloud as an image
        image_path = os.path.join(output_folder, f"wordcloud_{year}.png")
        wordcloud.to_file(image_path)

