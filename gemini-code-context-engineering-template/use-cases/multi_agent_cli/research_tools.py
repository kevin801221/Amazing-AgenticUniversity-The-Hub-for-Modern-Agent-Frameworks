import os
from dotenv import load_dotenv
from brave import Brave

# Load environment variables from .env file
load_dotenv()

# Get the Brave API key from environment variables
BRAVE_API_KEY = os.getenv("BRAVE_API_KEY")

def brave_search(query: str) -> str:
    """
    Performs a web search using the Brave Search API.

    Args:
        query: The search query.

    Returns:
        A formatted string containing the search results, or an error message.
    """
    if not BRAVE_API_KEY:
        return "Brave API key is not set. Please add it to your .env file."

    try:
        brave = Brave(BRAVE_API_KEY)
        search_results = brave.search(q=query, count=5) # Get top 5 results

        if not search_results.web or not search_results.web.results:
            return "No search results found."

        # Format the results into a readable string
        formatted_results = f"Search results for '{query}':\n\n"
        for i, result in enumerate(search_results.web.results, 1):
            formatted_results += f"{i}. {result.title}\n"
            formatted_results += f"   URL: {result.url}\n"
            formatted_results += f"   Snippet: {result.description}\n\n"
        
        return formatted_results

    except Exception as e:
        return f"An error occurred during the Brave search: {e}"

if __name__ == '__main__':
    # This is for testing the brave_search tool directly
    # Make sure you have your BRAVE_API_KEY in a .env file.
    print("Testing the Brave search tool...")
    test_query = "What is Pydantic AI?"
    results = brave_search(test_query)
    print(results)

