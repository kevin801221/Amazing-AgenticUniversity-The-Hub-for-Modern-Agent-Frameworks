# RAG 中的文件載入器 (Document Loaders)

在 RAG (Retrieval-Augmented Generation) 流程中，**文件載入器 (Document Loader)** 是第一步，負責從各種不同的來源讀取資料，並將其轉換為 LangChain 標準的 `Document` 物件格式。一個 `Document` 物件包含 `page_content` (文字內容) 和 `metadata` (中繼資料) 兩個部分。

本文件將根據 `06-DocumentLoader` 資料夾中的筆記本內容，介紹幾種常用於處理不同檔案格式的文件載入器。

## 1. 處理 PDF 檔案

PDF 是最常見的文件格式之一。LangChain 提供了多種工具來載入 PDF，每種工具都有其優缺點。

- **`PyPDFLoader`**: 這是最基礎的 PDF 載入器，它能快速地將 PDF 中的文字內容按頁提取出來。它還支援透過 `extract_images=True` 來進行 OCR，從圖片中提取文字。
- **`PyMuPDFLoader`**: 以速度著稱，除了提取文字外，還能提供豐富的 metadata，如作者、標題、建立日期等。
- **`UnstructuredPDFLoader`**: 功能強大，它不僅能提取文字，還能理解文件的**版面結構**。透過設定 `mode="elements"`，它可以將文件中的標題、段落、列表等不同元素區分開來，並作為獨立的 `Document` 物件返回。
- **`PDFMinerLoader`**: 專注於文字與版面分析，也可以將 PDF 內容轉換為 HTML 格式，便於後續進行更細緻的結構化解析。
- **`PDFPlumberLoader`**: 擅長提取文字與**表格**資料，同樣能提供詳細的 metadata。

**程式碼範例 (`PyPDFLoader`)：**
```python
from langchain_community.document_loaders import PyPDFLoader

loader = PyPDFLoader("./data/layout-parser-paper.pdf")
docs = loader.load()

# 每個頁面都會成為一個獨立的 Document 物件
print(f"文件共有 {len(docs)} 頁")
print(docs[0].page_content[:200])
print(docs[0].metadata)
```

## 2. 處理網頁內容 (WebBaseLoader)

`WebBaseLoader` 專門用來從網頁上抓取內容。它底層使用 `BeautifulSoup` 來解析 HTML，功能非常靈活。

**核心概念：**
- **指定解析範圍**: 透過 `bs_kwargs` 參數，可以傳入 `bs4.SoupStrainer` 來指定只解析網頁中的特定 HTML 標籤，例如只抓取文章主體 `<div>`，過濾掉導覽列、廣告等無關內容。
- **並行載入**: 支援使用 `alazy_load()` 非同步地載入多個網址，大幅提升效率。
- **XML 支援**: 透過設定 `default_parser="xml"`，也可以用來載入 XML 格式的檔案，如網站地圖 (sitemap)。

**程式碼範例：**
```python
import bs4
from langchain_community.document_loaders import WebBaseLoader

# 只解析 class 為 'post-content' 的 <div> 標籤
bs_kwargs = dict(parse_only=bs4.SoupStrainer("div", attrs={"class": ["post-content"]}))

loader = WebBaseLoader(
    web_paths=("https://lilianweng.github.io/posts/2023-06-23-agent/",),
    bs_kwargs=bs_kwargs,
)
docs = loader.load()
print(docs[0].page_content[:300])
```

## 3. 處理結構化資料 (CSV & Excel)

對於像 CSV 和 Excel 這類表格化的結構化資料，LangChain 也提供了相應的載入器。

- **`CSVLoader`**: 將 CSV 檔案的**每一列**轉換成一個 `Document` 物件。你可以透過 `source_column` 參數指定某一欄作為文件的來源識別。
- **`UnstructuredExcelLoader`**: 類似於處理 PDF，它可以將 Excel 檔案的內容作為一個整體載入，或者在 `mode="elements"` 模式下，將其轉換為 HTML 表格格式儲存在 metadata 中。
- **`DataFrameLoader`**: 如果你已經使用 `pandas` 將資料讀取為 DataFrame，`DataFrameLoader` 可以直接從 DataFrame 載入資料，並指定某一欄作為 `page_content`。

**程式碼範例 (`CSVLoader`)：**
```python
from langchain_community.document_loaders.csv_loader import CSVLoader

loader = CSVLoader(file_path="./data/titanic.csv", source_column="Name")
docs = loader.load()

# 第一個乘客的資料
print(docs[0].page_content)
# metadata 中的 'source' 會是該乘客的姓名
print(docs[0].metadata)
```

## 4. 處理 Word 與 PowerPoint 檔案

- **`Docx2txtLoader`**: 一個輕量級的 Word (`.docx`) 檔案載入器，能快速提取純文字內容。
- **`UnstructuredWordDocumentLoader`**: 功能更強大，類似於 `UnstructuredPDFLoader`，能夠在 `mode="elements"` 模式下識別文件結構（標題、段落等）。
- **`UnstructuredPowerPointLoader`**: 專門用來處理 PowerPoint (`.pptx`) 檔案，同樣支援 `elements` 模式，可以將每張投影片中的標題、內文等元素分開處理。

**程式碼範例 (`UnstructuredWordDocumentLoader`)：**
```python
from langchain_community.document_loaders import UnstructuredWordDocumentLoader

# 使用 "elements" 模式來區分文件結構
loader = UnstructuredWordDocumentLoader(
    "./data/sample.docx", mode="elements"
)
docs = loader.load()

# 每個元素 (如標題、段落) 都會是一個獨立的 Document
print(f"文件包含 {len(docs)} 個元素")
print(docs[0].metadata["category"]) # 可能會是 'Title'
```

## 5. 特殊用途的載入器

- **`ArxivLoader`**: 直接從學術論文預印本網站 [arXiv.org](https://arxiv.org/) 搜尋並下載論文。你可以透過關鍵字查詢，並設定載入的論文數量。
- **`HWPLoader`**: 專門用於處理韓國常用的 HWP (Hangeul Word Processor) 文件格式。
- **`UpstageDocumentParseLoader`** 和 **`LlamaParse`**: 這些是更進階的、由第三方服務（Upstage, LlamaIndex）提供的文件解析工具。它們通常整合了更強大的版面分析和 OCR 模型，能夠處理非常複雜或掃描品質不佳的文件，並提供結構化的輸出（如 Markdown 或 JSON）。

**程式碼範例 (`ArxivLoader`)：**
```python
from langchain_community.document_loaders import ArxivLoader

# 搜尋關於 "Chain of Thought" 的論文，最多載入 2 篇
loader = ArxivLoader(query="Chain of thought", load_max_docs=2)
docs = loader.load()

print(f"載入 {len(docs)} 篇論文")
print(f"標題: {docs[0].metadata['Title']}")
print(f"摘要: {docs[0].metadata['Summary']}")
```

選擇合適的文件載入器是建構高效 RAG 系統的第一步。你需要根據你的資料來源、文件格式的複雜度以及是否需要保留結構化資訊來做出決定。