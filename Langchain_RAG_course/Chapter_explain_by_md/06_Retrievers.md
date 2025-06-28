# RAG 中的檢索器 (Retrievers)

在 RAG (Retrieval-Augmented Generation) 流程中，**檢索器 (Retriever)** 是一個核心組件，其主要職責是根據使用者的查詢 (Query)，從一個大規模的資料來源（通常是向量儲存）中「取回 (Retrieve)」最相關的文件區塊 (Chunks)。

與直接查詢向量儲存相比，檢索器提供了一個更抽象、更靈活的介面，並支援多種先進的檢索策略，以提升檢索結果的品質和多樣性。本文件將根據 `10-Retriever` 資料夾中的筆記本內容，介紹幾種關鍵的檢索器類型。

## 1. 基礎：VectorStoreRetriever

這是最基礎的檢索器，它直接將一個向量儲存 (Vector Store) 封裝成檢索器介面。任何向量儲存都可以透過 `.as_retriever()` 方法輕鬆轉換。

**核心功能：**
- **相似度搜尋 (Similarity Search)**：預設的檢索方式，回傳與查詢向量最相似的 `k` 個文件。
- **最大邊際相關性 (Maximal Marginal Relevance, MMR)**：一種更進階的搜尋策略。它在回傳結果時，不僅考慮文件與查詢的**相關性**，還會考慮文件之間的**多樣性**，避免回傳過於相似、冗餘的內容。
- **相似度分數過濾 (Similarity Score Threshold)**：只回傳相似度分數高於某個閾值的結果，用於過濾掉低相關性的雜訊。

**程式碼範例：**
```python
# 假設 `db` 是一個已建立的 FAISS 或 Chroma 向量儲存

# 建立一個使用 MMR 的檢索器
retriever = db.as_retriever(
    search_type="mmr",
    search_kwargs={"k": 5, "fetch_k": 20, "lambda_mult": 0.7}
)

relevant_docs = retriever.invoke("關於 RAG 的檢索策略有哪些？")
```

## 2. 提升檢索品質的進階檢索器

### MultiQueryRetriever

單一的使用者查詢可能因為用詞或觀點的限制，無法涵蓋所有相關的文件。`MultiQueryRetriever` 透過 LLM 從一個原始查詢**自動生成多個不同角度的相似查詢**，然後對每個查詢都進行檢索，最後將所有結果合併並去重。

**運作流程：**
1.  **生成查詢**：LLM 根據原始問題生成多個變體（例如：「LangChain 的優點是什麼？」可能會生成「LangChain 有哪些主要功能？」、「LangChain 的架構如何？」等）。
2.  **並行檢索**：對每個生成的查詢進行獨立的向量搜尋。
3.  **合併結果**：將所有檢索到的文件合併，得到一個更全面、更多樣的結果集。

### ContextualCompressionRetriever

有時候，即使是相關的文件區塊，也可能只有一小部分內容與查詢直接相關。`ContextualCompressionRetriever` 旨在解決這個問題，它會在檢索後對文件進行**壓縮**，只保留與查詢最相關的部分。

**運作流程：**
1.  **基礎檢索**：先由一個基礎檢索器（如 `VectorStoreRetriever`）取回一批文件。
2.  **文件壓縮**：一個**文件壓縮器 (Document Compressor)** 會過濾或重寫這些文件。
    - **`LLMChainExtractor`**: 使用 LLM 判斷每個文件中的哪些句子與查詢相關，並只保留這些句子。
    - **`EmbeddingsFilter`**: 計算每個文件與查詢的嵌入相似度，只保留高於某個閾值的文件。

### LongContextReorder

研究顯示，LLM 在處理長上下文時，對於開頭和結尾的資訊注意力最高，而中間的資訊容易被「遺忘」。`LongContextReorder` 是一個後處理步驟，它會將檢索到的文件列表進行**重排序**，將最相關的文件放在列表的**開頭和結尾**，而將次要的文件放在中間，以最大化 LLM 的注意力。

## 3. 處理複雜文件結構的檢索器

### ParentDocumentRetriever

在處理文件時，我們常常面臨一個兩難：小的文件區塊有利於精準的語意搜尋，但大的區塊能提供更完整的上下文。`ParentDocumentRetriever` 巧妙地解決了這個問題。

**運作流程：**
1.  **分割與儲存**：將原始文件分割成兩種尺寸：較大的「父區塊 (Parent Chunks)」和更小的「子區塊 (Child Chunks)」。
2.  **索引子區塊**：只將**子區塊**的向量存入向量儲存中，用於進行高效的相似度搜尋。
3.  **回傳父區塊**：當檢索到相關的子區塊後，檢索器會回傳其對應的**父區塊**（或完整的原始文件），從而為 LLM 提供更豐富的上下文。

### MultiVectorRetriever

這個檢索器更進一步，它允許你為一份文件儲存**多個不同的向量**，這些向量可以代表文件的不同方面。

**常見策略：**
- **儲存摘要 (Summary)**：為每個文件區塊生成一個摘要，然後將**摘要的向量**存入向量儲存。檢索時，先透過摘要找到相關區塊，再回傳完整的區塊內容。
- **假設性問題 (Hypothetical Questions)**：為每個文件區塊生成幾個「這個區塊可以回答什麼問題？」，然後將這些**問題的向量**存入向量儲存。這種方法對於問答場景特別有效。

## 4. 結合不同檢索策略：EnsembleRetriever

不同的檢索方法各有優劣。例如，傳統的關鍵字搜尋（如 `BM25`）擅長匹配精確的術語，而向量搜尋擅長捕捉語意相似度。`EnsembleRetriever` 可以將多個不同的檢索器（如一個 `BM25Retriever` 和一個 `VectorStoreRetriever`）**組合**起來。

**運作流程：**
- **並行檢索**：同時使用所有配置的檢索器進行搜尋。
- **結果融合**：使用 **Reciprocal Rank Fusion (RRF)** 演算法將不同檢索器的結果進行重排序和合併，得到一個綜合了多種檢索優勢的最終列表。

**程式碼範例：**
```python
from langchain.retrievers import BM25Retriever, EnsembleRetriever

# 假設 `faiss_retriever` 和 `docs` 已準備好
bm25_retriever = BM25Retriever.from_documents(docs)

ensemble_retriever = EnsembleRetriever(
    retrievers=[bm25_retriever, faiss_retriever],
    weights=[0.5, 0.5] # 設定不同檢索器的權重
)
```

選擇和組合正確的檢索器是建構高效能 RAG 應用的關鍵。你需要根據你的資料特性、查詢類型和應用場景，來設計最適合的檢索策略。