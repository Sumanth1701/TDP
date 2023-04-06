from googleapiclient.discovery import build
from datetime import datetime, timedelta
import json


api_key = "AIzaSyCyUQGCgq86G-FUfz752oIUMPwQK8cOzi8"

video_id = "7XgD6Wuou20"

youtube = build('youtube', 'v3', developerKey=api_key)


videos_list = youtube.videos().list(
    part='snippet,liveStreamingDetails',
    id=video_id
).execute()

start_time = videos_list['items'][0]['liveStreamingDetails']['actualStartTime']
end_time = videos_list['items'][0]['liveStreamingDetails']['actualEndTime']

print('Start time:', start_time)
print('End time:', end_time)


video_response = youtube.videos().list(id=video_id, part='snippet,statistics').execute()

video = video_response['items'][0]
title = video['snippet']['title']
description = video['snippet']['description']
view_count = video['statistics']['viewCount']
like_count = video['statistics']['likeCount']
comment_count = video['statistics']['commentCount']

comments_response = youtube.commentThreads().list(
    videoId=video_id,
    part='snippet',
    textFormat='plainText',
    order='time'
).execute()

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

data = {
    'title': title,
    'description': description,
    'view_count': view_count,
    'like_count': like_count,
    'comment_count': comment_count,
    'comments': comments
}

filename = f"{video_id}.json"
with open(filename, 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
