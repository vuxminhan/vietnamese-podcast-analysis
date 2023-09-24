import requests
from bs4 import BeautifulSoup
import re
import pandas as pd
import os
from dotenv import load_dotenv
import matplotlib.pyplot as plt
import seaborn as sns
load_dotenv()
PATH = (os.environ.get('P'))

def get_star_ratings(url_list):
    pattern = r'(\d+\.\d+)\((\d+)\)'
    results = []

    for url in url_list:
        # Send a GET request to the URL
        try: 
            response = requests.get(url)

        # Check if the request was successful
            if response.status_code == 200:
                # Parse the HTML content of the page using BeautifulSoup
                soup = BeautifulSoup(response.text, 'html.parser')

                # Locate the element that contains the star rating information
                # You would need to inspect the HTML structure of the page to find the right element
                # and extract the star rating from it.

                # For example, if the star rating is in a <div> element with a class "star-rating",
                # you might do something like this:
                star_rating_element = soup.find('button', class_='_yl4tOZxcpoUt28k6B8I')

                if star_rating_element:
                    # Extract the star rating value
                    star_rating = star_rating_element.text.strip()
                    match = re.search(pattern, star_rating)
                    if match:
                        star_rating = match.group(1)  # Extract the star rating (group 1)
                        num_ratings = match.group(2)  # Extract the number of ratings (group 2)
                        results.append({"url": url, "star_rating": star_rating, "num_ratings": num_ratings})
                    else:
                        print("No match found in the input string for URL:", url)
                else:
                    print("Star rating not found on the page for URL:", url)
            else:
                print("Failed to retrieve the web page for URL:", url)
        except:
            print("Failed to retrieve the web page for URL:", url)
    
    return results

if __name__ == "__main__":
    # Read the CSV file into a DataFrame
    # df = pd.read_csv(PATH + '/data/podcast_list - chartable - channel_id.csv')
    # df1 = pd.read_csv(PATH + '/data/podcast_list - chartable - channel_details1.csv')
    # spotify = df.merge(df1, left_on='youtube_channel_id', right_on='channel_id', how='left')
    # spotify = spotify[['channel_title','published_at', 'spotify', 'youtube_channel_id']]
    # youtube = pd.read_csv(PATH + '/data/youtube_channel_stat.csv')
    # # get only channel stat with topicCategory being Entertainment, Business or Religion

    # both = youtube.merge(spotify, left_on='channelTitle', right_on='channel_title', how='left').drop_duplicates()
    # both.drop_duplicates(inplace=True)
    
    # both.to_csv(PATH + '/data/pocast_list-chartable-channel_id-both_platform.csv')
    # results = get_star_ratings(both['spotify'].tolist())
    # results_df = pd.DataFrame(results)
    # test = both.merge(results_df, left_on='spotify', right_on='url', how='left').to_csv(PATH + '/data/pocast_list-chartable-channel_id-both-star_ratings.csv', encoding = 'utf-8' ,index=False)
    
    df = pd.read_csv(PATH + '/data/pocast_list-chartable-channel_id-both-star_ratings.csv')
    
    # Sort the DataFrame by the weighted ranking in descending order
    # df = df.sort_values(by='weighted_rank', ascending=False)

    # Create separate ranking bar charts for Spotify, YouTube, and both platforms
    top_channels_spotify = df.sort_values(by=['star_rating','num_ratings'], ascending=False)
    top_channels_spotify.reset_index(drop=True, inplace=True)
    top_channels_spotify['spotify_rank'] = top_channels_spotify.index + 1
    top_channels_spotify.sort_values(by='spotify_rank', ascending=True, inplace=True) 
    
    top_channels_youtube = df.sort_values(by='likeCount', ascending=False).drop_duplicates(subset=['youtube_channel_id'])
    top_channels_youtube.reset_index(drop=True, inplace=True)
    top_channels_youtube['youtube_rank'] = top_channels_youtube.index + 1
    top_channels_youtube.sort_values(by='youtube_rank', ascending=True, inplace=True)
    
    top_channels_both = top_channels_spotify.join(top_channels_youtube.set_index('channelTitle'), on='channelTitle', how='inner', lsuffix='_spotify', rsuffix='_youtube')
    top_channels_both['average_rank'] = (top_channels_both['spotify_rank'] + top_channels_both['youtube_rank']) / 2
    top_channels_both.sort_values(by='average_rank', ascending=True, inplace=True)
    # Create figure and axes for the subplots
    fig, axes = plt.subplots(nrows=3, ncols=1, figsize=(10, 15))

    # Plotting the top 15 channels on Spotify
    sns.barplot(x='star_rating', y='channelTitle', data=top_channels_spotify.head(15), ax=axes[0], palette='viridis')
    axes[0].set_title('Top 15 Channels on Spotify based on Star Rating')

    # Plotting the top 15 channels on YouTube
    sns.barplot(x='likeCount', y='channelTitle', data=top_channels_youtube.head(15), ax=axes[1], palette='magma')
    axes[1].set_title('Top 15 Channels on YouTube based on Like Count')

    # Plotting the top 15 channels on both platforms combined
    sns.barplot(x='average_rank', y='channelTitle', data=top_channels_both.head(17), ax=axes[2], palette='plasma')
    axes[2].set_title('Top 15 Channels on Both Platforms (Weighted Rank)')

    # Adjusting spacing between subplots
    plt.tight_layout()

    # Show the plots
    plt.show()
    
    # average_rank_by_category = df.groupby('topicCategories')['weighted_rank'].mean().reset_index()

    # # Sort the DataFrame by average ranking in descending order
    # average_rank_by_category = average_rank_by_category.sort_values(by='weighted_rank', ascending=False)

    # # Create a bar chart for average ranking by topicCategory
    # plt.figure(figsize=(10, 6))
    # sns.barplot(x='weighted_rank', y='topicCategories', data=average_rank_by_category, palette='viridis')
    # plt.title('Average Ranking by Topic Category')
    # plt.xlabel('Average Weighted Rank')
    # plt.ylabel('Topic Category')
    # plt.show()