from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

def fetch_video_comments(video_id, api_key):
    # Create a YouTube API client
    youtube = build('youtube', 'v3', developerKey = api_key)

    try:
        # Get video comments using the video's ID
        comments = []
        nextPageToken = None

        while True:
            response = youtube.commentThreads().list(
                part='snippet',
                videoId=video_id,
                pageToken=nextPageToken,
                maxResults=100
            ).execute()

            # Iterate through each comment thread
            for item in response['items']:
                comment = item['snippet']['topLevelComment']['snippet']['textDisplay']
                comments.append(comment)

            # Check if there are more comments
            nextPageToken = response.get('nextPageToken')
            if not nextPageToken:
                break

        return comments

    except HttpError as e:
#        print('An HTTP error occurred:')
#        print(e)
        return "ERROR 1"




