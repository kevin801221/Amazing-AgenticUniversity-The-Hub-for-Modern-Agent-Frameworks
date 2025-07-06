import inspect
import math
import types
import uuid
from typing import Callable
from unittest.mock import patch

import pytest
from langchain_core.embeddings import Embeddings
from langchain_core.embeddings.fake import DeterministicFakeEmbedding
from langchain_core.language_models import GenericFakeChatModel, LanguageModelLike
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import BaseTool
from langgraph.prebuilt import InjectedStore
from langgraph.store.base import BaseStore
from langgraph.store.memory import InMemoryStore
from typing_extensions import Annotated

from langgraph_bigtool import create_agent
from langgraph_bigtool.graph import State
from langgraph_bigtool.utils import convert_positional_only_function_to_tool

EMBEDDING_SIZE = 1536


# Create a list of all the functions in the math module
all_names = dir(math)

math_functions = [
    getattr(math, name)
    for name in all_names
    if isinstance(getattr(math, name), types.BuiltinFunctionType)
]

# Convert to tools, handling positional-only arguments (idiosyncrasy of math module)
all_tools = []
for function in math_functions:
    if wrapper := convert_positional_only_function_to_tool(function):
        all_tools.append(wrapper)

# Store tool objects in registry
tool_registry = {str(uuid.uuid4()): tool for tool in all_tools}


class FakeModel(GenericFakeChatModel):
    def bind_tools(self, *args, **kwargs) -> "FakeModel":
        """Do nothing for now."""
        return self


def _get_fake_llm_and_embeddings(retriever_tool_name: str = "retrieve_tools"):
    fake_embeddings = DeterministicFakeEmbedding(size=EMBEDDING_SIZE)

    acos_tool = next(tool for tool in tool_registry.values() if tool.name == "acos")
    initial_query = (
        f"{acos_tool.name}: {acos_tool.description}"  # make same as embedding
    )
    fake_llm = FakeModel(
        messages=iter(
            [
                AIMessage(
                    "",
                    tool_calls=[
                        {
                            "name": retriever_tool_name,
                            "args": {"query": initial_query},
                            "id": "abc123",
                            "type": "tool_call",
                        }
                    ],
                ),
                AIMessage(
                    "",
                    tool_calls=[
                        {
                            "name": "acos",
                            "args": {"x": 0.5},
                            "id": "abc234",
                            "type": "tool_call",
                        }
                    ],
                ),
                AIMessage("The arc cosine of 0.5 is approximately 1.047 radians."),
            ]
        )
    )

    return fake_llm, fake_embeddings


def _validate_result(result: State, tool_registry=tool_registry) -> None:
    assert set(result.keys()) == {"messages", "selected_tool_ids"}
    selected = []
    for tool_id in result["selected_tool_ids"]:
        if isinstance(tool_registry[tool_id], BaseTool):
            selected.append(tool_registry[tool_id].name)
        else:
            selected.append(tool_registry[tool_id].__name__)
    assert "acos" in selected
    assert set(message.type for message in result["messages"]) == {
        "human",
        "ai",
        "tool",
    }
    tool_calls = [
        tool_call
        for message in result["messages"]
        if isinstance(message, AIMessage)
        for tool_call in message.tool_calls
    ]
    assert tool_calls
    tool_call_names = [tool_call["name"] for tool_call in tool_calls]
    assert "retrieve_tools" in tool_call_names
    math_tool_calls = [
        tool_call for tool_call in tool_calls if tool_call["name"] == "acos"
    ]
    assert len(math_tool_calls) == 1
    math_tool_call = math_tool_calls[0]
    tool_messages = [
        message
        for message in result["messages"]
        if isinstance(message, ToolMessage)
        and message.tool_call_id == math_tool_call["id"]
    ]
    assert len(tool_messages) == 1
    tool_message = tool_messages[0]
    assert round(float(tool_message.content), 4) == 1.0472
    reply = result["messages"][-1]
    assert isinstance(reply, AIMessage)
    assert not reply.tool_calls
    assert reply.content


def run_end_to_end_test(
    llm: LanguageModelLike,
    embeddings: Embeddings,
    retrieve_tools_function: Callable | None = None,
    retrieve_tools_coroutine: Callable | None = None,
) -> None:
    # Store tool descriptions in store
    store = InMemoryStore(
        index={
            "embed": embeddings,
            "dims": EMBEDDING_SIZE,
            "fields": ["description"],
        }
    )
    for tool_id, tool in tool_registry.items():
        store.put(
            ("tools",),
            tool_id,
            {
                "description": f"{tool.name}: {tool.description}",
            },
        )

    builder = create_agent(
        llm,
        tool_registry,
        retrieve_tools_function=retrieve_tools_function,
        retrieve_tools_coroutine=retrieve_tools_coroutine,
    )
    agent = builder.compile(store=store)

    result = agent.invoke(
        {"messages": "Use available tools to calculate arc cosine of 0.5."}
    )
    _validate_result(result)


async def run_end_to_end_test_async(
    llm: LanguageModelLike,
    embeddings: Embeddings,
    retrieve_tools_function: Callable | None = None,
    retrieve_tools_coroutine: Callable | None = None,
) -> None:
    # Store tool descriptions in store
    store = InMemoryStore(
        index={
            "embed": embeddings,
            "dims": EMBEDDING_SIZE,
            "fields": ["description"],
        }
    )
    for tool_id, tool in tool_registry.items():
        await store.aput(
            ("tools",),
            tool_id,
            {
                "description": f"{tool.name}: {tool.description}",
            },
        )

    builder = create_agent(
        llm,
        tool_registry,
        retrieve_tools_function=retrieve_tools_function,
        retrieve_tools_coroutine=retrieve_tools_coroutine,
    )
    agent = builder.compile(store=store)

    result = await agent.ainvoke(
        {"messages": "Use available tools to calculate arc cosine of 0.5."}
    )
    _validate_result(result)


class CustomError(Exception):
    pass


def custom_retrieve_tools_store(
    query: str,
    *,
    store: Annotated[BaseStore, InjectedStore],
) -> list[str]:
    """Custom retrieve tools."""
    raise CustomError


async def acustom_retrieve_tools_store(
    query: str,
    *,
    store: Annotated[BaseStore, InjectedStore],
) -> list[str]:
    """Custom retrieve tools."""
    raise CustomError


def custom_retrieve_tools_no_store(query: str) -> list[str]:
    """Custom retrieve tools."""
    raise CustomError


async def acustom_retrieve_tools_no_store(query: str) -> list[str]:
    """Custom retrieve tools."""
    raise CustomError


@pytest.mark.parametrize(
    "custom_retrieve_tools, acustom_retrieve_tools",
    [
        (custom_retrieve_tools_store, acustom_retrieve_tools_store),
        (custom_retrieve_tools_no_store, acustom_retrieve_tools_no_store),
    ],
)
def test_end_to_end(custom_retrieve_tools, acustom_retrieve_tools) -> None:
    retriever_tool_name = custom_retrieve_tools.__name__
    retriever_tool_name_async = acustom_retrieve_tools.__name__
    # Default
    fake_llm, fake_embeddings = _get_fake_llm_and_embeddings()
    run_end_to_end_test(fake_llm, fake_embeddings)

    # Custom
    fake_llm, fake_embeddings = _get_fake_llm_and_embeddings(
        retriever_tool_name=retriever_tool_name_async
    )
    with pytest.raises(TypeError):
        # No sync function provided
        run_end_to_end_test(
            fake_llm,
            fake_embeddings,
            retrieve_tools_coroutine=acustom_retrieve_tools,
        )

    fake_llm, fake_embeddings = _get_fake_llm_and_embeddings(
        retriever_tool_name=retriever_tool_name
    )
    with pytest.raises(CustomError):
        # Calls custom sync function
        run_end_to_end_test(
            fake_llm,
            fake_embeddings,
            retrieve_tools_function=custom_retrieve_tools,
            retrieve_tools_coroutine=acustom_retrieve_tools,
        )

    fake_llm, fake_embeddings = _get_fake_llm_and_embeddings(
        retriever_tool_name=retriever_tool_name
    )
    with pytest.raises(CustomError):
        # Calls custom sync function
        run_end_to_end_test(
            fake_llm,
            fake_embeddings,
            retrieve_tools_function=custom_retrieve_tools,
        )


@pytest.mark.parametrize(
    "custom_retrieve_tools, acustom_retrieve_tools",
    [
        (custom_retrieve_tools_store, acustom_retrieve_tools_store),
        (custom_retrieve_tools_no_store, acustom_retrieve_tools_no_store),
    ],
)
async def test_end_to_end_async(custom_retrieve_tools, acustom_retrieve_tools) -> None:
    retriever_tool_name = custom_retrieve_tools.__name__
    retriever_tool_name_async = acustom_retrieve_tools.__name__
    # Default
    fake_llm, fake_embeddings = _get_fake_llm_and_embeddings()
    await run_end_to_end_test_async(fake_llm, fake_embeddings)

    # Custom
    fake_llm, fake_embeddings = _get_fake_llm_and_embeddings(
        retriever_tool_name=retriever_tool_name
    )
    with pytest.raises(CustomError):
        # Calls custom sync function
        await run_end_to_end_test_async(
            fake_llm,
            fake_embeddings,
            retrieve_tools_function=custom_retrieve_tools,
        )

    fake_llm, fake_embeddings = _get_fake_llm_and_embeddings(
        retriever_tool_name=retriever_tool_name
    )
    with pytest.raises(CustomError):
        # Calls custom sync function
        await run_end_to_end_test_async(
            fake_llm,
            fake_embeddings,
            retrieve_tools_function=custom_retrieve_tools,
            retrieve_tools_coroutine=acustom_retrieve_tools,
        )

    fake_llm, fake_embeddings = _get_fake_llm_and_embeddings(
        retriever_tool_name=retriever_tool_name_async
    )
    with pytest.raises(CustomError):
        # Calls custom sync function
        await run_end_to_end_test_async(
            fake_llm,
            fake_embeddings,
            retrieve_tools_coroutine=acustom_retrieve_tools,
        )


def test_duplicate_tools() -> None:
    fake_embeddings = DeterministicFakeEmbedding(size=EMBEDDING_SIZE)

    acos_tool = next(tool for tool in tool_registry.values() if tool.name == "acos")
    initial_query = (
        f"{acos_tool.name}: {acos_tool.description}"  # make same as embedding
    )

    fake_llm = FakeModel(
        messages=iter(
            [
                AIMessage(
                    "",
                    tool_calls=[
                        {
                            "name": "retrieve_tools",
                            "args": {"query": initial_query},
                            "id": "abc123",
                            "type": "tool_call",
                        }
                    ],
                ),
                AIMessage(
                    "",
                    tool_calls=[
                        {
                            "name": "acos",
                            "args": {"x": 0.5},
                            "id": "abc234",
                            "type": "tool_call",
                        }
                    ],
                ),
                AIMessage(
                    "",
                    tool_calls=[
                        {
                            "name": "retrieve_tools",
                            "args": {"query": "another tool"},
                            "id": "abc345",
                            "type": "tool_call",
                        },
                        # Retrieval can return the same tool multiple times. Force this
                        # by adding the same tool call twice.
                        {
                            "name": "retrieve_tools",
                            "args": {"query": initial_query},
                            "id": "abc456",
                            "type": "tool_call",
                        },
                    ],
                ),
                AIMessage("The arc cosine of 0.5 is approximately 1.047 radians."),
            ]
        )
    )
    with patch.object(
        FakeModel, "bind_tools", wraps=fake_llm.bind_tools
    ) as mock_bind_tools:
        run_end_to_end_test(fake_llm, fake_embeddings)
        mock_bind_tools.assert_called()
        for args, _ in mock_bind_tools.call_args_list:
            tool_names = [tool.name for tool in args[0] if isinstance(tool, BaseTool)]
            assert len(tool_names) == len(set(tool_names))


def test_functions_in_registry() -> None:
    tool_registry = {str(uuid.uuid4()): tool.func for tool in all_tools}
    fake_embeddings = DeterministicFakeEmbedding(size=EMBEDDING_SIZE)

    acos_tool = next(tool for tool in tool_registry.values() if tool.__name__ == "acos")
    initial_query = (
        f"{acos_tool.__name__}: {inspect.getdoc(acos_tool)}"  # make same as embedding
    )
    fake_llm = FakeModel(
        messages=iter(
            [
                AIMessage(
                    "",
                    tool_calls=[
                        {
                            "name": "retrieve_tools",
                            "args": {"query": initial_query},
                            "id": "abc123",
                            "type": "tool_call",
                        }
                    ],
                ),
                AIMessage(
                    "",
                    tool_calls=[
                        {
                            "name": "acos",
                            "args": {"x": 0.5},
                            "id": "abc234",
                            "type": "tool_call",
                        }
                    ],
                ),
                AIMessage("The arc cosine of 0.5 is approximately 1.047 radians."),
            ]
        )
    )
    store = InMemoryStore(
        index={
            "embed": fake_embeddings,
            "dims": EMBEDDING_SIZE,
            "fields": ["description"],
        }
    )
    for tool_id, tool in tool_registry.items():
        store.put(
            ("tools",),
            tool_id,
            {
                "description": f"{tool.__name__}: {inspect.getdoc(tool)}",
            },
        )

    builder = create_agent(
        fake_llm,
        tool_registry,
    )
    agent = builder.compile(store=store)

    result = agent.invoke(
        {"messages": "Use available tools to calculate arc cosine of 0.5."}
    )
    _validate_result(result, tool_registry=tool_registry)
