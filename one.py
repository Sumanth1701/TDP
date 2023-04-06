import os
from googleapiclient.discovery import build
from datetime import datetime, timedelta



# set your API key
os.environ['GOOGLE_API_KEY'] = 'AIzaSyCyUQGCgq86G-FUfz752oIUMPwQK8cOzi8'

# create YouTube API client
youtube = build('youtube', 'v3', developerKey=os.environ['GOOGLE_API_KEY'])


published_after = '2023-03-05T01:17:19Z'  # replace with your desired start time in ISO 8601 format
published_before = strftime('2023-03-05T03:35:20Z')  # replace with your desired end time in ISO 8601 format

# retrieve the video ID of the first search result
video_id = "7XgD6Wuou20"

# Convert the time frame strings to datetime objects
start_time_dt = datetime.fromisoformat(published_after)
end_time_dt = datetime.fromisoformat(published_before)

# Call the API to retrieve the comments for the video
next_page_token = ''
while next_page_token is not None:
    comments = youtube.commentThreads().list(
        part='snippet',
        videoId=video_id,
        pageToken=next_page_token
    ).execute()

    for comment in comments['items']:
        # Check if the comment was published within the time frame
        comment_time = datetime.fromisoformat(comment['snippet']['publishedAt'])
        if comment_time is None:
            continue  # skip if publishedAt key is not present
        comment_time = datetime.fromisoformat(comment_time[:-1])
        if start_time_dt <= comment_time <= end_time_dt:
            # Print the comment text and timestamp
            print(f"{comment['snippet']['topLevelComment']['snippet']['textOriginal']} - {comment_time}")
    
    # Check if there are more pages of comments to retrieve
    if 'nextPageToken' in comments:
        next_page_token = comments['nextPageToken']
    else:
        next_page_token = None
