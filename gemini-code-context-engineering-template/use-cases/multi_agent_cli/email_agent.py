from pydantic_ai import Agent
from pydantic_ai.models import Gemini
from multi_agent_cli.gmail_tools import get_gmail_service, create_gmail_draft

# Get the Gmail service once
# Note: This will trigger the OAuth flow on the first run if token.json is not present.
gmail_service = get_gmail_service()

# Create a wrapper for the tool so the agent doesn't need to handle the 'service' object.
def draft_email_tool(to: str, subject: str, body: str) -> str:
    """
    A tool to create a draft email in Gmail.

    Args:
        to: The recipient's email address.
        subject: The subject of the email.
        body: The content of the email.

    Returns:
        A confirmation message indicating success or failure.
    """
    if not gmail_service:
        return "Gmail service is not available. Please check your credentials."
    return create_gmail_draft(gmail_service, to, subject, body)

# Define the email agent
email_agent = Agent(
    model=Gemini(
        "gemini-1.5-pro",
        # Add your Google API Key for the AI model here if needed,
        # separate from the Gmail OAuth credentials.
        # api_key="YOUR_GEMINI_API_KEY"
    ),
    system_prompt="You are an assistant that helps draft emails. Use the provided tool to create drafts in the user's Gmail account.",
    tools=[draft_email_tool],
)

if __name__ == '__main__':
    # This is for testing the email agent directly
    # Ensure your credentials.json is set up.
    print("Testing the email agent...")
    result = email_agent.run_sync(
        "Draft an email to 'friend@example.com' with the subject 'Hello from the Agent' and the body 'This is a test message sent from the Pydantic AI email agent.'"
    )
    print("Agent Result:")
    print(result)
