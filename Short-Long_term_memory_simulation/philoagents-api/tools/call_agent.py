import asyncio
from functools import wraps

import click

from philoagents.application.conversation_service.generate_response import (
    get_streaming_response,
)
from philoagents.domain.philosopher_factory import PhilosopherFactory


def async_command(f):
    """Decorator to run an async click command."""

    @wraps(f)
    def wrapper(*args, **kwargs):
        return asyncio.run(f(*args, **kwargs))

    return wrapper


@click.command()
@click.option(
    "--philosopher-id",
    type=str,
    required=True,
    help="ID of the philosopher to call.",
)
@click.option(
    "--query",
    type=str,
    required=True,
    help="Query to call the agent with.",
)
@async_command
async def main(philosopher_id: str, query: str) -> None:
    """CLI command to query a philosopher.

    Args:
        philosopher_id: ID of the philosopher to call.
        query: Query to call the agent with.
    """

    philosopher_factory = PhilosopherFactory()
    philosopher = philosopher_factory.get_philosopher(philosopher_id)

    print(
        f"\033[32mCalling agent with philosopher_id: `{philosopher_id}` and query: `{query}`\033[0m"
    )
    print("\033[32mResponse:\033[0m")
    print("\033[32m--------------------------------\033[0m")
    async for chunk in get_streaming_response(
        messages=query,
        philosopher_id=philosopher_id,
        philosopher_name=philosopher.name,
        philosopher_perspective=philosopher.perspective,
        philosopher_style=philosopher.style,
        philosopher_context="",
    ):
        print(f"\033[32m{chunk}\033[0m", end="", flush=True)
    print("\033[32m--------------------------------\033[0m")


if __name__ == "__main__":
    main()
