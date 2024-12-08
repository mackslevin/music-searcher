import secrets
import google.generativeai as genai
import json
import typing_extensions as typing
import os
from dotenv import load_dotenv

load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_SYSTEM_INSTRUCTION = os.getenv("GEMINI_SYSTEM_INSTRUCTION")

class Song(typing.TypedDict):
    title: str
    artist: str

genai.configure(api_key=GOOGLE_API_KEY)
model = genai.GenerativeModel("gemini-1.5-pro-latest", system_instruction=GEMINI_SYSTEM_INSTRUCTION) 

def textFromGeminiResult(result):
    """ 
    Returns the text of the first candidate in the result. 
    Args: 
        A Google GenerateContentResponse object. (https://ai.google.dev/api/generate-content#generatecontentresponse)
    """
    try:
        return result.candidates[0].content.parts[0].text
    except (AttributeError, IndexError) as e:
        return f"Error extracting text from Gemini result: {e}"


def get_songs_from_gemini(prompt):
    """ 
    Returns a list of Song objects from a Gemini prompt. 
    
    Args: 
        prompt: String, the instructions for what kind of music the user would like
    Returns: 
        JSON list of objects structured to match the Song class (i.e. title and artist strings)
    """
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
