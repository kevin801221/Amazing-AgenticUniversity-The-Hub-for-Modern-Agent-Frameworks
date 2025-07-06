<a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.

# uv 股票資料洞察應用程式快速建構指南

## 1. 安裝 uv

```bash
# macOS/Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Windows (PowerShell)
powershell -c "irm https://astral.sh/uv/install.ps1 | iex"

# 驗證安裝
uv --version
```

## 2. 初始化專案

```bash
# 創建專案
uv init stock-insights-app
cd stock-insights-app

# 設定 Python 版本
uv python pin 3.11

# 創建基本目錄結構
mkdir -p {scripts,documentation,images,src/stock_insights}
touch src/stock_insights/__init__.py
touch src/stock_insights/main.py
```

## 3. 依賴管理

### 3.1 安裝核心依賴

```bash
# Web 框架
uv add fastapi uvicorn[standard]

# AI/ML 核心
uv add langchain langchain-openai langgraph
uv add openai

# 資料庫
uv add pymongo psycopg2-binary chromadb

# 資料處理
uv add pandas numpy matplotlib

# 工具類
uv add python-dotenv pydantic requests
```

### 3.2 安裝開發依賴

```bash
# 測試和代碼品質
uv add --dev pytest black flake8
```

### 3.3 查看依賴

```bash
# 查看已安裝的依賴
uv pip list

# 查看依賴樹
uv pip tree
```

## 4. 環境配置

### 4.1 創建環境變數文件

```bash
# 創建 .env 文件
cat > .env << 'EOF'
OPENAI_API_KEY=your_openai_api_key_here
MONGODB_URL=mongodb://localhost:27017
POSTGRES_URL=postgresql://username:password@localhost:5432/stock_data
API_HOST=0.0.0.0
API_PORT=8080
EOF
```

### 4.2 創建簡單的 FastAPI 應用

```python
# src/stock_insights/main.py
from fastapi import FastAPI
import uvicorn
import os
from dotenv import load_dotenv

load_dotenv()

app = FastAPI(title="股票資料洞察 API", version="1.0.0")

@app.get("/")
async def root():
    return {"message": "歡迎使用股票資料洞察 API", "status": "running"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

@app.get("/stock/{ticker}/price-stats")
async def get_stock_price_stats(ticker: str, operation: str, price_type: str, duration: int):
    return {
        "ticker": ticker,
        "operation": operation,
        "price_type": price_type,
        "duration": duration,
        "result": f"模擬結果：{ticker} 的 {operation} {price_type} 價格（{duration}天）"
    }

@app.get("/news/{ticker}")
async def get_news(ticker: str, topic: str = None):
    return {
        "ticker": ticker,
        "topic": topic,
        "result": f"模擬新聞：{ticker} 相關新聞分析"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=os.getenv("API_HOST", "0.0.0.0"),
        port=int(os.getenv("API_PORT", 8080)),
        reload=True
    )
```

## 5. 執行 API

### 5.1 啟動開發服務器

```bash
# 方法 1：直接運行
uv run src/stock_insights/main.py

# 方法 2：使用 uvicorn
uv run uvicorn src.stock_insights.main:app --host 0.0.0.0 --port 8080 --reload
```

### 5.2 測試 API

```bash
# 測試根路由
curl http://localhost:8080/

# 測試健康檢查
curl http://localhost:8080/health

# 測試股票價格統計
curl "http://localhost:8080/stock/AAPL/price-stats?operation=highest&price_type=close&duration=30"

# 測試新聞查詢
curl "http://localhost:8080/news/AAPL?topic=earnings"
```

### 5.3 查看 API 文檔

打開瀏覽器訪問：
- Swagger UI：http://localhost:8080/docs
- ReDoc：http://localhost:8080/redoc

## 6. 常用命令

```bash
# 查看專案信息
uv pip show fastapi

# 更新依賴
uv pip install --upgrade fastapi

# 導出依賴列表
uv pip freeze > requirements.txt

# 運行測試
uv run pytest

# 代碼格式化
uv run black src/

# 檢查代碼品質
uv run flake8 src/
```

## 7. 專案結構

建構完成後的專案結構：

```
Agentic_Stock_Insight/                                                                           
 │     ├── config/               # 專案設定檔                                                           
 │     ├── db/                   # 資料庫模組 (MongoDB, PostgreSQL)                                     
 │     ├── documentation/        # 專案文件                                                             
 │     ├── images/               # 專案圖片資源                                                         
 │     ├── logs/                 # 日誌文件                                                             
 │     ├── rag_graphs/           # LangGraph RAG 工作流程定義                                            
 │     │   ├── news_rag_graph/                                                                          
 │     │   └── stock_data_rag_graph/                                                                    
 │     ├── rest_api/             # FastAPI 應用程式與路由                                                
 │     │   └── main.py           # API 進入點                                                            
 │     ├── scraper/              # 資料爬蟲 (新聞, 股票)                                                
 │     ├── scripts/              # 獨立腳本 (資料庫初始化, 健康檢查)                                    
 │     ├── templates/            # HTML 模板                                                             
 │     ├── utils/                # 共用工具函式                                                          
 │     ├── vector_db/            # ChromaDB 向量資料庫儲存目錄                                          
 │     ├── .env                  # 環境變數 (需自行創建)                                                
 │     ├── requirements.txt      # Python 依賴                                                          
 │     └── README.md             # 專案說明  
```

這樣就完成了基本的 uv 專案建構和 API 啟動！

# 股票資料洞察應用程式使用指南

## 資料庫概覽
- **MongoDB**：存儲超過 10,000 筆新聞文章，集合名稱為 `news_articles`
- **PostgreSQL**：存儲超過 19,000 筆股票價格資料，資料表名稱為 `stock_data`
- **向量資料庫**：存儲新聞文章的向量嵌入，用於語意搜尋

## 如何使用 API 端點

### 股票資料查詢
- **價格統計**：
  ```bash
  GET http://localhost:8080/stock/{股票代碼}/price-stats?operation={操作}&price_type={價格類型}&duration={天數}
  ```
  - 範例：`http://localhost:8080/stock/AAPL/price-stats?operation=highest&price_type=close&duration=30`
  - 參數說明：
    - `operation`：highest (最高)、lowest (最低)、average (平均)
    - `price_type`：open (開盤價)、close (收盤價)、high (最高價)、low (最低價)
    - `duration`：查詢天數 (1、7、14、30)

- **股票圖表**：
  ```bash
  GET http://localhost:8080/stock/{股票代碼}/chart?price_type={價格類型}&duration={天數}
  ```
  - 範例：`http://localhost:8080/stock/AAPL/chart?price_type=close&duration=30`

### 新聞查詢
- **主題新聞**：
  ```bash
  GET http://localhost:8080/news/{股票代碼}?topic={主題}
  ```
  - 範例：`http://localhost:8080/news/AAPL`
  - 帶主題查詢：`http://localhost:8080/news/AAPL?topic=earnings`

## 使用腳本進行離線分析

### 可視化股票資料
```bash
python scripts/visualize_data.py
```
將生成多檔股票的股價與成交量圖表，並輸出為 PNG 檔案。

### 查詢 PostgreSQL 資料
```bash
python scripts/query_postgres.py
```
從 PostgreSQL 拉取股票價格資料。

### 查詢 MongoDB 資料
```bash
python scripts/query_mongodb.py
```
從 MongoDB 拉取新聞文章。

### 環境健康檢查
```bash
python scripts/health_check.py
```
驗證 OpenAI API Key、MongoDB 與 PostgreSQL 連線狀態。

## 專案簡介

本專案示範如何結合 Agentic RAG（Retrieval‑Augmented Generation）工作流程，從新聞與金融資料中提取洞察。整合大型語言模型 (LLM)、ChromaDB 向量資料庫、LangChain、LangChain Expression Language (LCEL) 與 LangGraph，提供完整、動態的分析能力。

## 主要功能

- **股票績效可視化**：繪製所選股票的歷史表現圖表。
- **屬性化資料檢索**：根據使用者需求，擷取特定股票屬性的詳細資訊。
- **新聞彙整**：聚合與特定股票或公司相關的一般新聞及主題新聞。

## 高層架構
![高層架構](documentation/high_level_design.png)

## 實作方式

### 非同步資料抓取
1. **新聞資料**：以非同步方式定期抓取預先定義股票的新聞，存入 MongoDB，並同步至 ChromaDB 以供語意搜尋。
2. **金融資料**：以非同步方式定期抓取所選股票的金融資料，存入 PostgreSQL。

### LangGraph 工作流程

#### 新聞資料 RAG 圖
用於先從向量資料庫（MongoDB 同步）檢索股票新聞，若文件不夠相關，則透過網路搜尋補足，再由 LLM 生成最終結果。

![新聞 RAG 圖](images/news-rag-graph.png)

核心節點：
- **從資料庫檢索新聞 (`retrieve_news`)**：使用 LLM、LangChain 與檢索器工具，進行語意搜尋。
- **文件評分 (`grade_documents`)**：評估檢索文件品質，決定是否產出結果或觸發網路搜尋。
- **網路搜尋 (`web_search`)**：整合 TavilySearch 工具與 LLM，進行網路擴充搜尋。
- **產生結果 (`generate_results`)**：依據查詢與文件內容，產出最終回答。

#### 股票資料 RAG 圖
用於從 SQL 資料庫 (PostgreSQL) 檢索金融數據，並由 LLM 分析、生成自然語言結果。

![股票資料 RAG 圖](images/stock-data-rag-graph.png)

核心節點：
- **產生 SQL (`generate_sql`)**：LLM 與 LangChain 自動生成查詢語句。
- **執行 SQL (`execute_sql`)**：執行查詢並擷取資料。
- **產生結果 (`generate_results`)**：LLM 根據資料與需求輸出回答。

#### 股票資料圖表 RAG 圖
用於從 SQL 資料庫檢索金融數據並產生視覺化圖表。

![股票圖表 RAG 圖](images/stock-charts-rag-graph.png)

核心節點：
- **產生 SQL (`generate_sql`)**：同上。
- **執行 SQL (`execute_sql`)**：同上。

## API 介面

詳細規格請參考 `documentation/openapi.json`。

### 股價統計 (GET `/stock/{ticker}/price-stats`)
取得特定股票的價格統計結果。

**參數：**
| 參數      | 型別   | 說明                              |
|----------|-------|---------------------------------|
| ticker   | str   | 股票代碼                          |
| operation| str   | 操作：highest / lowest / average |
| price_type| str  | 價格類型：open / close / high / low |
| duration | int   | 時間範圍（天數）                 |

**回傳：**
```json
{
  "ticker": "AAPL",
  "operation": "highest",
  "price_type": "close",
  "duration": "30",
  "result": "..."
}
```

### 股價圖表 (GET `/stock/{ticker}/chart`)
取得特定股票的價格資料並回傳資料點。

**參數：同上**

**回傳：**
```json
{
  "ticker": "AAPL",
  "price_type": "close",
  "duration": "30",
  "result": [...]
}
```

### 主題新聞查詢 (GET `/news/{ticker}`)
取得特定股票的一般或主題新聞。

**參數：**
| 參數    | 型別   | 說明           |
|--------|-------|--------------|
| ticker | str   | 股票代碼       |
| topic  | str   | 主題 (可選)    |

**回傳：**
```json
{
  "ticker": "AAPL",
  "topic": "earnings",
  "result": "..."
}
```

### 根路由 (GET `/`)
應用程式首頁。

**參數：** 無

## 類別圖
![類別圖](images/classes_stock_proj.png)

## 圖片資源
請參考 `images/` 目錄中的示意圖。

## 測試架構
專案使用 pytest 進行自動化測試，以確保各模組之可靠性與穩定性。
執行命令：
```bash
pytest
```

## 可觀測性與追蹤
為監控應用程式效能並除錯 LLM 流程，本專案整合了 LangSmith 追蹤，提供：
- **LLM 呼叫追蹤**：記錄所有與模型之互動，包括輸入、輸出與執行時間。
- **除錯協助**：協助偵測 RAG 流程之瓶頸與錯誤。
- **LangSmith 儀表板**：視覺化分析追蹤資料。

LangSmith 已完整整合至所有 RAG 工作流程，提供可操作之觀測洞察。

## 參考資料
- **LangGraph**：用於構建具狀態、多角色 LLM 應用之函式庫，便於建立代理與多代理工作流程。
- **LangChain Expression Language (LCEL)**：宣告式鏈結語言，用於撰寫並優化複雜工作流程的組合。

本專案示範先進 AI 工作流程整合，提供財經與新聞資料之深入分析，打造全方位股票市場評估工具。
