"""
gemini_api_VEO.py

This script demonstrates how to generate a video using the Google Generative AI SDK.
It represents the culmination of extensive debugging and testing to find a method
that works with the currently available public library version.

Key Learnings & Why This Code Works:
1.  **Correct Import**: It uses `import google.generativeai as genai`. This is the
    stable and correct way to import the library, avoiding `ImportError` from
    namespace conflicts with other `google-*` packages.

2.  **Correct Client Initialization**: It uses `genai.GenerativeModel()`. The
    `genai.Client()` object, seen in some newer documentation, is not available
    in the current public library version. `GenerativeModel` is the correct
    class for all generation requests.

3.  **Correct Model Name**: It uses a specific, versioned model name,
    `"models/veo-2.0-generate-001"`. Generic names like "veo" or preview names
    like "veo-3.0-generate-preview" were not found by the API with this library
    version. This was a known working model at the time of writing.

4.  **Asynchronous Execution**: Video generation is a long-running operation.
    This script uses `asyncio` and `model.generate_content_async()` to handle
    the request without blocking the program. A generous timeout is also set.

This script serves as a reliable template for video generation.
"""

import os
import asyncio
from dotenv import load_dotenv
import google.generativeai as genai

# --- Load Environment Variables ---
load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file or environment")

# --- Configure the SDK ---
genai.configure(api_key=API_KEY)


# --- Configuration ---
# This model name was found to be available via API discovery.
MODEL_NAME = "models/veo-2.0-generate-001"
PROMPT = """A close up of two people staring at a cryptic drawing on a wall, torchlight flickering.
A man murmurs, 'This must be it. That's the secret code.' The woman looks at him and whispering excitedly, 'What did you find?'"""
OUTPUT_FILENAME = "dialogue_example_final.mp4"


async def generate_video():
    """
    Asynchronously generates and saves a video based on a text prompt.
    """
    print("Starting video generation process...")
    try:
        # 1. Initialize the GenerativeModel for video
        print(f"Initializing model: {MODEL_NAME}")
        model = genai.GenerativeModel(model_name=MODEL_NAME)

        # 2. Send the asynchronous generation request
        print(f"Sending prompt to model: '{PROMPT[:50]}...' ")
        response = await model.generate_content_async(
            [PROMPT],
            request_options={'timeout': 600}  # 10-minute timeout for the operation
        )

        # 3. Extract video data from the response
        print("Response received. Extracting video data...")
        video_part = next((part for part in response.parts if part.file_data), None)

        if not video_part:
            print("Error: No video data found in the API response.")
            print("Full response:", response)
            return

        # 4. Download the video file
        video_file_uri = video_part.file_data.uri
        print(f"Video data found. URI: {video_file_uri}")
        
        # Use the SDK's async file getter
        video_file = await genai.get_file_async(video_file_uri.split('/')[-1])
        
        print(f"Downloading video to '{OUTPUT_FILENAME}'...")
        with open(OUTPUT_FILENAME, "wb") as f:
            f.write(video_file.get_bytes())
            
        print(f"\nSuccess! Video saved to '{OUTPUT_FILENAME}'")

    except Exception as e:
        print(f"\nAn error occurred during video generation: {e}")


if __name__ == "__main__":
    # Run the asynchronous main function
    asyncio.run(generate_video())