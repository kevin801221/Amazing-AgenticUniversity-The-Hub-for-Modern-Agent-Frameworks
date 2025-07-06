# LangGraph 持久化機制詳解

## 概述

LangGraph 內建了強大的持久化層，透過檢查點（checkpointer）實現。當您使用檢查點編譯圖形時，檢查點會在每個超級步驟（super-step）中保存圖形狀態的快照。這些檢查點會保存到線程（thread）中，可以在圖形執行後訪問。正是因為線程允許在執行後訪問圖形狀態，才使得**人機互動**、**記憶功能**、**時間旅行**和**容錯性**等強大功能成為可能。

> 💡 **LangGraph API 自動處理檢查點**
> 
> 使用 LangGraph API 時，您不需要手動實現或配置檢查點。API 會在幕後為您處理所有持久化基礎設施。

## 核心概念

### 1. 線程（Threads）

**線程是什麼？**
- 線程是分配給檢查點保存器保存的每個檢查點的唯一 ID 或線程識別符
- 它包含一系列運行的累積狀態
- 當執行運行時，助手底層圖形的狀態會持久化到線程中

**如何使用線程？**
```python
# 調用圖形時必須指定 thread_id
config = {"configurable": {"thread_id": "1"}}
```

線程的當前和歷史狀態都可以檢索。要持久化狀態，必須在執行運行之前創建線程。

### 2. 檢查點（Checkpoints）

**檢查點的定義**
檢查點是線程在特定時間點的狀態快照，在每個超級步驟中保存圖形狀態。檢查點由 `StateSnapshot` 對象表示，具有以下關鍵屬性：

- **config**: 與此檢查點相關的配置
- **metadata**: 與此檢查點相關的元數據
- **values**: 此時間點狀態通道的值
- **next**: 要在圖形中執行的下一個節點名稱的元組
- **tasks**: 包含下一個要執行任務信息的 `PregelTask` 對象元組

## 實際範例：理解檢查點的工作原理

讓我們通過一個簡單的圖形來理解檢查點是如何工作的：

```python
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import InMemorySaver
from typing import Annotated
from typing_extensions import TypedDict
from operator import add

class State(TypedDict):
    foo: str
    bar: Annotated[list[str], add]  # 注意：使用 add 作為歸約器

def node_a(state: State):
    return {"foo": "a", "bar": ["a"]}

def node_b(state: State):
    return {"foo": "b", "bar": ["b"]}

# 構建工作流
workflow = StateGraph(State)
workflow.add_node(node_a)
workflow.add_node(node_b)
workflow.add_edge(START, "node_a")
workflow.add_edge("node_a", "node_b")
workflow.add_edge("node_b", END)

# 使用檢查點編譯圖形
checkpointer = InMemorySaver()
graph = workflow.compile(checkpointer=checkpointer)

# 執行圖形
config = {"configurable": {"thread_id": "1"}}
graph.invoke({"foo": ""}, config)
```

**執行後會產生 4 個檢查點：**

1. **空檢查點**：`START` 作為下一個要執行的節點
2. **用戶輸入後**：`{'foo': '', 'bar': []}` 和 `node_a` 作為下一個節點
3. **node_a 完成後**：`{'foo': 'a', 'bar': ['a']}` 和 `node_b` 作為下一個節點
4. **node_b 完成後**：`{'foo': 'b', 'bar': ['a', 'b']}` 且沒有下一個節點

> 🔍 **重要觀察**：注意 `bar` 通道的值包含來自兩個節點的輸出，這是因為 `bar` 通道有歸約器（`add`）。

## 狀態管理操作

### 獲取狀態

```python
# 獲取最新狀態快照
config = {"configurable": {"thread_id": "1"}}
latest_state = graph.get_state(config)

# 獲取特定檢查點的狀態快照
config = {"configurable": {"thread_id": "1", "checkpoint_id": "特定檢查點ID"}}
specific_state = graph.get_state(config)
```

### 獲取狀態歷史

```python
config = {"configurable": {"thread_id": "1"}}
history = list(graph.get_state_history(config))
# 返回按時間順序排列的 StateSnapshot 列表，最近的在前
```

### 狀態重播（時間旅行）

```python
# 從特定檢查點重播執行
config = {"configurable": {"thread_id": "1", "checkpoint_id": "特定檢查點ID"}}
graph.invoke(None, config=config)
```

**重播的奧妙：**
- LangGraph 知道哪些步驟之前已經執行過
- 對於檢查點 ID 之前的步驟，LangGraph 會重播（不重新執行）
- 對於檢查點 ID 之後的步驟，會重新執行（創建新分支）

### 更新狀態

```python
# 更新狀態
graph.update_state(config, {"foo": 2, "bar": ["b"]})
```

**更新狀態的奧妙：**
- 更新被當作節點更新來處理
- 會傳遞給歸約器函數（如果定義了）
- 對於沒有歸約器的通道會覆蓋值
- 對於有歸約器的通道會合併值

例如：
```python
# 如果當前狀態是 {"foo": 1, "bar": ["a"]}
# 更新為 {"foo": 2, "bar": ["b"]}
# 結果將是 {"foo": 2, "bar": ["a", "b"]}
```

## 記憶體存儲（Memory Store）

### 跨線程共享狀態的挑戰

想像一個聊天機器人場景：我們希望在所有與用戶的對話（即線程）中保留用戶的特定信息。僅靠檢查點無法在線程間共享信息，這就是 Store 介面的用武之地。

### 基本使用

```python
from langgraph.store.memory import InMemoryStore
import uuid

# 創建記憶體存儲
in_memory_store = InMemoryStore()

# 記憶體按元組命名空間組織
user_id = "1"
namespace_for_memory = (user_id, "memories")

# 保存記憶體
memory_id = str(uuid.uuid4())
memory = {"food_preference": "我喜歡披薩"}
in_memory_store.put(namespace_for_memory, memory_id, memory)

# 讀取記憶體
memories = in_memory_store.search(namespace_for_memory)
print(memories[-1].dict())
```

### 語意搜尋功能

```python
from langchain.embeddings import init_embeddings

# 配置語意搜尋
store = InMemoryStore(
    index={
        "embed": init_embeddings("openai:text-embedding-3-small"),
        "dims": 1536,
        "fields": ["food_preference", "$"]
    }
)

# 使用自然語言查詢
memories = store.search(
    namespace_for_memory,
    query="用戶喜歡吃什麼？",
    limit=3
)
```

### 在 LangGraph 中使用

```python
from langgraph.checkpoint.memory import InMemorySaver

# 同時使用檢查點和存儲
checkpointer = InMemorySaver()
graph = graph.compile(checkpointer=checkpointer, store=in_memory_store)

# 在節點中使用存儲
def update_memory(state: MessagesState, config: RunnableConfig, *, store: BaseStore):
    user_id = config["configurable"]["user_id"]
    namespace = (user_id, "memories")
    
    # 創建新記憶體
    memory_id = str(uuid.uuid4())
    store.put(namespace, memory_id, {"memory": "新的記憶體內容"})

def call_model(state: MessagesState, config: RunnableConfig, *, store: BaseStore):
    user_id = config["configurable"]["user_id"]
    namespace = (user_id, "memories")
    
    # 搜尋相關記憶體
    memories = store.search(
        namespace,
        query=state["messages"][-1].content,
        limit=3
    )
    
    # 在模型調用中使用記憶體
    info = "\n".join([d.value["memory"] for d in memories])
```

## 檢查點實現選項

LangGraph 提供多種檢查點實現：

### 1. 記憶體檢查點（實驗用）
```python
from langgraph.checkpoint.memory import InMemorySaver
checkpointer = InMemorySaver()
```

### 2. SQLite 檢查點（本地開發）
```python
from langgraph.checkpoint.sqlite import SqliteSaver
import sqlite3

conn = sqlite3.connect("checkpoint.db")
checkpointer = SqliteSaver(conn)
```

### 3. PostgreSQL 檢查點（生產環境）
```python
from langgraph.checkpoint.postgres import PostgresSaver

checkpointer = PostgresSaver.from_conn_string("postgresql://...")
checkpointer.setup()
```

## 加密功能

```python
from langgraph.checkpoint.serde.encrypted import EncryptedSerializer

# 使用加密序列化器
serde = EncryptedSerializer.from_pycryptodome_aes()  # 讀取 LANGGRAPH_AES_KEY
checkpointer = SqliteSaver(sqlite3.connect("checkpoint.db"), serde=serde)
```

## 核心能力總結

### 1. 人機互動（Human-in-the-loop）
- 允許人類檢查、中斷和批准圖形步驟
- 人類可以查看任何時間點的圖形狀態
- 圖形可以在人類更新狀態後恢復執行

### 2. 記憶功能（Memory）
- 在互動間保持"記憶"
- 後續消息可以發送到同一線程
- 保留之前對話的記憶

### 3. 時間旅行（Time Travel）
- 允許重播先前的圖形執行
- 用於審查和調試特定圖形步驟
- 可以在任意檢查點分叉圖形狀態

### 4. 容錯性（Fault-tolerance）
- 如果節點失敗，可以從最後成功的步驟重新開始
- 存儲來自成功完成節點的待處理檢查點寫入
- 避免重新運行已成功的節點

## 總結

LangGraph 的持久化機制是其強大功能的基礎，它不僅提供了狀態管理，還實現了複雜的工作流程控制。通過檢查點和存儲的結合，開發者可以構建具有記憶、可恢復、可調試的智能應用程序。

**關鍵奧妙：**
- 檢查點提供了圖形執行的完整歷史記錄
- 存儲允許跨線程共享信息
- 歸約器控制狀態如何合併
- 時間旅行使調試和實驗變得簡單
- 容錯性確保長期運行的工作流程的可靠性