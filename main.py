import json
import sys
import gemini.gemini as gemini
import youtube.youtube as youtube

def generate_songs(prompt):
    """
    Searches for music based on a prompt and returns results in JSON format.
    
    Args: 
        prompt: String, the instructions for what kind of music the user would like
    Returns: 
        JSON list representing a playlist of songs. This is the structure: 
        [
            { 
                "title": String,
                "artist": String,
                "youtube_url": String?
            }
        ]
    """

    songs = gemini.get_songs_from_gemini(prompt)

    if isinstance(songs, str) and songs.startswith("Error"):  # Check if Gemini returned an error
        return json.dumps({"error": songs}, indent=4)

    results = []
    for song in songs:
        youtube_url = youtube.get_youtube_url(song["title"], song["artist"])
        results.append({
            "title": song["title"],
            "artist": song["artist"],
            "youtube_url": youtube_url
        })

    return json.dumps(results, indent=4)


if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_prompt = " ".join(sys.argv[1:])  # Combine all arguments after the script name
        print(generate_songs(user_prompt))
    else:
        print(json.dumps({"error": "No prompt provided"}, indent=4))

