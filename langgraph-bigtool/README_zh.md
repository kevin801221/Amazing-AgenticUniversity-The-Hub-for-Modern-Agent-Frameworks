# langgraph-bigtool

`langgraph-bigtool` 是一個 Python 函式庫，專為建立能夠存取大量工具的 [LangGraph](https://langchain-ai.github.io/langgraph/) Agent 而設計。它解決了一個常見的挑戰：如何在不超出大型語言模型 (LLM) 的上下文視窗或影響其性能的前提下，為 Agent 提供龐大的工具集。

其核心思想是將您的工具集視為一個資料庫，並讓 Agent 使用「檢索增強生成 (RAG)」技術，僅檢索與當前任務最相關的工具。

## 🎯 為什麼選擇 `langgraph-bigtool`？

現代的 LLM Agent 經常需要與各種工具互動，從簡單的實用程式到複雜的 API。然而，在單個提示中直接向 LLM 提供大量工具會導致幾個問題：

- **上下文視窗限制**：所有工具描述的總長度很容易超過模型的上下文視窗限制。
- **性能下降**：即使工具描述能放入上下文，大量的工具也可能使模型感到困惑，導致回應時間變慢且工具選擇不準確。
- **擴展性問題**：為不同任務手動管理要提供哪些工具子集非常複雜，且難以擴展。

`langgraph-bigtool` 透過讓 Agent 從儲存在向量資料庫中的大型「工具註冊表」中動態搜尋和選擇工具，來解決這些挑戰。如此一來，Agent 在任何給定步驟中，只會將最相關的工具載入其上下文中，使其更有效率且更具擴展性。

## ✨ 功能特性

- 🧰 **可擴展的工具存取**：讓 Agent 能夠使用數百甚至數千個工具，而不受上下文視窗的限制。
- 🔍 **動態工具檢索**：根據使用者查詢，使用語意搜尋從工具註冊表中找到最相關的工具。
- 📝 **持久化工具儲存**：利用 LangGraph 內建的[持久化層](https://langchain-ai.github.io/langgraph/concepts/persistence/)來儲存和管理工具元數據。支援 [in-memory](https://langchain-ai.github.io/langgraph/how-tos/cross-thread-persistence/) 和 [Postgres](https://langchain-ai.github.io/langgraph/reference/store/#langgraph.store.postgres.PostgresStore) 等後端。
- 💡 **可自訂的檢索邏輯**：輕鬆定義您自己的工具檢索函式，允許基於規則、分類或任何其他自訂選擇邏輯。
-  **無縫整合 LangGraph**：建立在 [LangGraph](https://github.com/langchain-ai/langgraph) 之上，它繼承了對[串流](https://langchain-ai.github.io/langgraph/how-tos/#streaming)、[記憶體](https://langchain-ai.github.io/langgraph/concepts/memory/)和[人在迴路](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/)工作流程的開箱即用支援。

## 🔧 運作原理

該函式庫建立了一個具有簡單而強大迴圈的 `StateGraph`。其核心是為 Agent 提供一個單一工具：`retrieve_tools`。

1.  **工具檢索**：Agent 首先使用與任務相關的搜尋查詢呼叫 `retrieve_tools`。
2.  **工具選擇**：此工具搜尋工具註冊表（例如，向量儲存），並返回最相關工具的 ID。
3.  **狀態更新**：圖將檢索到的工具新增至 Agent 的狀態中，使其在下一步中可用。
4.  **工具執行**：Agent 現在可以看到所選工具並執行它們以解決任務。
5.  **迴圈**：此過程可以重複，允許 Agent 隨著任務的演變搜尋不同的工具。

整個過程都封裝在 `create_agent` 建構函式中。

![Graph diagram](static/img/graph.png)

## 🚀 快速入門

首先，安裝必要的套件：

```bash
pip install langgraph-bigtool "langchain[openai]"
```

設定您的環境變數：
```bash
export OPENAI_API_KEY=<your_api_key>
```

此範例為 Agent 配備了 Python 內建 `math` 函式庫中的所有函式（約 50 個工具），以展示 Agent 如何搜尋正確的工具。

```python
import math
import types
import uuid

from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langgraph.store.memory import InMemoryStore

from langgraph_bigtool import create_agent
from langgraph_bigtool.utils import convert_positional_only_function_to_tool

# 1. 收集工具
# 在這裡，我們將使用 Python 內建 `math` 函式庫中的所有函式。
all_tools = []
for function_name in dir(math):
    function = getattr(math, function_name)
    if not isinstance(function, types.BuiltinFunctionType):
        continue
    # 此實用程式處理 `math` 函式庫函式的一個特性
    if tool := convert_positional_only_function_to_tool(function):
        all_tools.append(tool)

# 2. 建立工具註冊表
# 這是一個將唯一 ID 對應到工具實例的字典。
tool_registry = {f"tool_{i}": tool for i, tool in enumerate(all_tools)}

# 3. 在 LangGraph Store 中索引工具元數據
# 我們使用一個簡單的記憶體內儲存，並帶有向量索引以進行語意搜尋。
embeddings = OpenAIEmbeddings(model="text-embedding-3-small")
store = InMemoryStore(
    index={
        "embed": embeddings,
        "dims": 1536,
        "fields": ["description"],
    }
)
# 將工具描述新增至儲存中
for tool_id, tool in tool_registry.items():
    store.put(
        ("tools",),  # 命名空間
        tool_id,
        {"description": f"{tool.name}: {tool.description}"},
    )

# 4. 初始化並編譯 Agent
llm = ChatOpenAI(model="gpt-4o-mini")
builder = create_agent(llm, tool_registry)
agent = builder.compile(store=store)

# 5. 執行 Agent
query = "0.5 的反餘弦值是多少？"
for step in agent.stream({"messages": query}, stream_mode="updates"):
    for _, update in step.items():
        for message in update.get("messages", []):
            message.pretty_print()
```

輸出顯示 Agent 首先呼叫 `retrieve_tools` 來尋找相關工具，然後呼叫 `acos` 工具以取得最終答案。

```
================================== Ai Message ==================================
Tool Calls:
  retrieve_tools (call_...)
 Call ID: call_...
  Args:
    query: 0.5 的反餘弦值
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
0.5 的反餘弦值約為 1.0472。
```

## 🛠️ 進階用法

### 自訂工具檢索

您可以透過將自訂函式傳遞給 `create_agent` 來覆寫預設的語意搜尋行為。此函式負責從註冊表中返回工具 ID 列表。

#### 範例：自訂搜尋邏輯

```python
from langgraph.prebuilt import InjectedStore
from langgraph.store.base import BaseStore
from typing_extensions import Annotated

def my_custom_retriever(
    query: str,
    # 您可以在此處新增其他自訂參數
    *,
    store: Annotated[BaseStore, InjectedStore],
) -> list[str]:
    """一個根據查詢檢索工具的自訂函式。"""
    # 使用硬式編碼限制的簡單語意搜尋
    results = store.search(("tools",), query=query, limit=2)
    tool_ids = [result.key for result in results]
    
    # 在此處新增您自己的自訂邏輯，例如過濾、重新排序等。
    print(f"檢索到的工具：{tool_ids}")
    
    return tool_ids

# 使用自訂檢索器建立 Agent
builder = create_agent(
    llm, tool_registry, retrieve_tools_function=my_custom_retriever
)
agent = builder.compile(store=store)
```

#### 範例：分類（非語意）檢索

您的檢索邏輯完全不必使用語意搜尋。您可以實現任何邏輯，例如根據類別檢索工具。

```python
from typing import Literal

# 一個簡單的工具註冊表
tool_registry = {
    "billing_id_1": get_balance,
    "billing_id_2": get_transaction_history,
    "support_id_1": create_support_ticket,
}

def retrieve_tools_by_category(
    category: Literal["billing", "support"],
) -> list[str]:
    """取得特定類別的所有工具。"""
    if category == "billing":
        return ["billing_id_1", "billing_id_2"]
    else:
        return ["support_id_1"]

# LLM 將從函式的型別提示中推斷出 'category' 參數。
builder = create_agent(
    llm, tool_registry, retrieve_tools_function=retrieve_tools_by_category
)
agent = builder.compile()
```

> [!TIP]
> 透過將函式參數的型別提示為 `Literal`，您可以向 LLM 發出信號，表示它應該提供一個分類值，從而使工具選擇更加結構化。

## 🤝 貢獻

歡迎貢獻！此專案使用 `ruff` 進行程式碼檢查和格式化，並使用 `pytest` 進行測試。

若要設定您的開發環境：
1.  安裝相依性，包括測試工具：
    ```bash
    uv sync --group test
    ```
2.  使用 Makefile 執行程式碼檢查和格式化：
    ```bash
    make format
    make lint
    ```
3.  執行測試：
    ```bash
    make test
    ```

歡迎隨時提出問題或提交拉取請求。

## 📚 相關研究

- [Toolshed: Scale Tool-Equipped Agents with Advanced RAG-Tool Fusion and Tool Knowledge Bases](https://doi.org/10.48550/arXiv.2410.14594)
- [Graph RAG-Tool Fusion](https://doi.org/10.48550/arXiv.2502.07223)
- [LLM-Tool-Survey](https://github.com/quchangle1/LLM-Tool-Survey)
- [Retrieval Models Aren't Tool-Savvy: Benchmarking Tool Retrieval for Large Language Models](https://doi.org/10.48550/arXiv.2503.01763)
