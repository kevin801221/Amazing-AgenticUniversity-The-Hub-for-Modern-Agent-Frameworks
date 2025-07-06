# RAG 中的嵌入模型 (Embedding Models)

在 RAG (Retrieval-Augmented Generation) 流程中，**嵌入 (Embedding)** 是將文字資料轉換為電腦能夠理解和處理的**數值向量 (Numerical Vectors)** 的核心技術。這些向量能夠捕捉文字的**語意資訊**，使得我們可以計算不同文字片段之間的相似度，從而實現精準的資訊檢索。

本文件將根據 `08-Embedding` 資料夾中的筆記本內容，介紹幾種在 LangChain 中常用的嵌入模型及其應用。

## 1. 什麼是嵌入 (Embedding)？

嵌入是一種將高維度的離散資料（如單字、句子、文件）對應到一個低維度的連續向量空間的技術。在這個向量空間中，語意上相似的文字會被對應到相近的位置。

**為何需要嵌入？**
- **語意搜尋**：傳統的關鍵字搜尋只能匹配字面上的文字，而語意搜尋可以找到意思相近但用詞不同的內容。
- **相似度計算**：可以量化地計算兩段文字的相似程度，常用於推薦系統、文本分類等任務。
- **機器學習輸入**：將文字轉換為數值向量，是將其作為機器學習模型輸入的必要步驟。

## 2. 常用的嵌入模型

LangChain 整合了多種嵌入模型，開發者可以根據需求、成本和效能來選擇。

### OpenAI Embeddings

由 OpenAI 提供的商業嵌入模型，以其高品質和強大的語意理解能力而聞名。

**核心特點：**
- **高效能**：在多數語意任務上表現出色。
- **維度可調**：新一代模型（如 `text-embedding-3-large`）支援調整輸出向量的維度，以在效能和成本之間取得平衡。
- **簡單易用**：透過 API 呼叫即可使用，無需自行部署模型。

**程式碼範例：**
```python
from langchain_openai import OpenAIEmbeddings

# 初始化 OpenAI 嵌入模型
openai_embedding = OpenAIEmbeddings(model="text-embedding-3-large")

# 將查詢和文件轉換為向量
query_vector = openai_embedding.embed_query("關於 OpenAI 的 gpt 嵌入模型是什麼？")
docs_vectors = openai_embedding.embed_documents(["文件一的內容", "文件二的內容"])
```

### Hugging Face Embeddings

Hugging Face 是一個開源社群，提供了大量免費的預訓練模型，包括多種高效能的嵌入模型。`HuggingFaceEmbeddings` 允許你在本地端或透過 Hugging Face 的 API 來使用這些模型。

**核心特點：**
- **開源免費**：可以免費在本地部署和使用，無需支付 API 費用。
- **模型選擇多樣**：可以從 [MTEB (Massive Text Embedding Benchmark) Leaderboard](https://huggingface.co/spaces/mteb/leaderboard) 上選擇最適合你任務的模型。
- **本地部署**：模型在本地運行，資料無需上傳至雲端，保障了資料隱私。

**常用模型：**
- `intfloat/multilingual-e5-large-instruct`：支援多語言的指令型嵌入模型。
- `BAAI/bge-m3`：針對大規模文字處理優化的模型，在檢索和語意相似度任務上表現優異。

**程式碼範例 (本地運行)：**
```python
from langchain_huggingface.embeddings import HuggingFaceEmbeddings

model_name = "intfloat/multilingual-e5-large-instruct"

# 初始化 Hugging Face 嵌入模型，並指定在本地 GPU/CPU 上運行
hf_embeddings = HuggingFaceEmbeddings(
    model_name=model_name,
    model_kwargs={"device": "cpu"}, # 或 'cuda', 'mps'
    encode_kwargs={"normalize_embeddings": True},
)

query_vector = hf_embeddings.embed_query(query_text)
docs_vectors = hf_embeddings.embed_documents(document_texts)
```

### 本地端開源模型 (Ollama, Llama.cpp, GPT4All)

對於追求極致隱私和成本效益的應用，可以直接在本地運行完全開源的模型。

- **`OllamaEmbeddings`**: Ollama 是一個簡化本地部署 LLM 的工具，透過它可以輕鬆運行如 `nomic-embed-text` 等嵌入模型。
- **`LlamaCppEmbeddings`**: Llama.cpp 是一個用 C++ 實現的高效能 LLM 推理框架，支援 GGUF 等量化模型格式，非常適合在 CPU 上運行。
- **`GPT4AllEmbeddings`**: GPT4All 是一個提供免費、隱私保護的本地聊天機器人專案，其嵌入模型經過優化，可在 CPU 上高效運行。

**程式碼範例 (`OllamaEmbeddings`)：**
```python
from langchain_ollama import OllamaEmbeddings

# 確保你已經透過 `ollama run nomic-embed-text` 運行了該模型
ollama_embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
)

query_vector = ollama_embeddings.embed_query(query_text)
```

### 多模態嵌入 (Multimodal Embeddings)

傳統的嵌入模型只處理文字，而**多模態嵌入模型**可以同時處理**文字和圖片**，將它們轉換到同一個向量空間中。這使得我們可以實現「以文搜圖」或「以圖搜圖」的功能。

- **`OpenCLIPEmbeddings`**: LangChain 整合了 OpenCLIP，這是一個開源的 CLIP (Contrastive Language–Image Pre-training) 模型實現，能夠生成圖片和文字的嵌入向量。

**程式碼範例：**
```python
from langchain_experimental.open_clip import OpenCLIPEmbeddings

# 初始化 OpenCLIP 模型
clip_embedding = OpenCLIPEmbeddings(
    model_name="ViT-g-14",
    checkpoint="laion2b_s34b_b88k",
)

# 嵌入圖片 (傳入圖片路徑列表)
image_vectors = clip_embedding.embed_image(image_paths)

# 嵌入文字
text_vector = clip_embedding.embed_query(text_query)
```

## 3. 嵌入快取 (CacheBackedEmbeddings)

為了避免重複計算相同文字的嵌入，從而節省時間和 API 成本，LangChain 提供了 `CacheBackedEmbeddings`。它會將文字的嵌入結果儲存在一個快取儲存區（可以是本地檔案系統或記憶體）。當下次遇到相同的文字時，它會直接從快取中讀取結果，而不是重新呼叫嵌入模型。

**程式碼範例：**
```python
from langchain.storage import LocalFileStore
from langchain.embeddings import CacheBackedEmbeddings
from langchain_openai import OpenAIEmbeddings

# 設定本地檔案儲存區
store = LocalFileStore("./cache/")

# 建立底層的嵌入模型
underlying_embeddings = OpenAIEmbeddings()

# 建立支援快取的嵌入器
cached_embedder = CacheBackedEmbeddings.from_bytes_store(
    underlying_embeddings,
    store,
    namespace=underlying_embeddings.model, # 為不同模型設定獨立的命名空間
)

# 第一次呼叫會計算並快取結果
embeddings_a = cached_embedder.embed_documents(["你好", "世界"])

# 第二次呼叫會直接從快取讀取，速度極快
embeddings_b = cached_embedder.embed_documents(["你好", "世界"])
```

選擇合適的嵌入模型是 RAG 系統效能的關鍵。你需要綜合考量**成本**、**效能**、**資料隱私**以及是否需要**多模態**或**多語言**支援來做出最佳決策。