import pandas as pd
import os
from dotenv import load_dotenv
import ast
from matplotlib import pyplot as plt
from utils import clean_title
load_dotenv()
PATH = (os.environ.get('P'))

#change dir to path 
os.chdir(PATH)
from utils import tokenize_vietnamese, tokenize_text_Np, is_vietnamese, tokenize_english, detect_language, translate_text

file_path = PATH + '/data/youtube - episode_details - 59862 records.csv'
df = pd.read_csv(file_path)

def episode_name_translated(df):
    attributes = ['title', 'publishedAt', 'channelTitle']
    df = df[attributes]

    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df['publishedAt'] = df['publishedAt'].dt.year
    df['language'] = df['title'].apply(detect_language)

    vi_df = df[df['language'] == 'vi']
    en_df = df[df['language'] == 'en']

    # Translate Vietnamese to English
    vi_df['title'] = vi_df['title'].apply(translate_text)

    # # Create summary df to save distribution of all languages in the dataset
    # summary_df = pd.DataFrame(columns=['language', 'count'])
    # summary_df['language'] = df['language'].unique()
    # summary_df['count'] = [len(df[df['language'] == lang]) for lang in summary_df['language']]
    # summary_df.to_csv(PATH + '/modules/spotify/summary.csv', index=False)

    df.to_csv(PATH + '/data/youtube_title_language_detected.csv', index=False)
    vi_df.to_csv(PATH + '/data/vi_youtube_title_translated.csv', index=False)
    en_df.to_csv(PATH + '/data/en_youtube_title.csv', index=False)


def clean_topic_categories(x):
    try:
        x = ast.literal_eval(x)
        x = [i.replace("https://en.wikipedia.org/wiki/", "") for i in x]
    except:
        x = []
    return x

from collections import Counter

def most_frequent(List):
    try:
        # Count the occurrences of each element in the list
        counts = Counter(List)

        # Find the element with the highest count (most frequent)
        most_common_element = counts.most_common(1)

        # Return the most frequent element
        return most_common_element[0][0]
    
    except IndexError:
        return ''

def channel_stat_stars(df):
    df = pd.read_csv(PATH + '/data/podcast_list - chartable - channel_details - vn - no duplicates.csv')
    
    
def channel_stat(df):
    #group by channelTitle, sum viewcount, likecount, dislikecount, commentcount    
    df.topicCategories = df.topicCategories.apply(clean_topic_categories)
    #group df by channel title and merge topic categories list for each channel
    df['count'] = 1
    df = df.groupby(['channelTitle']).agg({'viewCount': 'sum', 'likeCount': 'sum', 'commentCount': 'sum', 'topicCategories': 'sum', 'count': 'sum'})
    df.topicCategories = df.topicCategories.apply(lambda x: most_frequent(x))
    df['averageViewCount'] = df['viewCount'] / df['count']
    df = df.sort_values(by=['viewCount'], ascending=False)
    df.to_csv(PATH + '/data/youtube_channel_stat.csv', index=True)

def category_distribution_view(df):
    df.topicCategories = df.topicCategories.apply(clean_topic_categories)
    # create line chart for category distribution throughout the years
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df['publishedAt'] = df['publishedAt'].dt.year
    df = df[['publishedAt', 'topicCategories', 'viewCount']]

    # Create a dictionary to store the view counts of each topic
    topic_view_counts = {}

    # Iterate through the DataFrame
    for _, row in df.iterrows():
        year = row['publishedAt']
        topics = row['topicCategories']
        
        for topic in topics:
            if topic not in topic_view_counts:
                topic_view_counts[topic] = {year: 0}
            if year in topic_view_counts[topic]:
                # Increment the view count for the topic in the given year
                # topic_view_counts[topic][year] += row['viewCount']
                topic_view_counts[topic][year] += 1
            else:
                # Initialize view count for the topic in the given year
                # topic_view_counts[topic][year] = row['viewCount']
                topic_view_counts[topic][year] = 1

    # Convert the dictionary to a DataFrame
    distribution_df = pd.DataFrame.from_dict(topic_view_counts, orient='index')
    distribution_df.fillna(0, inplace=True)
    distribution_df['Total'] = distribution_df.sum(axis=1)

    
    # Reset the index
    distribution_df.reset_index(inplace=True)
    distribution_df.rename(columns={'index': 'Topics'}, inplace=True)

    # Display the resulting DataFrame
    distribution_df.to_csv(PATH + '/data/youtube_category_distribution_by_year.csv', index=False)
    
    distribution_df = pd.read_csv(PATH + '/data/youtube_category_distribution_by_year.csv')
    # Select the "Total" column for the bar chart
    total_data = distribution_df[['Topics','Total']]
    total_data.sort_values(by=['Total'], ascending=False, inplace=True)
    total_data.set_index(total_data['Topics'], inplace=True)
    
    # Create a bar chart
    ax = total_data.plot(kind='bar', figsize=(12, 8), legend=None)
    plt.title('Number of videos on YouTube by category 2012 - 2023')
    plt.xlabel('Category')
    plt.ylabel('Total Number Of Video')
    # plt.savefig('plot_output/total_topic_distribution_bar_chart.png')
    plt.savefig('plot_output/total_topic_video_distribution_bar_chart.png')
    # Display the bar chart
    plt.show()
    
    
    
    
    
    
    
    
    # Calculate total view count for each topic
    distribution_df = distribution_df[distribution_df['Total'] > 0.01 * distribution_df['Total'].sum()]
    #drop column with total
    distribution_df.drop(columns=['Total'], inplace=True)
    distribution_df = distribution_df.iloc[:,::-1]
    ax = distribution_df.T.plot(kind='line', marker='o', figsize=(12, 6), title='Topic Distribution Over the Years')
    plt.xlabel('Year')
    plt.ylabel('Total Count')
    plt.grid(True)

    # Save the line chart as an image (e.g., PNG)
    plt.savefig('plot_output/topic_distribution_line_chart.png')

    # Show the chart (optional)
    plt.show()
    

    return distribution_df


df2 = category_distribution(df)
    
def category_distribution(df):
    df.topicCategories = df.topicCategories.apply(clean_topic_categories)
    # create line chart for category distribution throughout the years
    df['publishedAt'] = pd.to_datetime(df['publishedAt'])
    df['publishedAt'] = df['publishedAt'].dt.year
    df = df[['publishedAt', 'topicCategories']]


    # Create a dictionary to store the counts of each topic
    topic_counts = {}

    # Iterate through the DataFrame
    for _, row in df.iterrows():
        year = row['publishedAt']
        topics = row['topicCategories']
        
        for topic in topics:
            if topic not in topic_counts:
                topic_counts[topic] = {year: 1}
            else:
                if year in topic_counts[topic]:
                    topic_counts[topic][year] += 1
                else:
                    topic_counts[topic][year] = 1

    # Convert the dictionary to a DataFrame
    distribution_df = pd.DataFrame.from_dict(topic_counts, orient='index')
    distribution_df.fillna(0, inplace=True)

    # Sum the counts for each topic across years to get the total count
    distribution_df['Total'] = distribution_df.sum(axis=1)

    # Reset the index
    distribution_df.reset_index(inplace=True)
    distribution_df.rename(columns={'index': 'Topics'}, inplace=True)

    # Display the resulting DataFrame
    distribution_df.to_csv(PATH + '/data/youtube_category_distribution_by_year.csv', index=False)
    
    distribution_df = pd.read_csv(PATH + '/data/youtube_category_distribution_by_year.csv')
    # Select the "Total" column for the bar chart
    total_data = distribution_df[['Total']]
    total_data.sort_values(by=['Total'], ascending=False, inplace=True)
    total_data.set_index(distribution_df['Topics'], inplace=True)
    
    # Create a bar chart
    ax = total_data.plot(kind='bar', figsize=(12, 8), legend=None)
    plt.title('Total Topic distribution 2012 - 2023 ranked by total view count')
    plt.xlabel('Year')
    plt.ylabel('Total View Count')
    plt.savefig('plot_output/total_topic_distribution_bar_chart.png')
    # Display the bar chart
    plt.show()
    
    #drop column with total count less than 1%
    distribution_df = distribution_df[distribution_df['Total'] > 0.01 * distribution_df['Total'].sum()]
    
    distribution_df.drop(columns=['Total'], inplace=True)
    distribution_df = distribution_df.iloc[:,::-1]
    distribution_df.set_index('Topics', inplace=True)
    ax = distribution_df.T.plot(kind='line', marker='o', figsize=(12, 6), title='Topic Distribution Over the Years')
    plt.xlabel('Year')
    plt.ylabel('Total Count')
    plt.grid(True)

    # Save the line chart as an image (e.g., PNG)
    plt.savefig('plot_output/topic_distribution_line_chart.png')

    # Show the chart (optional)
    plt.show()
    

# if __name__ == '__main__':
#     # episode_description_translated(df)
#     categorized_df = pd.read_csv(PATH + '/data/spotify_name_language_detected.csv')
#     data = create_full_country_mapping(categorized_df)

#     total_count = sum(data.values())

#     # Define the threshold for languages below 1%
#     threshold = total_count * 0.01

#     # Create a new dictionary to store the combined data
#     combined_data = {}

#     # Iterate through the data and combine languages below the threshold
#     for language, count in data.items():
#         if count >= threshold:
#             combined_data[language] = count
#         else:
#             combined_data['Other'] = combined_data.get('Other', 0) + count


#     labels = combined_data.keys()
#     sizes = combined_data.values()

#     # Create a pie chart
#     plt.figure(figsize=(10, 8))
#     plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=140)
#     plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.

#     # Set the title
#     plt.title("Distribution of Country Names")

#     # Show the pie chart
#     plt.savefig('plot_output/language_distribution.png')
