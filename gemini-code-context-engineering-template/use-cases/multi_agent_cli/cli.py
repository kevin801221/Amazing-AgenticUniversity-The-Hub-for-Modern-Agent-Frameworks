import sys
import argparse
from multi_agent_cli.research_agent import research_agent

def main():
    """
    Main function to run the CLI for the multi-agent system.
    """
    parser = argparse.ArgumentParser(
        description="A CLI to interact with a research agent that can also draft emails."
    )
    parser.add_argument(
        "instruction",
        type=str,
        nargs='+',
        help="The instruction for the research agent. E.g., 'Research the weather in SF and draft an email to bob@example.com'",
    )

    args = parser.parse_args()
    
    # Join the list of instruction words into a single string.
    full_instruction = " ".join(args.instruction)

    print(f"Executing instruction: {full_instruction}\n")

    # Run the main research agent
    # We are using a streaming response to see the agent's thought process.
    response_generator = research_agent.run(full_instruction)

    final_output = ""
    for chunk in response_generator:
        # The chunk can be a string or a data structure depending on the stream content.
        # For simplicity, we print its string representation.
        print(chunk, end="", flush=True)
        if isinstance(chunk, str):
            final_output += chunk
    
    print("\n\n--- Execution Finished ---")
    # The final consolidated output might be useful if you need to process it further.
    # print(f"Final consolidated output:\n{final_output}")


if __name__ == "__main__":
    # To run from the command line:
    # python multi_agent_cli/cli.py "Your full instruction here"
    main()
