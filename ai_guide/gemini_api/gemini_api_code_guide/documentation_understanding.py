"""
documentation_understanding.py

This script demonstrates how to process local DOCX files and use their
content as context for the Gemini API.

Key Learnings & Best Practices:
1.  **Handling Local DOCX Files**: The Gemini API cannot directly process .docx
    file formats. This script uses the `python-docx` library to extract the
    plain text content from the documents first.

2.  **Providing Multiple Documents as Context**: The script reads text from
    multiple files and passes them all within the same `contents` list to the
    API. This allows the model to compare and analyze information across
    different sources in a single request.

3.  **Context Length Limitations**: While this method works for a few small
    documents, sending many large files will exceed the model's context window
    limit. For large-scale document analysis, a Retrieval-Augmented Generation
    (RAG) system is the appropriate architecture.

4.  **File Path Handling**: Uses `os.path.join` to correctly construct file
    paths that work across different operating systems.
"""

import os
import docx
from dotenv import load_dotenv
import google.generativeai as genai

# --- Load Environment Variables & Configure SDK ---
load_dotenv()
API_KEY = os.environ.get("GEMINI_API_KEY")
if not API_KEY:
    raise ValueError("GEMINI_API_KEY not found in .env file or environment")
genai.configure(api_key=API_KEY)


def read_docx_text(file_path):
    """Extracts all text from a .docx file."""
    try:
        doc = docx.Document(file_path)
        full_text = [para.text for para in doc.paragraphs]
        return '\n'.join(full_text)
    except Exception as e:
        print(f"Error reading {file_path}: {e}")
        return None


def analyze_local_documents():
    """
    Reads two local .docx files, sends their content to the Gemini API,
    and asks for a comparison.
    """
    print("Starting local document analysis process...")
    try:
        # 1. Initialize the GenerativeModel
        model = genai.GenerativeModel(model_name="gemini-2.5-flash")

        # 2. Define the paths to the local documents
        # NOTE: This script can only handle .docx files, not the older .doc format.
        doc_paths = [
            os.path.join("原始文檔", "【編號1】批覆書_大企_信用.docx"),
            os.path.join("原始文檔", "【編號1】批覆書_大企_擔保.docx")
        ]

        # 3. Read the text content from each document
        document_contents = []
        for path in doc_paths:
            print(f"Reading content from: {path}")
            text = read_docx_text(path)
            if text:
                # We create a simple text part for each document's content
                document_contents.append({"text": f"--- Document: {os.path.basename(path)} ---\n{text}"})
            else:
                print(f"Could not read or found no content in {path}")
                return # Exit if a file can't be read

        # 4. Prepare the prompt for the API
        prompt = {
            "text": "\n\n--- Task ---\nPlease carefully read the two documents provided above ('信用' and '擔保'). Compare them and summarize the key differences and similarities between the two."
        }
        
        # The `contents` list includes the text from both documents and the final prompt.
        contents = document_contents + [prompt]

        # 5. Send the request and print the response
        print("\nSending content of both DOCX files to Gemini API...")
        response = model.generate_content(contents, request_options={'timeout': 180}) # 3 min timeout
        
        print("\n--- Gemini API Analysis ---")
        print(response.text)
        print("\n---------------------------\n")

    except Exception as e:
        print(f"\nAn unexpected error occurred: {e}")


if __name__ == "__main__":
    analyze_local_documents()
