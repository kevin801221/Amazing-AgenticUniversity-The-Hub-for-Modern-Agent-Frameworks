# RAG 中的記憶體管理

在建構能夠進行多輪對話的 RAG (Retrieval-Augmented Generation) 應用時，「記憶體 (Memory)」是一個至關重要的組件。它負責儲存、追蹤和取回對話歷史，讓大型語言模型 (LLM) 能夠理解上下文，從而生成更連貫、更具相關性的回應。

LangChain 提供了多種記憶體管理機制，每種機制都有其獨特的運作方式和適用場景。本文件將根據 `05-Memory` 資料夾中的筆記本內容，詳細介紹幾種核心的記憶體類型。

## 1. ConversationBufferMemory

這是最基礎的記憶體類型，它會將所有對話歷史完整地儲存在一個緩衝區中，並在需要時將其全部傳遞給 LLM。

**核心概念：**
- **完整保存**：不對對話內容做任何刪減或摘要，保留最完整的上下文。
- **簡單易用**：實現方式非常直觀，適合快速開發和測試。

**潛在問題：**
- **Token 限制**：隨著對話變長，完整的歷史記錄可能會超過 LLM 的 Token 上下文視窗限制，導致錯誤或效能下降。

**程式碼範例：**
```python
from langchain.memory import ConversationBufferMemory
from langchain_openai import ChatOpenAI
from langchain.chains import ConversationChain

# 初始化記憶體
memory = ConversationBufferMemory()

# 建立對話鏈
llm = ChatOpenAI(temperature=0, model_name="gpt-4o")
conversation = ConversationChain(
    llm=llm,
    memory=memory,
)

# 進行對話
response = conversation.predict(input="你好，我想遠端開立一個銀行帳戶。該如何開始？")
print(response)

# 檢查記憶體中的歷史紀錄
print(memory.load_memory_variables({})["history"])
```

## 2. ConversationBufferWindowMemory

為了緩解 `ConversationBufferMemory` 可能導致的 Token 過多問題，`ConversationBufferWindowMemory` 引入了「滑動視窗」的概念。它只會保留最近的 `k` 次對話互動。

**核心概念：**
- **滑動視窗**：只儲存最近的 `k` 輪對話，舊的對話會被捨棄。
- **控制長度**：有效防止記憶體無限增長，確保不會輕易超出 Token 限制。

**程式碼範例：**
```python
from langchain.memory import ConversationBufferWindowMemory

# 只保留最近 2 次的對話互動 (k=2)
memory = ConversationBufferWindowMemory(k=2, return_messages=True)

memory.save_context(inputs={"human": "第一輪問題"}, outputs={"ai": "第一輪回答"})
memory.save_context(inputs={"human": "第二輪問題"}, outputs={"ai": "第二輪回答"})
memory.save_context(inputs={"human": "第三輪問題"}, outputs={"ai": "第三輪回答"})

# 此時，記憶體中只會保留第二輪和第三輪的對話
print(memory.load_memory_variables({})["history"])
```

## 3. ConversationTokenBufferMemory

這種記憶體管理方式更加精確，它不是根據對話的「次數」，而是根據對話內容的「Token 數量」來決定何時需要刪減歷史紀錄。

**核心概念：**
- **Token 長度限制**：設定一個 `max_token_limit`，當對話歷史的總 Token 數超過此限制時，會從最舊的紀錄開始刪除。
- **精確控制**：比 `ConversationBufferWindowMemory` 更能精準地控制傳遞給 LLM 的上下文長度。

**程式碼範例：**
```python
from langchain.memory import ConversationTokenBufferMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-4o-mini")

# 將最大 Token 長度限制為 150
memory = ConversationTokenBufferMemory(
    llm=llm,
    max_token_limit=150,
    return_messages=True,
)

# ... 多次儲存對話 ...

# 檢查記憶體，只有總 Token 數在 150 以內的最新對話會被保留
print(memory.load_memory_variables({})["history"])
```

## 4. ConversationSummaryMemory & ConversationSummaryBufferMemory

對於非常長的對話，即使只保留部分歷史也可能佔用大量 Token。`ConversationSummaryMemory` 提供了一種解決方案：將舊的對話內容進行「摘要」。

- **`ConversationSummaryMemory`**：會將**所有**的對話歷史都摘要成一段精簡的文字。
- **`ConversationSummaryBufferMemory`**：這是一種混合策略。它會保留最近的一部分對話原文（基於 Token 數量），並將更早的對話內容進行摘要。

**核心概念：**
- **對話摘要**：利用 LLM 將冗長的對話歷史濃縮成精華摘要，大幅減少 Token 消耗。
- **混合策略 (Buffer + Summary)**：兼顧了保留近期對話細節和控制整體上下文長度的需求。

**程式碼範例 (`ConversationSummaryBufferMemory`)：**
```python
from langchain.memory import ConversationSummaryBufferMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI()

# 設定 Token 門檻為 200
memory = ConversationSummaryBufferMemory(
    llm=llm,
    max_token_limit=200,
    return_messages=True,
)

# ... 多次儲- 存對話 ...

# 當對話總 Token 超過 200 時，舊的對話會被摘要
# 最新的對話（在 200 Token 內）會被完整保留
print(memory.load_memory_variables({})["history"])
```

## 5. ConversationEntityMemory & ConversationKGMemory

這兩種記憶體專注於從對話中提取和管理「實體 (Entity)」及其相關資訊。

- **`ConversationEntityMemory`**：以「鍵值對」的形式儲存關於特定實體的資訊。例如，它可以記住 `{"Amelia": "是一位屢獲殊榮的風景攝影師..."}`。
- **`ConversationKGMemory`**：以「知識圖譜 (Knowledge Graph)」的形式儲存實體之間的**關係**。它將資訊結構化為「主詞-關係-受詞」的三元組，例如 `(Shelly Kim, lives in, Pangyo)`。

**核心概念：**
- **實體提取**：自動從對話中識別出人名、地名、組織等關鍵實體。
- **結構化儲存**：將關於實體的零散資訊整理成結構化的格式，便於查詢和推理。
- **關係網絡 (KG)**：`ConversationKGMemory` 能夠建立複雜的實體關係網絡，回答如「誰是 Shelly 的同事？」這類問題。

**程式碼範例 (`ConversationKGMemory`)：**
```python
from langchain_community.memory.kg import ConversationKGMemory
from langchain_openai import ChatOpenAI

llm = ChatOpenAI(model_name="gpt-4o", temperature=0)
memory = ConversationKGMemory(llm=llm, return_messages=True)

memory.save_context(
    {"input": "這位是居住在板橋的 Shelly Kim。"},
    {"output": "你好 Shelly，很高興認識你！"},
)
memory.save_context(
    {"input": "Shelly Kim 是我們公司的新設計師。"},
    {"output": "太好了！歡迎加入我們的團隊。"},
)

# 檢索關於 "Shelly Kim" 的所有結構化資訊
print(memory.load_memory_variables({"input": "誰是 Shelly Kim？"}))
# 輸出: {'history': [SystemMessage(content="On Shelly Kim: Shelly Kim lives in Pangyo. Shelly Kim is our company's new designer.")]}
```

## 6. VectorStoreRetrieverMemory

這種記憶體將對話歷史儲存在一個「向量資料庫 (Vector Store)」中。當需要取回記憶時，它不是按照時間順序，而是根據「語意相關性」來查詢最相關的對話片段。

**核心概念：**
- **向量化儲存**：將每段對話轉換成向量 (Embedding) 並存入向量資料庫。
- **語意搜尋**：根據新問題的語意，在資料庫中尋找最相似、最相關的歷史對話。
- **非時序性**：不依賴對話的時間順序，非常適合需要從大量歷史中查找特定資訊的場景，如面試或客服對話。

**程式碼範例：**
```python
import faiss
from langchain_openai.embeddings import OpenAIEmbeddings
from langchain_community.vectorstores.faiss import FAISS
from langchain.memory import VectorStoreRetrieverMemory

# 初始化向量資料庫 (以 FAISS 為例)
embeddings_model = OpenAIEmbeddings()
embedding_size = 1536
index = faiss.IndexFlatL2(embedding_size)
vectorstore = FAISS(embeddings_model, index, InMemoryDocstore({}), {})
retriever = vectorstore.as_retriever(search_kwargs={"k": 1})

# 初始化記憶體
memory = VectorStoreRetrieverMemory(retriever=retriever)

# ... 儲存多段面試對話 ...

# 查詢與 "主修" 相關的歷史對話
print(memory.load_memory_variables({"prompt": "面試者的主修是什麼？"}))
```

## 7. 使用資料庫儲存記憶 (以 SQLite 為例)

對於需要持久化儲存、跨會話共享記憶的應用，可以將對話歷史儲存在 SQL 資料庫中。`SQLChatMessageHistory` 提供了與 SQLAlchemy 相容的介面。

**核心概念：**
- **持久化儲存**：對話歷史被保存在資料庫檔案中，不會因程式結束而消失。
- **會話管理**：透過 `session_id` 來區分和管理不同使用者或不同對話的歷史紀錄。
- **靈活性**：支援所有 SQLAlchemy 相容的資料庫 (如 SQLite, PostgreSQL, MySQL)。

**程式碼範例：**
```python
from langchain_community.chat_message_histories import SQLChatMessageHistory

# 初始化，指定 session_id 和資料庫連線
chat_message_history = SQLChatMessageHistory(
    session_id="user123_conversation456",
    connection="sqlite:///sqlite.db"
)

# 新增對話
chat_message_history.add_user_message("你好，我是 Heesun。")
chat_message_history.add_ai_message("你好 Heesun！很高興認識你。")

# 檢視儲存的訊息
print(chat_message_history.messages)
```

透過 `RunnableWithMessageHistory`，可以輕鬆地將這種持久化記憶與 LCEL (LangChain Expression Language) 鏈結合，實現可配置的、按需加載的對話歷史管理。
