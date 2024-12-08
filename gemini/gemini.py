import secrets
import google.generativeai as genai
import json
import typing_extensions as typing
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

class Song(typing.TypedDict):
    title: str
    artist: str

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest", system_instruction="""
        - You will respond only in valid JSON. The response will be a playlist of songs.
        - You are to recommend good music, by critical standards, as much as possible. That said, some music genres simply don't have much content that fits that description, so in those cases you should be a poptimist, so to speak.
        - In your recommendations, you focus on important and influential work.
        - You are not afraid to toss out an obscure recommendation when appropriate.
        - When it comes to genre, you want to be as specific as possible. For example, rather than 'indie rock', you would gravitate toward something more specific, like 'early-2000s psychedelic indie pop'.         
        - You will serve as a bit of a music educator to the user, giving them songs that define and are emblematic of the type of music they request.                
    """) 

def textFromGeminiResult(result):
    """ Returns the text of the first candidate in the result. """
    try:
        return result.candidates[0].content.parts[0].text
    except (AttributeError, IndexError) as e:
        return f"Error extracting text from Gemini result: {e}"


def get_songs_from_gemini(prompt):
    """ Returns a list of Song objects from a Gemini prompt. """
    try:
        gemini_result = model.generate_content(
            prompt, 
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=list[Song]
            )
        )
        songs_json = textFromGeminiResult(gemini_result)
        error_prefix = "Error extracting text from Gemini result:"
        if songs_json.startswith(error_prefix):
            return songs_json

        songs = json.loads(songs_json)
        if not isinstance(songs, list):
             return f"Unexpected Gemini response format: Expected list, got {type(songs)}"
        for song in songs:
          if not isinstance(song.get("title"), str) or not isinstance(song.get("artist"), str):
            return f"Invalid song format in Gemini response: {song}"


        return songs

    except (genai.types.APIError, json.JSONDecodeError) as e:
        return f"Error processing Gemini response: {e}"
