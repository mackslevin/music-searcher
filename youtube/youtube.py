from googleapiclient.discovery import build, HttpError
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def create_youtube_query(track_title, artist_name):
    """ 
    Creates a very special YouTube search query for a song. 

    Args: 
    track_title: String, a song title.
    artist_name: String, the name of the artist who made that song.
    Returns: 
    String representing a YouTube search query.
    """
    return f"{artist_name} - {track_title} (Official Music Video)"

def get_youtube_url(track_title, artist_name):
    """ 
    Retrieves the first YouTube search result's URL for the given song.

    Args: 
      track_title: String, a song title.
      artist_name: String, the name of the artist who made that song.
    Returns:
      String representing a YouTube URL.
    """

    try: 
        youtube = build('youtube', 'v3', developerKey=GOOGLE_API_KEY)
        request = youtube.search().list(
            part='snippet',
            maxResults=1,
            q=create_youtube_query(track_title, artist_name), 
            type='video'
        )

        response = request.execute()
        if response['items']:
            video_id = response['items'][0]['id']['videoId']
            return f"https://www.youtube.com/watch?v={video_id}"
        else:
            return None
    except HttpError as e:
        print(f"YouTube API Error: {e}")  
        return None
    except Exception as e: 
        print(f"An unexpected error occurred: {e}")
        raise

    
    
    
    