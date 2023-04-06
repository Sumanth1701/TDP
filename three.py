from googleapiclient.discovery import build
from datetime import datetime, timedelta
import json

# Enter your API key
api_key = "AIzaSyCyUQGCgq86G-FUfz752oIUMPwQK8cOzi8"

# Enter the YouTube video ID
video_id = "7XgD6Wuou20"

# Create a YouTube API client
youtube = build('youtube', 'v3', developerKey=api_key)

# Call the API to get video details
video_response = youtube.videos().list(id=video_id, part='snippet,statistics').execute()

# Extract video details
video = video_response['items'][0]
title = video['snippet']['title']
description = video['snippet']['description']
view_count = video['statistics']['viewCount']
like_count = video['statistics']['likeCount']
comment_count = video['statistics']['commentCount']

# Call the API to get video comments
comments_response = youtube.commentThreads().list(
    videoId=video_id,
    part='snippet',
    textFormat='plainText',
    order='time'
).execute()

# Extract comment details
comments = []
for item in comments_response['items']:
    comment = item['snippet']['topLevelComment']['snippet']
    author = comment['authorDisplayName']
    text = comment['textDisplay']
    timestamp = comment['publishedAt']
    comments.append({
        'author': author,
        'text': text,
        'timestamp': timestamp
    })

# Create a JSON object with video and comment details
data = {
    'title': title,
    'description': description,
    'view_count': view_count,
    'like_count': like_count,
    'comment_count': comment_count,
    'comments': comments
}

# Save JSON object to file
filename = f"{video_id}.json"
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
