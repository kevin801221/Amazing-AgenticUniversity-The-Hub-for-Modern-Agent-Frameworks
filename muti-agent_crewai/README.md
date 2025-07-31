# CrewAI 金融分析代理專案

這是一個使用 [CrewAI](https://github.com/joaomdmoura/crewai) 框架構建的多代理（Multi-Agent）系統，旨在模擬一個金融分析團隊，自動對指定公司進行市場研究和財務分析，並最終提供是否值得投資的建議。

## 專案架構

本專案由兩個核心代理（Agent）協同工作，每個代理都有明確的角色和任務：

1.  **市場研究分析師 (Market Research Analyst)**:
    *   **目標**: 負責從網路上搜索指定公司的最新市場動態、新聞和財務狀況。
    *   **工具**: 使用 `Serper` API 進行即時的網路新聞搜索。
    *   **產出**: 整理並總結出公司的整體表現和關鍵新聞事件。

2.  **特許財務分析師 (Chartered Financial Analyst - CFA)**:
    *   **目標**: 接收市場研究分析師的報告，進行深度分析和解讀。
    *   **任務**: 根據現有資料，評估公司的市場走向、潛在風險與機遇，並撰寫最終的投資分析報告。
    *   **產出**: 一份包含市場總結、公司走向分析以及明確的��買入/不買入」建議的綜合報告。

## 檔案結構說明

```
muti-agent_crewai/
├── main.py             # 專案主入口，用於啟動 Crew
├── agents.py           # 定義所有代理 (Agent) 的角色、目標和背景故事
├── tasks.py            # 定義每個代理需要執行的任務 (Task)
├── search.py           # 提供給代理使用的搜索工具 (Tool)
├── requirements.txt    # 專案所需的 Python 依賴庫
└── README.md           # (本文件) 專案說明
```

-   **`main.py`**: 程式的啟動點。它會提示使用者輸入公司名稱，然後初始化 `AnalysisAgents` 和 `AnalysisTasks`，組建一個 `Crew`，並以順序模式（Sequential Process）啟動整個分析流程。
-   **`agents.py`**: 定義了「市場研究分析師」和「特許財務分析師」兩個代理。每個代理都配置了其獨特的 `role`, `goal`, `backstory` 和可用的 `tools`。
-   **`tasks.py`**: 定義了「研究任務」和「分析任務」。研究任務交給研究分析師，分析任務則交給財務分析師，並將前者的結果作為後者的上下文（Context）。
-   **`search.py`**: 實現了一個名為 `searchInfo` 的工具，該工具封裝了對 `google.serper.dev` 的 API 請求，讓代理能夠執行網路搜索。
-   **`requirements.txt`**: 列��了專案運行的必要套件，主要是 `crewai` 和 `langchain`。

## 如何運行

### 1. 前置準備

-   確保您的系統已安裝 Python 3.8 或更高版本。
-   本專案預設使用本地的 Ollama 模型。請確保您已安裝 [Ollama](https://ollama.com/) 並已拉取 `llama3.1` 模型：
    ```bash
    ollama pull llama3.1
    ```

### 2. 克隆並進入專案

```bash
git clone https://github.com/your-username/AgenticU-The-Modular-Teaching-Hub-for-Modern-LLM-Agent-Frameworks.git
cd AgenticU-The-Modular-Teaching-Hub-for-Modern-LLM-Agent-Frameworks/muti-agent_crewai
```

### 3. 環境設定與依賴安裝 (推薦使用 Poetry)

本專案使用 [Poetry](https.python-poetry.org/) 進行依賴管理和虛擬環境控制，這能確保開發環境的一致性。

#### A. 使用 Poetry 進行安裝 (推薦)

1.  **安裝 Poetry**: 如果您尚未安裝 Poetry，請參考 [官方文檔](https://python-poetry.org/docs/#installation) 進行安裝。

2.  **配置虛擬環境**: (可選，但推薦) 為了方便管理，可以設定 Poetry 將虛擬環境直接創建在專案目錄下。
    ```bash
    poetry config virtualenvs.in-project true
    ```

3.  **安裝依賴**: 在專案根目錄 (`muti-agent_crewai/`) 下運行以下命令，Poetry 會自動創建虛擬環境並安裝 `pyproject.toml` 中定義的所有依賴。
    ```bash
    poetry install
    ```

4.  **啟動虛擬環境**: 使用 `poetry shell` 進入專案的虛擬環境。之後的所有命令都將在此環境中執行。
    ```bash
    poetry shell
    ```
    您會看到命令提示符前面出現了虛擬環境的標識。

#### B. 使用 pip 進行安裝 (備用選項)

如果您不想使用 Poetry，也可以使用傳統的 `pip` 方式安裝。

```bash
pip install -r requirements.txt
```

### 4. 設定 API 金鑰

本專案需要使用 `Serper` 進行網路搜索。

-   前往 [serper.dev](https://serper.dev/) 註冊並獲取您的免費 API 金鑰。
-   在 `muti-agent_crewai` 目錄下創建一個名為 `.env` 的檔案，並將您的金鑰添加進去：

    ```
    SERPER_API_KEY="YOUR_SERPER_API_KEY"
    ```
    程式將會自動讀取此環境變數。

### 5. 執行專案

確保您的 Ollama 服務正在本地運行。如果您是使用 Poetry，請確保已處於 `poetry shell` 環境中。然後執行 `main.py`：

```bash
python main.py or poetry run python main.py
```

程式將會提示您輸入想分析的公司名稱，例如 `Apple` 或 `台積電`，之後代理團隊便會開始工作。

## 預期輸出

執行完畢後，您將在終端機看到一份由「特許財務分析師」產出的詳細分析報告，內容包含市場動態總結以及對該公司股票的最終投資建議。
