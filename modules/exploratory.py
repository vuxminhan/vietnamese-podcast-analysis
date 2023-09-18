# from modules.youtube.extractor import *
import json
import glob
import os
from dotenv import load_dotenv
import pandas as pd
import re
import seaborn as sns
import matplotlib.pyplot as plt
import lux
from lux.vis.Vis import Vis
load_dotenv()
PATH = (os.environ.get('P'))

df = pd.read_csv(PATH + '/data/podcast_list - chartable - channel_details - vn - no duplicates - videodetails - 59862 records.csv')
df['publishedAt'] = pd.to_datetime(df['publishedAt'])
df = df[df['channelTitle']!='Truyền hình Đài Tiếng nói Việt Nam - VOVTV']

from wordcloud import WordCloud

import re
import matplotlib.pyplot as plt
import pandas as pd
from urllib.request import urlopen

with open(PATH + '/data/vietnamese-stopwords-dash.txt', 'r', encoding='utf-8') as f:
    vietnamese_stopwords = list(f.read().splitlines())

vietnamese_stopwords.extend(['best', 'cut', 'tập', 'podcast', "episode", "short", "shorts",])

# Convert float values in the 'description' column to strings
df['description'] = df['description'].astype(str)
from underthesea import word_tokenize, pos_tag
# Function to tokenize text using underthesea.word_tokenize and remove special characters and stop words
def tokenize_text(text, word_type = ['V']):
    text = re.sub(r"[!#$%&'()*+,-./:;<=>?@[\]^_`{|}~]", " ", text)
    text = re.sub(r"\\n", "", text)
    text = re.sub(r"\\", "", text)
    text = re.sub(r"\n", "", text)
    text = re.sub(r"\t", "", text)
    text = re.sub(r'"', "", text)
    words = pos_tag(text.lower(), format="text")
    words = [word[0] for word in words if word[0].strip().lower() not in vietnamese_stopwords and word[1] in word_type]
    return ' '.join(words)
  
    





# MOST FREQUENT WORDS IN VIDEO TAGS

# reduce the dataset such that each channel has only its 10 most viewed videos each year it was published
# Parse 'publishedAt' column to extract the year
df['publishedAt'] = pd.to_datetime(df['publishedAt'])
df['year'] = df['publishedAt'].dt.year

#  Group by 'channelId' and the parsed year, then select the top 10 most viewed videos for each group
reduced_df = df.groupby(['channelId', 'year']).apply(lambda group: group.nlargest(10, 'viewCount'))

# Reset index to create a flat DataFrame
reduced_df = reduced_df.reset_index(drop=True)

# Group the data by year and tag, and calculate the total view counts
grouped_df = df.groupby([df['publishedAt'].dt.year, 'tags']).agg({'viewCount': 'sum'}).reset_index()

# Specify the number of top tags to feature in the word cloud
top_tags_count = 20
threshold = 0.01  # Adjust the threshold as desired

# Calculate the total view counts for each tag within a year
yearly_total_view_counts = grouped_df.groupby('publishedAt')['viewCount'].transform('sum')

# Filter the data to include only tags with a view count above the threshold
filtered_df = grouped_df[grouped_df['viewCount'] / yearly_total_view_counts > threshold]

# Find the top tags with the highest view counts for each year
top_tags = filtered_df.groupby('publishedAt').apply(lambda x: x.nlargest(top_tags_count, 'viewCount')).reset_index(drop=True)

# Modify the tags column to replace spaces with underscores
top_tags['tags'] = top_tags['tags'].str.replace(' ', '_')

# Generate word clouds for the top tags in each year
for year, year_tags in top_tags.groupby('publishedAt'):
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(' '.join(year_tags['tags']))

    # Plot the word cloud
    plt.figure(figsize=(10, 6))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.title(f"Top {top_tags_count} Tags (Threshold: {threshold}) - Year {int(year)}")
    plt.axis('off')
    plt.show()
    
    

# # MOST FREQUENT WORDS IN VIDEO TITLES
# # Group the data by year and concatenate tokenized video titles and descriptions for each year
# grouped_df = df.groupby(df['publishedAt'].dt.year).agg({'title': lambda x: ' '.join(map(tokenize_text, x))}).reset_index()

# # Create a dictionary to store the word frequencies for each year
# word_freq_dict = {}

# # Generate word clouds for video titles for each year and calculate word frequencies
# for index, row in grouped_df.iterrows():
#     # Generate word cloud for video titles
#     title_wordcloud = WordCloud(width=800, height=400, background_color='white')
#     wordcloud = title_wordcloud.generate(row['title'])

#     # Get word frequencies
#     word_freq = title_wordcloud.process_text(row['title'])

#     # Convert word frequencies to a DataFrame
#     table_data = pd.DataFrame(list(word_freq.items()), columns=['Word', f"Year {int(row['publishedAt'])}"])
#     table_data.set_index('Word', inplace=True)

#     # Add the word frequencies to the dictionary
#     print(table_data.sort_values(by=f"Year {int(row['publishedAt'])}", ascending=False).head(10))

#     # Plot the word clouds
#     plt.figure(figsize=(8, 4))
#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.title(f"Most Common Words in Video Titles - Year {int(row['publishedAt'])}")
#     plt.axis('off')

#     plt.show()

    
    
# def tokenize_text(text, word_type=['V']):
#     text = re.sub(r"[!#$%&'()*+,-./:;<=>?@[\]^_`{|}~]", " ", text)
#     text = re.sub(r"\\n", "", text)
#     text = re.sub(r"\\", "", text)
#     text = re.sub(r"\n", "", text)
#     text = re.sub(r"\t", "", text)
#     text = re.sub(r'"', "", text)
#     words = pos_tag(text.lower(), format="text")  # Convert all words to lowercase
#     words = [word[0] for word in words if word[0].lower() not in vietnamese_stopwords and word[1] in word_type]
#     words = list(set(words))  # Remove duplicates from the list of tokens
#     return ' '.join(words)

# # Group the data by year and concatenate tokenized video titles and descriptions for each year
# grouped_df = df.groupby(df['publishedAt'].dt.year).agg({'title': lambda x: ' '.join(map(tokenize_text, x))}).reset_index()

# # Create a dictionary to store the word frequencies for each year
# word_freq_dict = {}

# # Generate word clouds for video titles for each year and calculate word frequencies
# for index, row in grouped_df.iterrows():
#     # Generate word cloud for video titles
#     title_wordcloud = WordCloud(width=800, height=400, background_color='white')
#     wordcloud = title_wordcloud.generate(row['title'])

#     # Get word frequencies
#     word_freq = title_wordcloud.process_text(row['title'])

#     # Convert word frequencies to a DataFrame
#     table_data = pd.DataFrame(list(word_freq.items()), columns=['Word', f"Year {int(row['publishedAt'])}"])
#     table_data.set_index('Word', inplace=True)

#     # Add the word frequencies to the dictionary
#     word_freq_dict[f"Year {int(row['publishedAt'])}"] = word_freq

#     # Plot the word clouds
#     plt.figure(figsize=(8, 4))
#     plt.imshow(wordcloud, interpolation='bilinear')
#     plt.title(f"Most Common Words in Video Titles - Year {int(row['publishedAt'])}")
#     plt.axis('off')

#     plt.show()

# # Create a DataFrame to store word frequencies for all years
# result_df = pd.DataFrame(word_freq_dict)
# result_df = result_df.fillna(0)
# result_df = result_df.sort_values(by='Year 2023', ascending=False)



# #fix all error in this explorations word cloud
# # combine dataset podcast search
# # redraw trend chart on google sheet

# # create dashboard for module spotify
# # create dashboard for module youtube

