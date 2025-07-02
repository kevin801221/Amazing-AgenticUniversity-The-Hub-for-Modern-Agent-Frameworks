# langgraph-bigtool

`langgraph-bigtool` is a Python library for creating [LangGraph](https://langchain-ai.github.io/langgraph/) agents that can access a large number of tools. It solves the common challenge of providing agents with vast toolsets without overwhelming the language model's context window or degrading its performance.

The core idea is to treat your toolset like a database and have the agent retrieve only the most relevant tools for a given task using Retrieval-Augmented Generation (RAG).

## 🎯 Why `langgraph-bigtool`?

Modern LLM agents often need to interact with a wide array of tools, from simple utilities to complex APIs. However, providing a large number of tools directly to an LLM in a single prompt can lead to several issues:

- **Context Window Limitation**: The total size of tool descriptions can easily exceed the model's context window.
- **Performance Degradation**: Even if the tools fit, a large number can confuse the model, leading to slower response times and less accurate tool selection.
- **Scalability Issues**: Manually managing which subset of tools to provide for different tasks is complex and doesn't scale.

`langgraph-bigtool` addresses these challenges by enabling an agent to dynamically search and select from a large "tool registry" stored in a vector database. This way, the agent only loads the most relevant tools into its context for any given step, making it more efficient and scalable.

## ✨ Features

- 🧰 **Scalable Access to Tools**: Equip agents with hundreds or thousands of tools without context limitations.
- 🔍 **Dynamic Tool Retrieval**: Uses semantic search to find the most relevant tools from a registry based on the user's query.
- 📝 **Persistent Tool Storage**: Leverages LangGraph's built-in [persistence layer](https://langchain-ai.github.io/langgraph/concepts/persistence/) to store and manage tool metadata. Supports backends like [in-memory](https://langchain-ai.github.io/langgraph/how-tos/cross-thread-persistence/) and [Postgres](https://langchain-ai.github.io/langgraph/reference/store/#langgraph.store.postgres.PostgresStore).
- 💡 **Customizable Retrieval Logic**: Easily define your own functions for tool retrieval, allowing for rule-based, categorical, or any other custom selection logic.
-  seamlessly **LangGraph Integration**: Built on [LangGraph](https://github.com/langchain-ai/langgraph), it inherits out-of-the-box support for [streaming](https://langchain-ai.github.io/langgraph/how-tos/#streaming), [memory](https://langchain-ai.github.io/langgraph/concepts/memory/), and [human-in-the-loop](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/) workflows.

## 🔧 How It Works

The library creates a `StateGraph` with a simple yet powerful loop. At its core, the agent is given a single tool: `retrieve_tools`.

1.  **Tool Retrieval**: The agent first calls `retrieve_tools` with a search query related to the task.
2.  **Tool Selection**: This tool searches the tool registry (e.g., a vector store) and returns the IDs of the most relevant tools.
3.  **State Update**: The graph adds the retrieved tools to the agent's state, making them available for the next step.
4.  **Tool Execution**: The agent can now see the selected tools and execute them to solve the task.
5.  **Loop**: The process can repeat, allowing the agent to search for different tools as the task evolves.

This entire process is encapsulated within the `create_agent` constructor.

![Graph diagram](static/img/graph.png)

## 🚀 Quickstart

First, install the necessary packages:

```bash
pip install langgraph-bigtool "langchain[openai]"
```

Set up your environment variables:
```bash
export OPENAI_API_KEY=<your_api_key>
```

This example equips an agent with all functions from Python's built-in `math` library (around 50 tools) to demonstrate how the agent can search for the right tool.

```python
import math
import types
import uuid

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langgraph.store.memory import InMemoryStore

from langgraph_bigtool import create_agent
from langgraph_bigtool.utils import convert_positional_only_function_to_tool

# 1. Collect tools
# Here, we'll use all functions from Python's built-in `math` library.
all_tools = []
for function_name in dir(math):
    function = getattr(math, function_name)
    if not isinstance(function, types.BuiltinFunctionType):
        continue
    # This utility handles an idiosyncrasy of the `math` library's functions
    if tool := convert_positional_only_function_to_tool(function):
        all_tools.append(tool)

# 2. Create a tool registry
# This is a dictionary mapping unique IDs to tool instances.
tool_registry = {f"tool_{i}": tool for i, tool in enumerate(all_tools)}

# 3. Index tool metadata in a LangGraph Store
# We use a simple in-memory store with a vector index for semantic search.
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
store = InMemoryStore(
    index={
        "embed": embeddings,
        "dims": 1536,
        "fields": ["description"],
    }
)
# Add tool descriptions to the store
for tool_id, tool in tool_registry.items():
    store.put(
        ("tools",),  # Namespace
        tool_id,
        {"description": f"{tool.name}: {tool.description}"},
    )

# 4. Initialize and compile the agent
llm = ChatOpenAI(model="gpt-4o-mini")
builder = create_agent(llm, tool_registry)
agent = builder.compile(store=store)

# 5. Run the agent
query = "What is the arc cosine of 0.5?"
for step in agent.stream({"messages": query}, stream_mode="updates"):
    for _, update in step.items():
        for message in update.get("messages", []):
            message.pretty_print()
```

The output shows the agent first calling `retrieve_tools` to find relevant tools, then calling the `acos` tool to get the final answer.

```
================================== Ai Message ==================================
Tool Calls:
  retrieve_tools (call_...)
 Call ID: call_...
  Args:
    query: arc cosine of 0.5
================================= Tool Message =================================
Available tools: ['acos', 'acosh']
================================== Ai Message ==================================
Tool Calls:
  acos (call_...)
 Call ID: call_...
  Args:
    x: 0.5
================================= Tool Message =================================
Name: acos

1.0471975511965976
================================== Ai Message ==================================
The arc cosine of 0.5 is approximately 1.0472.
```

## 🛠️ Advanced Usage

### Customizing Tool Retrieval

You can override the default semantic search behavior by passing a custom function to `create_agent`. This function is responsible for returning a list of tool IDs from the registry.

#### Example: Custom Search Logic

```python
from langgraph.prebuilt import InjectedStore
from langgraph.store.base import BaseStore
from typing_extensions import Annotated

def my_custom_retriever(
    query: str,
    # You can add other custom arguments here
    *,
    store: Annotated[BaseStore, InjectedStore],
) -> list[str]:
    """A custom function to retrieve tools based on a query."""
    # Simple semantic search with a hardcoded limit
    results = store.search(("tools",), query=query, limit=2)
    tool_ids = [result.key for result in results]
    
    # Add your own custom logic here, e.g., filtering, re-ranking, etc.
    print(f"Retrieved tools: {tool_ids}")
    
    return tool_ids

# Create the agent with the custom retriever
builder = create_agent(
    llm, tool_registry, retrieve_tools_function=my_custom_retriever
)
agent = builder.compile(store=store)
```

#### Example: Categorical (Non-Semantic) Retrieval

Your retrieval logic doesn't have to use semantic search at all. You can implement any logic, such as retrieving tools based on categories.

```python
from typing import Literal

# A simple tool registry
tool_registry = {
    "billing_id_1": get_balance,
    "billing_id_2": get_transaction_history,
    "support_id_1": create_support_ticket,
}

def retrieve_tools_by_category(
    category: Literal["billing", "support"],
) -> list[str]:
    """Get all tools for a specific category."""
    if category == "billing":
        return ["billing_id_1", "billing_id_2"]
    else:
        return ["support_id_1"]

# The LLM will infer the 'category' argument from the function's type hints.
builder = create_agent(
    llm, tool_registry, retrieve_tools_function=retrieve_tools_by_category
)
agent = builder.compile()
```

> [!TIP]
> By type-hinting the function argument as a `Literal`, you signal to the LLM that it should provide a categorical value, making the tool selection more structured.

## 🤝 Contributing

Contributions are welcome! This project uses `ruff` for linting and formatting, and `pytest` for testing.

To set up your development environment:
1.  Install dependencies, including test tools:
    ```bash
    uv sync --group test
    ```
2.  Run linters and formatters using the Makefile:
    ```bash
    make format
    make lint
    ```
3.  Run tests:
    ```bash
    make test
    ```

Please feel free to open an issue or submit a pull request.

## 📚 Related Work

- [Toolshed: Scale Tool-Equipped Agents with Advanced RAG-Tool Fusion and Tool Knowledge Bases](https://doi.org/10.48550/arXiv.2410.14594)
- [Graph RAG-Tool Fusion](https://doi.org/10.48550/arXiv.2502.07223)
- [LLM-Tool-Survey](https://github.com/quchangle1/LLM-Tool-Survey)
- [Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models](https://doi.org/10.48550/arXiv.2503.01763)