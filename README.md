# Music Searcher

    This project uses the Gemini and YouTube Data APIs to create a playlist of songs based on a user's text prompt.  It provides a JSON response containing the song title, artist, and YouTube URL.

## Installation

1. Clone the repository:

    ```
    git clone <your-repository-url>
    ```

2. Navigate to the project directory:

    ```
    cd music_search
    ```

3. Create a virtual environment (recommended):

    ```
    python3 -m venv .venv
    source .venv/bin/activate
    ```

4. Install dependencies:
    ```
    pip install -r requirements.txt
    ```

## Usage

1. Add your own API key and system instruction. The project is set up to use a .env for these values.

2. Run the script from the command line, providing your search prompt:
    ```
    python main.py "Give me five hard bop songs from the 1960s"
    ```
