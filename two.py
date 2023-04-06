import os
from googleapiclient.discovery import build

# set your API key
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCyUQGCgq86G-FUfz752oIUMPwQK8cOzi8'

# create YouTube API client
youtube = build('youtube', 'v3', developerKey=os.environ['GOOGLE_API_KEY'])

# specify the video ID of the live stream you want to retrieve information about
video_id = '7XgD6Wuou20'

# use the videos().list() method to retrieve information about the live stream
videos_list = youtube.videos().list(
    part='snippet,liveStreamingDetails',
    id=video_id
).execute()

# extract the start and end times of the live stream
start_time = videos_list['items'][0]['liveStreamingDetails']['actualStartTime']
end_time = videos_list['items'][0]['liveStreamingDetails']['actualEndTime']

# print the start and end times in ISO 8601 format
print('Start time:', start_time)
print('End time:', end_time)
