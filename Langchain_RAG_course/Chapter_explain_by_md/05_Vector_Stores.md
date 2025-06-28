# RAG 中的向量儲存 (Vector Stores)

在 RAG (Retrieval-Augmented Generation) 流程中，**向量儲存 (Vector Store)** 扮演著至關重要的角色。在文件經過「載入 (Load)」、「分割 (Split)」和「嵌入 (Embed)」之後，所產生的向量化區塊 (Vectorized Chunks) 需要一個專門的資料庫來進行高效的儲存、管理和檢索。這就是向量儲存的核心功能。

本文件將根據 `09-VectorStore` 資料夾中的筆記本內容，介紹向量儲存的基本概念以及幾種主流的向量資料庫。

## 1. 為什麼需要向量儲存？

傳統的關聯式資料庫（如 SQL）是為結構化資料設計的，不適合儲存和查詢高維度的向量資料。向量儲存則專為此而生，它具備以下關鍵優勢：

- **高效的相似度搜尋**：能夠在數百萬甚至數十億個向量中，快速找到與給定查詢向量最相似的向量。
- **可擴展性**：能夠應對不斷增長的資料量，而不會顯著降低查詢效能。
- **語意檢索**：支援基於語意相似度的檢索，而不僅僅是關鍵字匹配，這對於 RAG 應用至關重要。
- **中繼資料過濾 (Metadata Filtering)**：允許在進行向量搜尋的同時，根據文件的中繼資料（如標題、日期、來源）進行過濾，實現更精準的檢索。

## 2. 核心操作 (CRUD & Search)

LangChain 為各種向量儲存提供了一個統一的介面，主要包含以下操作：

- **`add_documents` / `upsert`**: 新增或更新文件。將文字區塊及其對應的向量和中繼資料存入資料庫。
- **`delete`**: 刪除文件。可以根據文件的唯一 ID 或中繼資料進行刪除。
- **`similarity_search`**: 這是最核心的功能。給定一個查詢向量，它會回傳資料庫中最相似的 K 個文件區塊。

## 3. 常用的向量儲存方案

LangChain 整合了多種向量儲存方案，開發者可以根據應用需求、部署環境（本地 vs. 雲端）和成本來選擇。

### 本地端方案 (Local / Self-Hosted)

適合快速原型開發、小型應用或對資料隱私有嚴格要求的場景。

- **`FAISS` (Facebook AI Similarity Search)**: 由 Facebook 開發的高效能程式庫，非常適合在記憶體中進行快速的相似度搜尋。它輕量且易於整合，但本身不提供持久化儲存（需要額外實現）。
- **`Chroma`**: 一個開源的、專為 AI 應用設計的嵌入式資料庫。它簡單易用，支援本地持久化儲存和中繼資料過濾。
- **`PGVector`**: PostgreSQL 的一個擴充套件，讓傳統的關聯式資料庫具備了儲存和查詢向量的能力。適合希望在現有 PostgreSQL 基礎設施上擴充向量搜尋功能的團隊。
- **`Elasticsearch`**: 一個強大的分散式搜尋和分析引擎，除了傳統的全文檢索外，也支援向量相似度搜尋，適合需要混合搜尋（關鍵字 + 語意）的複雜場景。

**程式碼範例 (`FAISS`)：**
```python
from langchain_community.vectorstores import FAISS
from langchain_openai import OpenAIEmbeddings

# 假設 `docs` 是分割好的 Document 物件列表
# `embedding` 是初始化的嵌入模型

# 從文件建立 FAISS 索引
db = FAISS.from_documents(docs, embedding)

# 進行相似度搜尋
results = db.similarity_search(query="小王子來自哪個星球？", k=3)
```

### 雲端託管方案 (Cloud-Hosted / Managed)

適合需要高可用性、可擴展性和無需自行維護基礎設施的生產環境應用。

- **`Pinecone`**: 一個完全託管的向量資料庫服務，專為高效能、低延遲的向量搜尋而設計，提供簡單的 API 和可擴展的基礎設施。
- **`Qdrant`**: 提供開源和雲端兩種版本，以其豐富的過濾功能和高效的查詢效能而聞名。
- **`Weaviate`**: 同樣提供開源和雲端版本，支援圖形化資料模型和 GraphQL API，適合需要複雜資料關聯的應用。
- **`MongoDB Atlas Vector Search`**: MongoDB 的雲端服務，將向量搜尋功能與其強大的 NoSQL 文件資料庫無縫整合，方便在現有資料上擴充 AI 功能。
- **`Neo4j`**: 一個圖資料庫，除了儲存節點和關係外，也支援向量索引。這使得它能夠進行結合了圖遍歷和向量相似度搜尋的複雜查詢。

**程式碼範例 (`Pinecone`)：**
```python
import os
from langchain_pinecone import PineconeVectorStore
from langchain_openai import OpenAIEmbeddings

# 初始化 Pinecone
pinecone_api_key = os.getenv("PINECONE_API_KEY")
index_name = "my-langchain-index"

# 假設 `docs` 和 `embedding` 已準備好
vectorstore = PineconeVectorStore.from_documents(
    docs, 
    embedding, 
    index_name=index_name
)

# 進行相似度搜尋
results = vectorstore.similarity_search(query="小王子和狐狸說了什麼？", k=3)
```

## 4. 向量儲存作為檢索器 (Retriever)

在 LangChain 中，任何向量儲存都可以透過 `.as_retriever()` 方法轉換為一個**檢索器 (Retriever)**。檢索器是一個更通用的介面，它封裝了從資料來源（如向量儲存）取回文件的邏輯。

將向量儲存轉換為檢索器後，可以更方便地將其整合到 LangChain 的鏈 (Chains) 和代理 (Agents) 中，並支援更進階的檢索策略，如：

- **`Maximal Marginal Relevance (MMR)`**: 在回傳結果時，不僅考慮與查詢的相似度，還考慮結果之間的多樣性，避免回傳過於相似的內容。
- **`Self-Querying`**: 讓 LLM 根據使用者的自然語言問題，自動生成結構化的中繼資料過濾條件。

**程式碼範例：**
```python
# 將向量儲存轉換為檢索器
retriever = db.as_retriever(
    search_type="mmr", # 使用 MMR 檢索
    search_kwargs={'k': 5, 'fetch_k': 20} # 檢索參數
)

# 使用檢索器
relevant_docs = retriever.invoke("關於馴養的意義")
```

選擇合適的向量儲存是建構 RAG 應用的重要決策。你需要根據你的**資料規模**、**查詢延遲要求**、**預算**、**部署環境**以及是否需要**進階過濾**或**混合搜尋**功能來做出選擇。