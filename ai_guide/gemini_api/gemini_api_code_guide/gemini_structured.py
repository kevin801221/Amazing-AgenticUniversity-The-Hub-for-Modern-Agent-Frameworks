"""
gemini_structured.py

This script demonstrates how to generate structured data (JSON) using the 
Google Generative AI SDK for Python. It represents the most stable method,
bypassing potential Pydantic compatibility issues by defining the JSON schema manually.

Key Learnings & Why This Code Works:
1.  **Correct Import & Initialization**: Uses `import google.generativeai as genai`
    and `genai.GenerativeModel()`, which is the correct approach for the current
    public library version.

2.  **Manual JSON Schema**: Instead of relying on the SDK's Pydantic integration,
    this script defines the desired JSON structure manually as a Python dictionary.
    This avoids compatibility errors (like '$ref' or 'unbound method' issues)
    between the SDK and specific versions of Pydantic or Python. This is the most
    robust method for ensuring structured JSON output.

This script serves as a reliable example for generating structured JSON with
the Gemini API in a typical Python environment.
"""

import os
import json
from dotenv import load_dotenv
import google.generativeai as genai

# --- Load Environment Variables ---
load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file or environment")

# --- Configure the SDK ---
genai.configure(api_key=API_KEY)


# --- Manually Define the JSON Schema ---
# This dictionary describes the exact structure we want the API to return.
# Defining it manually is more stable than using Pydantic's schema generation.
RECIPE_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "recipe_name": {
                "type": "string",
                "description": "The name of the cookie recipe."
            },
            "ingredients": {
                "type": "array",
                "items": {
                    "type": "string"
                },
                "description": "A list of ingredients with their amounts."
            }
        },
        "required": ["recipe_name", "ingredients"]
    }
}


def generate_structured_recipes():
    """
    Generates a list of cookie recipes by providing a manual JSON schema.
    """
    print("Initializing model (gemini-2.5-flash)...")
    try:
        # 1. Initialize the GenerativeModel with the correct model name
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")

        # 2. Define the generation configuration for JSON output
        generation_config = genai.types.GenerationConfig(
            response_mime_type="application/json",
            # Pass the manually defined dictionary as the schema.
            response_schema=RECIPE_SCHEMA,
        )

        # 3. Send the request to the API
        prompt = "List a few popular cookie recipes, and include the amounts of ingredients."
        print(f"Sending prompt: '{prompt}'")
        response = model.generate_content(
            prompt,
            generation_config=generation_config
        )

        # 4. Process and display the response
        print("\n--- Raw JSON Response from API ---")
        print(response.text)

        print("\n--- Parsed Python Objects ---")
        # The output is a JSON string, which can be loaded into Python objects.
        parsed_recipes = json.loads(response.text)
        
        for i, recipe in enumerate(parsed_recipes, 1):
            print(f"\nRecipe #{i}: {recipe.get('recipe_name', 'N/A')}")
            print("Ingredients:")
            for ingredient in recipe.get('ingredients', []):
                print(f"  - {ingredient}")
        
        return parsed_recipes

    except Exception as e:
        print(f"\nAn error occurred: {e}")
        return None

if __name__ == "__main__":
    generate_structured_recipes()