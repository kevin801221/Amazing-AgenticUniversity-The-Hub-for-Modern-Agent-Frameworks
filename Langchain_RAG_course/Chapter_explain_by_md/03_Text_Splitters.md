# RAG 中的文字分割器 (Text Splitters)

在將文件載入到 RAG (Retrieval-Augmented Generation) 系統後，下一個關鍵步驟是**文字分割 (Text Splitting)**。由於大型語言模型 (LLM) 的上下文視窗 (Context Window) 有其長度限制，我們無法將整份長文件一次性地傳遞給模型。因此，必須將長文件切分成更小、更易於管理的「區塊 (Chunks)」。

LangChain 提供了多種文字分割器，每種都有其獨特的策略和適用場景。本文件將根據 `07-TextSplitter` 資料夾中的筆記本內容，詳細介紹幾種核心的分割器。

## 1. 為何需要文字分割？

- **Token 限制**：避免超出 LLM 的 Token 上限。
- **檢索效率**：將文件切分成小區塊後，可以針對每個區塊進行向量化 (Embedding)，從而實現更精準的語意搜尋。
- **上下文精確性**：只檢索與使用者問題最相關的區塊，提供更具針對性的上下文給 LLM，減少雜訊干擾。

## 2. 基礎分割器：CharacterTextSplitter

這是最簡單的分割器，它根據指定的**單一字元**來進行分割。

**核心概念：**
- **分隔符 (Separator)**：你可以指定任何字元作為分隔符，例如換行符 `\n\n` 或空格 ` `。
- **區塊大小 (Chunk Size)**：定義每個區塊的最大長度（以字元數計算）。
- **區塊重疊 (Chunk Overlap)**：設定相鄰區塊之間重疊的字元數，這有助於保持區塊之間的語意連貫性，避免重要資訊在分割點被切斷。

**程式碼範例：**
```python
from langchain_text_splitters import CharacterTextSplitter

text_splitter = CharacterTextSplitter(
    separator="\n\n",  # 以雙換行符作為主要分隔符
    chunk_size=300,
    chunk_overlap=50,
)

docs = text_splitter.create_documents([long_text_string])
```

## 3. 遞迴分割器：RecursiveCharacterTextSplitter

這是 LangChain **官方推薦**且最常用的分割器。它的智慧之處在於它會**遞迴地**嘗試用不同的分隔符來分割文字，以確保區塊大小盡可能符合設定，同時最大程度地保留語意相關的文字片段在一起。

**核心概念：**
- **遞迴分割**：它會按照一個預設的分隔符列表 `["\n\n", "\n", " ", ""]` 依序嘗試分割。首先嘗試用雙換行符（段落），如果切分後的區塊仍然過大，則在該區塊內嘗試用單換行符（句子），再不行就用空格（單字），直到區塊大小符合要求。
- **語意保留**：這種策略優先保留段落，其次是句子，最後是單字，這符合人類閱讀和理解的邏輯。

**程式碼範例：**
```python
from langchain_text_splitters import RecursiveCharacterTextSplitter

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=250,
    chunk_overlap=50,
)

docs = text_splitter.create_documents([long_text_string])
```

## 4. 針對特定內容的分割器

除了通用的文字分割器，LangChain 還提供了針對特定內容格式的優化分割器。

### 程式碼分割 (Code Splitters)

`RecursiveCharacterTextSplitter` 可以透過 `from_language()` 方法，針對特定的程式語言（如 Python, JavaScript, Markdown）進行優化分割。它會使用該語言的語法結構（如 `class`, `def`, `\n\n`）作為優先的分隔符。

**程式碼範例 (Python)：**
```python
from langchain_text_splitters import Language, RecursiveCharacterTextSplitter

python_splitter = RecursiveCharacterTextSplitter.from_language(
    language=Language.PYTHON,
    chunk_size=100,
    chunk_overlap=20,
)

python_docs = python_splitter.create_documents([python_code_string])
```

### 結構化文件分割 (Markdown & HTML)

- **`MarkdownHeaderTextSplitter`**: 專門用來處理 Markdown 文件。它可以根據標頭 (`#`, `##`, `###`) 來分割文件，並將標頭資訊作為 metadata 加入到每個區塊中，從而保留了文件的層次結構。
- **`HTMLHeaderTextSplitter`**: 與 Markdown 分割器類似，但用於處理 HTML 文件，根據 `<h1>`, `<h2>` 等標頭標籤進行分割。

**程式碼範例 (`MarkdownHeaderTextSplitter`)：**
```python
from langchain_text_splitters import MarkdownHeaderTextSplitter

headers_to_split_on = [
    ("#", "Header 1"),
    ("##", "Header 2"),
]

markdown_splitter = MarkdownHeaderTextSplitter(headers_to_split_on=headers_to_split_on)
md_header_splits = markdown_splitter.split_text(markdown_document)
```

### JSON 分割 (RecursiveJsonSplitter)

`RecursiveJsonSplitter` 專門用於處理 JSON 資料。它會遞迴地遍歷 JSON 物件，將其分割成更小的 JSON 區塊，同時盡力保持巢狀物件的完整性。

**程式碼範例：**
```python
from langchain_text_splitters import RecursiveJsonSplitter

splitter = RecursiveJsonSplitter(max_chunk_size=300)
json_chunks = splitter.split_json(json_data=json_data)
```

## 5. 語意分割器：SemanticChunker

這是一種更先進的實驗性分割器，它不依賴固定的字元或規則，而是根據**語意相似性**來分割文字。

**核心概念：**
- **句子嵌入 (Sentence Embeddings)**：首先將文件分割成句子，然後將每個句子轉換成向量 (Embedding)。
- **相似性計算**：計算相鄰句子之間的語意相似度。當兩個句子之間的語意差異超過一個**閾值 (Breakpoint)** 時，就在此處進行分割。
- **動態分塊**：這種方法能夠更自然地將語意相關的句子群組在一起，形成更具邏輯性的區塊。
- **閾值類型**：可以基於「百分位數 (percentile)」、「標準差 (standard_deviation)」或「四分位距 (interquartile)」來動態決定分割點。

**程式碼範例：**
```python
from langchain_experimental.text_splitter import SemanticChunker
from langchain_openai.embeddings import OpenAIEmbeddings

# 使用 OpenAI 的嵌入模型
text_splitter = SemanticChunker(
    OpenAIEmbeddings(), 
    breakpoint_threshold_type="percentile", # 使用百分位數作為分割閾值
    breakpoint_threshold_amount=95 # 在相似度差異最大的前 5% 處分割
)

docs = text_splitter.create_documents([long_text_string])
```

## 結論

選擇哪種文字分割器取決於你的具體需求：
- 對於**通用文字**，`RecursiveCharacterTextSplitter` 是最推薦的選擇。
- 對於**程式碼**或**結構化文件 (Markdown, HTML, JSON)**，應優先使用其對應的專用分割器以保留結構資訊。
- 對於需要**最高語意連貫性**的場景，可以嘗試使用 `SemanticChunker`，但需注意它依賴於 Embedding 模型，計算成本較高。

有效的文字分割是提升 RAG 系統檢索準確性和最終生成品質的基石。
