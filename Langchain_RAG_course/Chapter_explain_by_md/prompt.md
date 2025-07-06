# 提示工程

本章節深入探討了 LangChain 中的提示工程，從基本模板到高階技術，如 few-shot 提示和動態範例選擇。

## 檔案

- **01-PromptTemplate.ipynb**: 介紹 `PromptTemplate`，一個用於建立可重複使用和動態提示的基礎元件。它還涵蓋了 `ChatPromptTemplate` 和 `MessagePlaceholder`，用於處理多輪對話。
- **02-FewShotPromptTemplate.ipynb**: 解釋如何使用 `FewShotPromptTemplate` 提供少量範例來引導模型的行為。它還示範了如何使用 `Chroma` 向量儲存進行動態範例選擇。
- **03-LangChain-Hub.ipynb**: 介紹 LangChain Hub，一個用於分享和發現提示的社群平台。
- **04-Personal-Prompts.ipynb**: 提供一個包含各種專業領域專門提示的 cookbook。
- **05-Prompt-Caching.ipynb**: 示範如何使用提示快取來最佳化 API 使用，特別是對於具有重複內容的長提示。

## 核心概念

- **提示模板**: LangChain 的一個核心元件，允許您建立可重複使用、動態的提示，以適應不同的輸入。
- **Few-shot 提示**: 一種強大的技術，透過提供少量精心挑選的範例來引導模型的行為，從而提高輸出的品質和一致性。
- **動態範例選擇**: 使用向量儲存（如 Chroma）根據語意相似性動態選擇最相關的範例，進一步增強模型的上下文理解能力。
- **LangChain Hub**: 一個社群驅動的平台，您可以在其中發現、分享和重複使用來自其他開發人員的提示。
- **提示快取**: 一種最佳化技術，可顯著減少重複任務或具有一致前置詞的長提示的處理時間和成本。
