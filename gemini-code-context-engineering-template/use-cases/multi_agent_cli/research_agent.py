from pydantic_ai import Agent
from pydantic_ai.models import Gemini
from multi_agent_cli.research_tools import brave_search
from multi_agent_cli.email_agent import email_agent

# This is the tool that the main research agent will use.
# When this tool is called, it will in turn run the email_agent.
def draft_email_via_sub_agent(to: str, subject: str, body: str) -> str:
    """
    A tool to delegate the task of drafting an email to a specialized sub-agent.
    
    Args:
        to: The recipient's email address.
        subject: The subject of the email.
        body: The content of the email.

    Returns:
        The result from the email sub-agent.
    """
    print("\n--- Delegating to Email Agent ---\n")
    # The actual instruction passed to the sub-agent.
    instruction = f"Draft an email to '{to}' with the subject '{subject}' and the following body:\n\n{body}"
    
    # Run the email agent to perform the task
    result = email_agent.run_sync(instruction)
    
    # The output of the sub-agent's run is returned as the result of this tool.
    # The main agent will see this confirmation message.
    return str(result.output)


# Define the main research agent
research_agent = Agent(
    model=Gemini(
        "gemini-1.5-pro",
        # Add your Google API Key for the AI model here if needed.
        # api_key="YOUR_GEMINI_API_KEY"
    ),
    system_prompt=(
        "You are a research assistant. Your goal is to use the search tool to find information, "
        "and then use the email drafting tool to compose a message with the findings. "
        "First, perform the research. Then, analyze the research results to create a comprehensive body for the email. "
        "Finally, call the draft_email_via_sub_agent tool with all the necessary information (recipient, subject, and the composed body)."
    ),
    tools=[
        brave_search,
        draft_email_via_sub_agent,
    ],
    # Enable streaming to see the agent's thought process
    stream_response=True, 
)

if __name__ == '__main__':
    # This is for testing the research agent directly
    # Ensure all your credentials (.env, credentials.json) are set up.
    print("Testing the main research agent...")
    
    # The agent should first call brave_search, then draft_email_via_sub_agent
    test_instruction = "Research the main features of the new Apple M4 chip and then draft an email to 'tech.team@example.com' with the subject 'Apple M4 Chip Briefing' summarizing the findings."
    
    response = research_agent.run_sync(test_instruction)

    print("\n--- Final Response from Research Agent ---")
    # The final output will likely be the confirmation from the email agent.
    print(response.output)
