# 基礎入門

本章節涵蓋了 LangChain 的基礎知識，從設定開發環境到使用核心元件。

## 檔案

- **01-Getting-Started-Windows.ipynb**: 提供在 Windows 上設定開發環境的逐步指南，包括安裝 Git、pyenv 和 Poetry。
- **02-Getting-started-Mac.ipynb**: 提供在 macOS 上設定開發環境的逐步指南，涵蓋 Homebrew、Xcode、pyenv 和 Poetry 的安裝。
- **03-OpenAIAPI-Key-Generation.ipynb**: 解釋如何生成和管理 OpenAI API 金鑰，包括設定付款方式和使用限制。
- **04-LangSmith-Tracking-Setup.ipynb**: 介紹 LangSmith，一個用於追蹤和監控 LLM 應用的平台，並說明如何設定它。
- **05-Using-OpenAIAPI-MultiModal.ipynb**: 示範如何使用 OpenAI 的多模態模型（如 GPT-4o）處理文字和圖片輸入。
- **06-LangChain-Expression-Language(LCEL).ipynb**: 介紹 LangChain 表達式語言（LCEL），一種用於鏈結不同元件的宣告式方式。
- **07-LCEL-Interface.ipynb**: 深入探討 LCEL 的介面，包括 `stream`、`invoke` 和 `batch` 等方法。
- **08-Runnable.ipynb**: 解釋 `Runnable` 協定，這是 LangChain 中所有元件的基礎，並介紹 `RunnableLambda`、`RunnablePassthrough` 和 `itemgetter` 等工具。

## 核心概念

- **環境設定**: 設定 Python、Jupyter Notebook 和其他必要的函式庫，是開始使用 LangChain 的第一步。
- **API 金鑰管理**: 安全地管理 API 金鑰對於與 OpenAI 等服務互動至關重要。
- **LangSmith**: 一個強大的工具，用於除錯、監控和評估您的 LLM 應用。
- **多模態**: 能夠處理多種類型的輸入，如文字和圖片，是現代 LLM 的一個關鍵特性。
- **LCEL**: LangChain 的核心，提供了一種強大而靈活的方式來組合不同的元件，建立複雜的應用。
- **Runnable**: LangChain 中的一個核心抽象，它為所有元件提供了一個統一的介面，使其易於組合和重複使用。
