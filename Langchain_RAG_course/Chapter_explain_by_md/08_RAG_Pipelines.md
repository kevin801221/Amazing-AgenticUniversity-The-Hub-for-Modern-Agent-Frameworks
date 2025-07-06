# RAG 中的管線 (Pipelines)

在 LangChain 中，**管線 (Pipeline)** 或 **鏈 (Chain)** 是將多個獨立的組件（如文件載入器、分割器、嵌入模型、向量儲存、檢索器、大型語言模型）串連起來，形成一個完整的、可執行的應用程式的核心概念。這得益於 LangChain 的**表達式語言 (LCEL)**，它允許開發者以一種聲明式、可組合的方式來建構複雜的邏輯。

本文件將根據 `12-RAG` 資料夾中的筆記本內容，展示如何從頭到尾建構一個完整的 RAG 管線，並介紹一些進階的 RAG 策略。

## 1. 基礎 RAG 管線

一個基礎的 RAG 管線通常包含以下步驟，這些步驟可以透過 LCEL 的 `|` (pipe) 運算子串連起來。

**運作流程：**
1.  **索引階段 (Indexing) - 通常離線進行**
    - **載入 (Load)**：使用 `DocumentLoader` (如 `PyPDFLoader`, `WebBaseLoader`) 讀取原始資料。
    - **分割 (Split)**：使用 `TextSplitter` (如 `RecursiveCharacterTextSplitter`) 將文件切分成小區塊。
    - **嵌入與儲存 (Embed & Store)**：使用 `Embedding` 模型將區塊轉換為向量，並存入 `VectorStore` (如 `FAISS`, `Chroma`)。

2.  **檢索與生成階段 (Retrieval & Generation) - 即時進行**
    - **檢索 (Retrieve)**：將向量儲存轉換為 `Retriever`，根據使用者查詢取回相關文件。
    - **生成 (Generate)**：將使用者的**問題 (question)** 和檢索到的**上下文 (context)** 傳遞給一個**提示模板 (PromptTemplate)**，然後將格式化後的提示送入**大型語言模型 (LLM)**（如 `ChatOpenAI`）生成最終答案。

**程式碼範例 (LCEL)：**
```python
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# 假設 retriever, prompt, llm 都已初始化

def format_docs(docs):
    return "\n\n".join(doc.page_content for doc in docs)

rag_chain = (
    {"context": retriever | format_docs, "question": RunnablePassthrough()}
    | prompt
    | llm
    | StrOutputParser()
)

# 執行管線
answer = rag_chain.invoke("歐盟的人工智慧法案有什麼主要目標？")
print(answer)
```

## 2. 具備對話歷史的 RAG (Conversational RAG)

為了讓 RAG 應用能夠進行多輪對話並記住先前的內容，我們需要為其增加**記憶 (Memory)** 功能。`RunnableWithMessageHistory` 是 LangChain 中實現此功能的關鍵組件。

**運作流程：**
1.  **修改提示模板**：在提示中加入一個 `MessagesPlaceholder`，用來存放歷史對話紀錄 (`chat_history`)。
2.  **建立歷史紀錄儲存區**：設定一個儲存機制（可以是記憶體中的字典，或更持久化的方案如 Redis、資料庫）來根據 `session_id` 保存每位使用者的對話歷史。
3.  **封裝鏈**：使用 `RunnableWithMessageHistory` 將原始的 RAG 鏈和歷史紀錄管理功能封裝在一起。

**程式碼範例：**
```python
from langchain_core.runnables.history import RunnableWithMessageHistory

# 假設 rag_chain 和 get_session_history 函式已定義

conversational_rag_chain = RunnableWithMessageHistory(
    rag_chain,
    get_session_history,
    input_messages_key="question",
    history_messages_key="chat_history",
)

# 第一次呼叫，傳入 session_id
response1 = conversational_rag_chain.invoke(
    {"question": "我的名字是 Bob。"}, 
    config={"configurable": {"session_id": "user123"}}
)

# 第二次呼叫，使用相同的 session_id，模型會記得先前的對話
response2 = conversational_rag_chain.invoke(
    {"question": "我叫什麼名字？"}, 
    config={"configurable": {"session_id": "user123"}}
)
```

## 3. 進階 RAG 策略：RAPTOR

RAPTOR (Recursive Abstractive Processing for Tree-Organized Retrieval) 是一種創新的 RAG 策略，旨在解決長上下文檢索的挑戰。它透過**遞迴地對文件進行聚類和摘要**，建立一個**樹狀的資訊結構**。

**運作流程：**
1.  **建立樹狀結構**：
    - **葉節點 (Leaf Nodes)**：將原始文件分割成小區塊作為樹的最底層。
    - **聚類 (Clustering)**：將語意上相似的區塊進行聚類。
    - **摘要 (Summarization)**：為每個聚類生成一個更高層次、更抽象的摘要。
    - **遞迴**：重複聚類和摘要的過程，直到生成一個代表整個文件集的根節點摘要，從而形成一棵資訊樹。
2.  **檢索**：
    - 將樹中的**所有節點**（包括原始區塊和各層級的摘要）都進行嵌入並存入同一個向量儲存中。
    - 檢索時，同時在所有層級上進行搜尋，這樣既能找到具體的細節（來自葉節點），也能找到高度概括的資訊（來自摘要節點）。

**優點：**
- **多層次檢索**：能夠根據查詢的抽象程度，在不同層級上找到最相關的資訊。
- **提升長上下文理解**：透過摘要，模型可以更好地理解和利用長篇文件的核心內容。

## 4. 多模態 RAG (Multimodal RAG)

傳統 RAG 只處理文字，而**多模態 RAG** 能夠同時理解和處理**文字與圖片**。這對於包含圖表、示意圖等視覺資訊的文件特別有用。

**運作流程 (以 Option 3 為例)：**
1.  **資料提取**：使用像 `unstructured` 這樣的工具，從 PDF 中同時提取文字區塊、表格和圖片。
2.  **圖片摘要**：使用一個多模態 LLM（如 GPT-4o）為每張圖片生成一段文字描述或摘要。
3.  **多向量索引**：
    - 將**文字區塊**、**表格摘要**和**圖片摘要**的向量存入向量儲存。
    - 同時，在一個獨立的文件儲存區 (`docstore`) 中，將原始的文字區塊、表格內容和**圖片本身**（例如以 Base64 格式）與其對應的摘要建立連結。
4.  **檢索與生成**：
    - 檢索時，在摘要的向量空間中進行搜尋。
    - 當檢索到相關的摘要時，取回其對應的**原始內容**（無論是文字、表格還是圖片）。
    - 將原始的文字、表格和**圖片**一起傳遞給一個多模態 LLM（如 GPT-4o），生成最終的圖文並茂的答案。

**優點：**
- **充分利用視覺資訊**：不會忽略文件中的圖表和圖片，能夠回答與視覺內容相關的問題。
- **更全面的理解**：結合文字和視覺上下文，生成更準確、更豐富的答案。

透過組合和應用這些基礎及進階的 RAG 管線，開發者可以建構出功能強大、能夠應對各種複雜場景的智慧應用。