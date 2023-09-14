from modules.youtube.extractor import *
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


df = pd.read_csv(PATH + '/data/podcast_list - chartable.csv')
df.drop(columns=['Unnamed: 0', 'Unnamed: 1'], inplace=True)

# get youtube channel id
df.fillna('', inplace=True)
df['youtube_channel_id'] = df['youtube'].apply(lambda x: extract_channel_id_from_url(x))
df.to_csv(PATH + '/data/podcast_list - chartable - channel_id.csv')

# get channel info
df = pd.read_csv(PATH + '/data/podcast_list - chartable - channel_id.csv')
res = []
for id in df['youtube_channel_id'].tolist():
    if id:
        channel = get_channel(id)
        if channel:
            res.append(channel)
    else:
        pass
df_channel = pd.DataFrame(res)
df_channel.to_csv(PATH + '/data/podcast_list - chartable - channel_details1.csv')   

#apply funtion category_to_list to df[topic_categories]
df_channel = pd.read_csv(PATH + '/data/podcast_list - chartable - channel_details.csv')

# drop rows with duplicate channel_id
df_channel.drop_duplicates(subset="channel_id", inplace=True)

# apply category_to_list function to topic_categories column
df_channel['topic_categories'] = df_channel['topic_categories'].apply(lambda x: category_to_list(x))

# drop columns that aren't needed
df_channel.drop(columns=['Unnamed: 0','topic_ids'], inplace=True)

# drop rows with missing values in channel_country column
df_channel.dropna(subset='channel_country', inplace=True)

# drop rows with missing values
df_channel.dropna(inplace=True)

# visualize channel_country column
Vis(['channel_country'],df_channel)

df_channel = pd.read_csv(PATH + '/data/podcast_list - chartable - channel_details.csv')

# drop duplicate rows
df_channel.drop_duplicates(subset="channel_id", inplace=True)

# split topic categories into a list
df_channel['topic_categories'] = df_channel['topic_categories'].apply(lambda x: category_to_list(x))

# drop unnecessary columns
df_channel.drop(columns=['Unnamed: 0','topic_ids'], inplace=True)

# filter for only Vietnamese channels
df_vn = df_channel[df_channel['channel_country'] == 'VN']

# save as csv
df_vn.to_csv(PATH + '/data/podcast_list - chartable - channel_details - vn - no duplicates.csv')

result_df = pd.read_csv(PATH + '/data/podcast_list - chartable - channel_details - vn - no duplicates.csv')
#count video by category
categories = df_vn.explode('topic_categories')['topic_categories'].unique()
distinct_categories = []
for item in categories:
    for i in item.split(','):
        if i not in distinct_categories:
            distinct_categories.append(re.sub('\W+','', i))

distinct_categories = list(set(distinct_categories))
total_video_count = {}
total_view_count = {}
total_subscriber_count = {}
total_channel_count = {}

for i,r in df_vn.iterrows():
    for category in r['topic_categories'].split(','):
        category = re.sub('\W+','', category)
        if category not in total_video_count:
            total_video_count[category] = r['video_count']
            total_view_count[category] = r['view_count']
            total_subscriber_count[category] = r['subscriber_count']
            total_channel_count[category] = 1
        else:
            total_video_count[category] += r['video_count']
            total_view_count[category] += r['view_count']
            total_subscriber_count[category]+= r['subscriber_count']
            total_channel_count[category] += 1
            
result_df = pd.DataFrame({'category': list(total_video_count.keys()),
                          'total_video_count': list(total_video_count.values()),
                          'total_channel_count': list(total_channel_count.values()),
                          'total_view_count': list(total_view_count.values()),
                            'total_subscriber_count': list(total_subscriber_count.values())})

result_df.to_csv(PATH + '/data/podcast_list - chartable - channel_details - vn - view_by_category.csv')


# Assuming you have the 'result_df' DataFrame as calculated previously

# Create subplots for each column
fig, axes = plt.subplots(4, 1, figsize=(10, 16))

# Plot for total_video_count
sns.barplot(ax=axes[0], x='category', y='total_video_count', data=result_df, palette='Blues_d', order=result_df.sort_values('total_video_count', ascending=False).category)
axes[0].set_title('Total Video Count by Category')
axes[0].set_xlabel('Category')
axes[0].set_ylabel('Total Video Count')
axes[0].tick_params(axis='x', rotation=90)

# Plot for total_channel_count
sns.barplot(ax=axes[1], x='category', y='total_channel_count', data=result_df, palette='Greens_d', order=result_df.sort_values('total_channel_count', ascending=False).category)
axes[1].set_title('Total Channel Count by Category')
axes[1].set_xlabel('Category')
axes[1].set_ylabel('Total Channel Count')
axes[1].tick_params(axis='x', rotation=90)

# Plot for total_view_count
sns.barplot(ax=axes[2], x='category', y='total_view_count', data=result_df, palette='Oranges_d', order=result_df.sort_values('total_view_count', ascending=False).category)
axes[2].set_title('Total View Count by Category')
axes[2].set_xlabel('Category')
axes[2].set_ylabel('Total View Count')
axes[2].tick_params(axis='x', rotation=90)

# Plot for total_subscriber_count
sns.barplot(ax=axes[3], x='category', y='total_subscriber_count', data=result_df, palette='Reds_d', order=result_df.sort_values('total_subscriber_count', ascending=False).category)
axes[3].set_title('Total Subscriber Count by Category')
axes[3].set_xlabel('Category')
axes[3].set_ylabel('Total Subscriber Count')
axes[3].tick_params(axis='x', rotation=90)

# Adjust spacing between subplots
plt.tight_layout()

# Show the plots
plt.show()


#get top 10 channel by subscriber

df_vn.sort_values(by=['subscriber_count'], ascending=False).head(20)




#postage (contain tokenize) keep only noun, verb, adj, private name, location name
#draw word cloud by year
#get a table of top 10 videos by year


# finish module spotify
# reuse function from youtube and draw word cloud on episodes by year on spotify

result_df = pd.read_csv(PATH + '/data/podcast_list - chartable - channel_details - vn.csv')
result_df.drop(columns=['Unnamed: 0'], inplace=True)
result_df.dropna(subset=['category'], inplace=True)
Vis(['category', 'total_video_count'],result_df)
Vis(['category', 'total_channel_count'],result_df)
Vis(['category', 'total_view_count'],result_df)
Vis(['category', 'total_subscriber_count'],result_df)

result_df.intent = ['category']
result_df



#get a video text pool for each channel 
df_channel = pd.read_csv(PATH + '/data/podcast_list - chartable - channel_details - vn - no duplicates.csv')

#apply funtion get_playlist_item to df[related_playlist_uploads]
df_channel['channel_video_ids'] = df_channel['related_playlist_uploads'].apply(lambda x: get_playlist_items(x))


df_vn_channel_videos = df_channel[['channel_id', 'channel_title', 'channel_video_ids']].copy()
df_vn_channel_videos = df_vn_channel_videos.explode('channel_video_ids').reset_index()
df_vn_channel_videos.drop(columns=['index'], inplace=True)



ids = df_vn_channel_videos['channel_video_ids'].tolist()
ids = [ids[i:i + 30] for i in range(0, len(ids), 30)]
rec = []
for id in ids:
    sub_res = get_video_details(id)[0].get('items')
    for res in sub_res:
        rec.append(
            {
                'id': res.get('id'),
                'title': res.get('snippet', {}).get('title'),
                'description': res.get('snippet', {}).get('description'),
                'publishedAt': res.get('snippet', {}).get('publishedAt'),
                'channelId': res.get('snippet', {}).get('channelId'),
                'channelTitle': res.get('snippet', {}).get('channelTitle'),
                'categoryId': res.get('snippet', {}).get('categoryId'),
                'tags': res.get('snippet', {}).get('tags'),
                'duration': res.get('contentDetails', {}).get('duration'),
                'viewCount': res.get('statistics', {}).get('viewCount'),
                'likeCount': res.get('statistics', {}).get('likeCount'),
                'commentCount': res.get('statistics', {}).get('commentCount'),
                'topicCategories': res.get('topicDetails', {}).get('topicCategories')
            }
        )
df = pd.DataFrame(rec)
df.to_csv(PATH + '/data/podcast_list - chartable - channel_details - vn - no duplicates - videodetails - 59862 records.csv', index=False)


Vis(['title'],df)

