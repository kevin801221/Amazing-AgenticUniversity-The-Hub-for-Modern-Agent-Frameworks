<div align="center">
  <h1>PhiloAgents 課程</h1>
  <h3>學習如何建構一個由 AI 驅動的遊戲模擬引擎，以模仿知名哲學家。</h3>
  <p class="tagline">由 <a href="https://theneuralmaze.substack.com/">The Neural Maze</a> 與 <a href="https://decodingml.substack.com">Decoding ML</a> 聯手，並與 <a href="https://rebrand.ly/philoagents-mongodb">MongoDB</a>、<a href="https://rebrand.ly/philoagents-opik">Opik</a> 及 <a href="https://rebrand.ly/philoagents-groq">Groq</a> 合作的開源課程。</p>
</div>

</br>

<p align="center">
    <img src="static/diagrams/system_architecture.png" alt="架構" width="600">
</p>

## 📖 關於本課程

曾經夢想過打造屬於自己的 AI 遊戲嗎？準備好踏上這段刺激的旅程，我們將結合遊戲開發的快感與尖端的 AI 技術！

歡迎來到 **PhiloAgents**（由 [Decoding ML](https://decodingml.substack.com) 與 [The Neural Maze](https://theneuralmaze.substack.com) 聯手推出）—— 在這裡，古老的哲學與現代 AI 相遇。在這門實作課程中，您將打造一個 AI 代理模擬引擎，讓歷史上的哲學家在互動遊戲環境中重獲新生。想像一下，與柏拉圖進行深度對話、與亞里斯多德辯論倫理學，或與圖靈本人討論人工智慧！

**在 6 個全面的模組中**，您將學習如何：
- 創造能夠真實體現歷史哲學家的 AI 代理
- 精通建構代理式應用程式 (agentic applications)
- 從頭開始設計並實現一個生產就緒的 RAG、LLM 與 LLMOps 系統

### 🎮 PhiloAgents 體驗：您將會做什麼

將靜態的 NPC 轉變為動態的 AI 人格，使其能夠：
- 建立一個由 AI 代理和大型語言模型 (LLM) 驅動的遊戲角色模擬引擎，模仿我們歷史上的哲學家，如柏拉圖、亞里斯多德和圖靈。
- 設計生產就緒的代理式 RAG 系統。
- 將代理以 RESTful API 的形式發布。
- 應用 LLMOps 和軟體工程的最佳實踐。
- 使用業界工具：Groq、MongoDB、Opik、LangGraph、LangChain、FastAPI、Websockets、Docker 等。

完成本課程後，您將擁有自己的代理式模擬引擎，如下方影片所示：

<video src="https://github.com/user-attachments/assets/aedc041e-00ed-42ce-99f2-24ce74847e7a"/></video>

-------

<table style="border-collapse: collapse; border: none;">
  <tr style="border: none;">
    <td width="20%" style="border: none;">
      <a href="https://theneuralmaze.substack.com/" aria-label="The Neural Maze">
        <img src="https://avatars.githubusercontent.com/u/151655127?s=400&u=2fff53e8c195ac155e5c8ee65c6ba683a72e655f&v=4" alt="The Neural Maze Logo" width="150"/>
      </a>
    </td>
    <td width="80%" style="border: none;">
      <div>
        <h2>📬 保持更新</h2>
        <p><b><a href="https://theneuralmaze.substack.com/">加入 The Neural Maze</a></b>，學習建構真正有效的 AI 系統，從原理到生產。每週三，直接送到您的收件匣。千萬不要錯過！
</p>
      </div>
    </td>
  </tr>
</table>

<p align="center">
  <a href="https://theneuralmaze.substack.com/">
    <img src="https://img.shields.io/static/v1?label&logo=substack&message=立即訂閱&style=for-the-badge&color=black&scale=2" alt="立即訂閱" height="40">
  </a>
</p>

<table style="border-collapse: collapse; border: none;">
  <tr style="border: none;">
    <td width="20%" style="border: none;">
      <a href="https://decodingml.substack.com/" aria-label="Decoding ML">
        <img src="https://github.com/user-attachments/assets/f2f2f9c0-54b7-4ae3-bf8d-23a359c86982" alt="Decoding ML Logo" width="150"/>
      </a>
    </td>
    <td width="80%" style="border: none;">
      <div>
        <h2>📬 保持更新</h2>
        <p><b><a href="https://decodingml.substack.com/">加入 Decoding ML</a></b>，獲取關於設計、編碼和部署生產級 AI 系統的實證內容，結合軟體工程和 MLOps 的最佳實踐，助您成功交付 AI 應用。每週，直接送到您的收件匣。</p>
      </div>
    </td>
  </tr>
</table>

<p align="center">
  <a href="https://decodingml.substack.com/">
    <img src="https://img.shields.io/static/v1?label&logo=substack&message=立即訂閱&style=for-the-badge&color=black&scale=2" alt="立即訂閱" height="40">
  </a>
p>

## 🎯 您將學到什麼

在建構 PhiloAgents 模擬引擎的過程中，您將精通：

- 使用 LangGraph 建構智慧代理
  - 代理開發與協調
  - RAG 代理式溝通模式
  - 透過提示工程（Plato、Aristotle、Turing）進行角色扮演

- 創建生產級 RAG 系統
  - 向量資料庫整合
  - 從維基百科和史丹佛哲學百科創建知識庫
  - 進階資訊檢索

- 設計系統架構
  - 端到端設計（UI → 後端 → 代理 → 監控）
  - 使用 FastAPI 和 Docker 部署 RESTful API
  - 透過 WebSockets 進行即時通訊

- 實現進階代理功能
  - 使用 MongoDB 實現短期和長期記憶
  - 動態對話處理
  - 即時回應生成

- 精通業界工具與實踐
  - 與 Groq、MongoDB、Opik 整合
  - 現代 Python 工具（uv、ruff）
  - LangChain 和 LangGraph 生態系統
  - 利用 GroqCloud 上的 LLM 進行高速推論

- 應用 LLMOps 最佳實踐
  - 自動化代理評估
  - 提示監控與版本控制
  - 評估資料集生成

🥷 課程結束時，您將成為生產就緒 AI 代理開發的忍者！

## 👥 誰該加入？

**本課程專為透過實作學習的人設計。** 完成課程後，您將擁有自己的程式碼模板和足夠的靈感來開發個人的代理式應用程式。

| 目標受眾 | 為何加入？ |
|---|---|
| ML/AI 工程師 | 建構生產就緒的代理式應用程式（超越 Jupyter Notebook 教學）。 |
| 資料/軟體工程師 | 設計端到端的代理式應用程式架構。 |
| 資料科學家 | 使用 LLMOps 和軟體工程最佳實踐來實現生產級代理系統。 |

## 🎓 先備條件

| 類別 | 要求 |
|---|---|
| **技能** | - Python (初學者) <br/> - 機器學習、LLM、RAG (初學者) |
| **硬體** | 現代筆記型電腦/個人電腦（我們將使用 Groq 和 OpenAI API 來呼叫我們的 LLM） |
| **程度** | 初級到中級 |

## 💰 費用結構

**本課程為開源且完全免費！** 您可以在不使用任何進階 LLMOps 功能的情況下，以 0 成本運行模擬引擎。

如果您選擇端到端運行整個系統（這是可選的），雲端工具的最高費用約為 1 美元：

| 服務 | 預估最高費用 |
|---|---|
| Groq 的 API | $0 |
| OpenAI 的 API (可選) | ~$1 |

在模組 5（可選模組）中，我們使用 OpenAI 的 API 作為「LLM 即評審」(LLM-as-a-judge) 來評估我們的代理。在課程的其餘部分，我們使用 Groq 的 API，它提供免費方案。

**只是閱讀教材？完全免費！**

## 🥂 開源課程：參與完全免費且開放

作為一門開源課程，您無需註冊。所有內容均為自學進度，完全免費，資源可自由取用（影片和文章相輔相成——建議兩者都看以獲得全貌）：
- **程式碼**：此 GitHub 儲存庫
- **影片**：[The Neural Maze](https://www.youtube.com/@TheNeuralMaze)
- **文章**：[Decoding ML](https://decodingml.substack.com)

## 📚 課程大綱

這門**開源課程包含 6 個全面的模組**，涵蓋理論、系統設計和實作。

[閱讀此文](https://decodingml.substack.com/p/from-0-to-pro-ai-agents-roadmap)以快速了解您將在每個模組中學到的內容。

我們建議您這樣做以充分利用本課程：
1.  複製此儲存庫。
2.  閱讀教材（影片和文章相輔相成——建議兩者都看以獲得全貌）。
3.  設定程式碼並運行它以重現我們的結果。
4.  深入研究程式碼以了解實作細節。

| 模組 | 書面課程 | 影片課程 | 描述 | 運行程式碼 |
|---|---|---|---|---|
| <div align="center">0</div> | <a href="https://decodingml.substack.com/p/from-0-to-pro-ai-agents-roadmap"><img src="static/diagrams/episode_1_play.png" alt="圖表 0" width="300"></a> | <div align="center">**無影片**</div> | 快速導覽您將在每個模組中學到的內容。 | <div align="center">**無程式碼**</div> |
| <div align="center">1</div> | <a href="https://decodingml.substack.com/p/build-your-gaming-simulation-ai-agent"><img src="static/diagrams/episode_1_play.png" alt="圖表 1" width="300"></a> | <a href="https://youtu.be/vbhShB70vFE?si=tK0hRQbEqlZMwFMm"><img src="static/thumbnails/episode_1_play.png" alt="縮圖 1" width="400"></a> | 設計您的遊戲模擬 AI PhiloAgent 架構。 | <div align="center">**無程式碼**</div> |
| <div align="center">2</div> | <a href="https://decodingml.substack.com/p/your-first-production-ready-rag-agent"><img src="static/diagrams/episode_2_play.png" alt="圖表 2" width="300"></a> | <a href="https://youtu.be/5fqkdiTP5Xw?si=Y1erl41qNSYlSaYx"><img src="static/thumbnails/episode_2_play.png" alt="縮圖 2" width="400"></a> | 使用代理式 RAG 在 LangGraph 中建構 PhiloAgent。 | [philoagents-api](philoagents-api) |
| <div align="center">3</div> | <a href="https://decodingml.substack.com/p/memory-the-secret-sauce-of-ai-agents"><img src="static/diagrams/episode_3_play.png" alt="圖表 3" width="300"></a> | <a href="https://youtu.be/xDouz4WNHV0?si=t2Wk179LQnSDY1iL"><img src="static/thumbnails/episode_3_play.png" alt="縮圖 3" width="400"></a> | 透過實現短期和長期記憶元件，完成我們的代理式 RAG 層。 | [philoagents-api](philoagents-api) |
| <div align="center">4</div> | <a href="https://decodingml.substack.com/p/deploying-agents-as-real-time-apis"><img src="static/diagrams/episode_4_play.png" alt="圖表 4" width="300"></a> | <a href="https://youtu.be/svABzOASrzg?si=nylMpFm0nozPNSbi"><img src="static/thumbnails/episode_4_play.png" alt="縮圖 4" width="400"></a> | 將代理公開為 RESTful API (FastAPI + Websockets)。 | [philoagents-api](philoagents-api) |
| <div align="center">5</div> | <a href="https://decodingml.substack.com/p/observability-for-rag-agents"><img src="static/diagrams/episode_5_play.png" alt="圖表 5" width="300"></a> | <a href="https://youtu.be/Yy0szt5OlNI?si=otYpqM_BY2gxdxnS"><img src="static/thumbnails/episode_5_play.png" alt="縮圖 5" width="400"></a> | RAG 代理的可觀察性（LLMOps 的一部分）：評估代理、提示監控、提示版本控制等。 | [philoagents-api](philoagents-api) |
| <div align="center">6</div> | <a href="https://decodingml.substack.com/p/engineer-python-projects-like-a-pro"><img src="static/diagrams/episode_6_play.png" alt="圖表 6" width="300"></a> | <div align="center">**無影片**</div> | 像專家一樣建構 Python 專案。現代 Python 工具。Docker 設定。 | [philoagents-api](philoagents-api) |

如果您覺得自己特別勇敢，這裡還有一段 2 小時 30 分鐘的影片課程，我們將所有影片課程合併為一。

<p align="center">
    <a href="https://youtu.be/pg1Sn9rsFak?si=bKMdL-EbaMb90PT3"><img src="static/thumbnails/full_course_play.png" alt="PhiloAgents 完整課程" width="500"></a>
</p>

------

<table style="border-collapse: collapse; border: none;">
  <tr style="border: none;">
    <td width="20%" style="border: none;">
      <a href="https://theneuralmaze.substack.com/" aria-label="The Neural Maze">
        <img src="https://avatars.githubusercontent.com/u/151655127?s=400&u=2fff53e8c195ac155e5c8ee65c6ba683a72e655f&v=4" alt="The Neural Maze Logo" width="150"/>
      </a>
    </td>
    <td width="80%" style="border: none;">
      <div>
        <h2>📬 保持更新</h2>
        <p><b><a href="https://theneuralmaze.substack.com/">加入 The Neural Maze</a></b>，學習建構真正有效的 AI 系統，從原理到生產。每週三，直接送到您的收件匣。千萬不要錯過！
</p>
      </div>
    </td>
  </tr>
</table>

<p align="center">
  <a href="https://theneuralmaze.substack.com/">
    <img src="https://img.shields.io/static/v1?label&logo=substack&message=立即訂閱&style=for-the-badge&color=black&scale=2" alt="立即訂閱" height="40">
  </a>
</p>

<table style="border-collapse: collapse; border: none;">
  <tr style="border: none;">
    <td width="20%" style="border: none;">
      <a href="https://decodingml.substack.com/" aria-label="Decoding ML">
        <img src="https://github.com/user-attachments/assets/f2f2f9c0-54b7-4ae3-bf8d-23a359c86982" alt="Decoding ML Logo" width="150"/>
      </a>
    </td>
    <td width="80%" style="border: none;">
      <div>
        <h2>📬 保持更新</h2>
        <p><b><a href="https://decodingml.substack.com/">加入 Decoding ML</a></b>，獲取關於設計、編碼和部署生產級 AI 系統的實證內容，結合軟體工程和 MLOps 的最佳實踐，助您成功交付 AI 應用。每週，直接送到您的收件匣。</p>
      </div>
    </td>
  </tr>
</table>

<p align="center">
  <a href="https://decodingml.substack.com/">
    <img src="https://img.shields.io/static/v1?label&logo=substack&message=立即訂閱&style=for-the-badge&color=black&scale=2" alt="立即訂閱" height="40">
  </a>
</p>

## 🏗️ 專案結構

在建構 PhiloAgents 模擬引擎時，我們將依賴兩個獨立的應用程式：

```bash
.
├── philoagents-api/     # 包含 PhiloAgents 模擬引擎的後端 API (Python)
└── philoagents-ui/      # 遊戲的前端 UI (Node)
```

本課程將只專注於包含所有代理模擬邏輯的 `philoagents-api` 應用程式。`philoagents-ui` 應用程式則用於玩遊戲。

## 👔 資料集

為了讓我們的哲學家代理具備真實世界的知識，我們將使用來自以下來源的資料來填充他們的長期記憶：
- 維基百科
- 史丹佛哲學百科

您無需明確下載任何東西。在填充長期記憶時，`philoagents-api` 應用程式會自動從網際網路下載資料。

## 🚀 開始使用

詳細的設定和使用說明請見 [INSTALL_AND_USAGE.md](INSTALL_AND_USAGE.md) 檔案。

**專家提示：** 先閱讀附帶的文章，以便更了解您將要建構的系統。

## 💡 問題與疑難排解

有問題或遇到困難嗎？我們隨時提供協助！

請開啟一個 [GitHub issue](https://github.com/neural-maze/philoagents-course/issues) 來：
- 詢問有關課程材料的問題
- 技術疑難排解
- 釐清概念

## 🥂 貢獻

作為一門開源課程，我們可能無法修復所有出現的錯誤。

如果您發現任何錯誤並知道如何修復，請透過您的錯誤修復為本課程做出貢獻，以支持未來的讀者。

您可以隨時透過以下方式貢獻：
- Fork 本儲存庫
- 修復錯誤
- 建立一個 pull request

📍 [更多詳情，請參閱貢獻指南。](CONTRIBUTING.md)

我們將深深感謝您對 AI 社群和未來讀者的支持 🤗

## 贊助商

<div align="center">
  <table style="border-collapse: collapse; border: none;">
    <tr style="border: none;">
      <td align="center" style="border: none; padding: 20px;">
        <a href="https://rebrand.ly/philoagents-mongodb" target="_blank">
          <img src="static/sponsors/mongo.png" width="200" style="max-height: 45px; width: auto;" alt="MongoDB">
        </a>
      </td>
      <td align="center" style="border: none; padding: 20px;">
        <a href="https://rebrand.ly/philoagents-opik" target="_blank">
          <img src="static/sponsors/opik.png" width="200" style="max-height: 45px; width: auto;" alt="Opik">
        </a>
      </td>
      <td align="center" style="border: none; padding: 20px;">
        <a href="https://rebrand.ly/philoagents-groq" target="_blank">
          <img src="static/sponsors/groq.png" width="200" style="max-height: 45px; width: auto;" alt="Groq">
        </a>
      </td>
    </tr>
  </table>
</div>

## 核心貢獻者

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/iusztinpaul">
        <img src="https://github.com/iusztinpaul.png" width="100px;" alt="Paul Iusztin"/><br />
        <sub><b>Paul Iusztin</b></sub>
      </a><br />
      <sub>AI/ML 工程師</sub>
    </td>
    <td align="center">
      <a href="https://github.com/MichaelisTrofficus">
        <img src="https://github.com/MichaelisTrofficus.png" width="100px;" alt="Miguel Otero Pedrido"/><br />
        <sub><b>Miguel Otero Pedrido</b></sub>
      </a><br />
      <sub>AI/ML 工程師</sub>
    </td>
  </tr>
</table>

## 授權

本專案採用 MIT 授權 - 詳情請見 [LICENSE](LICENSE) 檔案。

------

<table style="border-collapse: collapse; border: none;">
  <tr style="border: none;">
    <td width="20%" style="border: none;">
      <a href="https://theneuralmaze.substack.com/" aria-label="The Neural Maze">
        <img src="https://avatars.githubusercontent.com/u/151655127?s=400&u=2fff53e8c195ac155e5c8ee65c6ba683a72e655f&v=4" alt="The Neural Maze Logo" width="150"/>
      </a>
    </td>
    <td width="80%" style="border: none;">
      <div>
        <h2>📬 保持更新</h2>
        <p><b><a href="https://theneuralmaze.substack.com/">加入 The Neural Maze</a></b>，學習建構真正有效的 AI 系統，從原理到生產。每週三，直接送到您的收件匣。千萬不要錯過！
</p>
      </div>
    </td>
  </tr>
</table>

<p align="center">
  <a href="https://theneuralmaze.substack.com/">
    <img src="https://img.shields.io/static/v1?label&logo=substack&message=立即訂閱&style=for-the-badge&color=black&scale=2" alt="立即訂閱" height="40">
  </a>
</p>

<table style="border-collapse: collapse; border: none;">
  <tr style="border: none;">
    <td width="20%" style="border: none;">
      <a href="https://decodingml.substack.com/" aria-label="Decoding ML">
        <img src="https://github.com/user-attachments/assets/f2f2f9c0-54b7-4ae3-bf8d-23a359c86982" alt="Decoding ML Logo" width="150"/>
      </a>
    </td>
    <td width="80%" style="border: none;">
      <div>
        <h2>📬 保持更新</h2>
        <p><b><a href="https://decodingml.substack.com/">加入 Decoding ML</a></b>，獲取關於設計、編碼和部署生產級 AI 系統的實證內容，結合軟體工程和 MLOps 的最佳實踐，助您成功交付 AI 應用。每週，直接送到您的收件匣。</p>
      </div>
    </td>
  </tr>
</table>

<p align="center">
  <a href="https://decodingml.substack.com/">
    <img src="https://img.shields.io/static/v1?label&logo=substack&message=立即訂閱&style=for-the-badge&color=black&scale=2" alt="立即訂閱" height="40">
  </a>
</p>

## 🏗️ 專案結構

在建構 PhiloAgents 模擬引擎時，我們將依賴兩個獨立的應用程式：

```bash
.
├── philoagents-api/     # 包含 PhiloAgents 模擬引擎的後端 API (Python)
└── philoagents-ui/      # 遊戲的前端 UI (Node)
```

本課程將只專注於包含所有代理模擬邏輯的 `philoagents-api` 應用程式。`philoagents-ui` 應用程式則用於玩遊戲。

## 👔 資料集

為了讓我們的哲學家代理具備真實世界的知識，我們將使用來自以下來源的資料來填充他們的長期記憶：
- 維基百科
- 史丹佛哲學百科

您無需明確下載任何東西。在填充長期記憶時，`philoagents-api` 應用程式會自動從網際網路下載資料。

## 🚀 開始使用

詳細的設定和使用說明請見 [INSTALL_AND_USAGE.md](INSTALL_AND_USAGE.md) 檔案。

**專家提示：** 先閱讀附帶的文章，以便更了解您將要建構的系統。

## 💡 問題與疑難排解

有問題或遇到困難嗎？我們隨時提供協助！

請開啟一個 [GitHub issue](https://github.com/neural-maze/philoagents-course/issues) 來：
- 詢問有關課程材料的問題
- 技術疑難排解
- 釐清概念

## 🥂 貢獻

作為一門開源課程，我們可能無法修復所有出現的錯誤。

如果您發現任何錯誤並知道如何修復，請透過您的錯誤修復為本課程做出貢獻，以支持未來的讀者。

您可以隨時透過以下方式貢獻：
- Fork 本儲存庫
- 修復錯誤
- 建立一個 pull request

📍 [更多詳情，請參閱貢獻指南。](CONTRIBUTING.md)

我們將深深感謝您對 AI 社群和未來讀者的支持 🤗

## 贊助商

<div align="center">
  <table style="border-collapse: collapse; border: none;">
    <tr style="border: none;">
      <td align="center" style="border: none; padding: 20px;">
        <a href="https://rebrand.ly/philoagents-mongodb" target="_blank">
          <img src="static/sponsors/mongo.png" width="200" style="max-height: 45px; width: auto;" alt="MongoDB">
        </a>
      </td>
      <td align="center" style="border: none; padding: 20px;">
        <a href="https://rebrand.ly/philoagents-opik" target="_blank">
          <img src="static/sponsors/opik.png" width="200" style="max-height: 45px; width: auto;" alt="Opik">
        </a>
      </td>
      <td align="center" style="border: none; padding: 20px;">
        <a href="https://rebrand.ly/philoagents-groq" target="_blank">
          <img src="static/sponsors/groq.png" width="200" style="max-height: 45px; width: auto;" alt="Groq">
        </a>
      </td>
    </tr>
  </table>
</div>

## 核心貢獻者

<table>
  <tr>
    <td align="center">
      <a href="https://github.com/iusztinpaul">
        <img src="https://github.com/iusztinpaul.png" width="100px;" alt="Paul Iusztin"/><br />
        <sub><b>Paul Iusztin</b></sub>
      </a><br />
      <sub>AI/ML 工程師</sub>
    </td>
    <td align="center">
      <a href="https://github.com/MichaelisTrofficus">
        <img src="https://github.com/MichaelisTrofficus.png" width="100px;" alt="Miguel Otero Pedrido"/><br />
        <sub><b>Miguel Otero Pedrido</b></sub>
      </a><br />
      <sub>AI/ML 工程師</sub>
    </td>
  </tr>
</table>

## 授權

本專案採用 MIT 授權 - 詳情請見 [LICENSE](LICENSE) 檔案。

------

<table style="border-collapse: collapse; border: none;">
  <tr style="border: none;">
    <td width="20%" style="border: none;">
      <a href="https://theneuralmaze.substack.com/" aria-label="The Neural Maze">
        <img src="https://avatars.githubusercontent.com/u/151655127?s=400&u=2fff53e8c195ac155e5c8ee65c6ba683a72e655f&v=4" alt="The Neural Maze Logo" width="150"/>
      </a>
    </td>
    <td width="80%" style="border: none;">
      <div>
        <h2>📬 保持更新</h2>
        <p><b><a href="https://theneuralmaze.substack.com/">加入 The Neural Maze</a></b>，學習建構真正有效的 AI 系統，從原理到生產。每週三，直接送到您的收件匣。千萬不要錯過！
</p>
      </div>
    </td>
  </tr>
</table>

<p align="center">
  <a href="https://theneuralmaze.substack.com/">
    <img src="https://img.shields.io/static/v1?label&logo=substack&message=立即訂閱&style=for-the-badge&color=black&scale=2" alt="立即訂閱" height="40">
  </a>
</p>

<table style="border-collapse: collapse; border: none;">
  <tr style="border: none;">
    <td width="20%" style="border: none;">
      <a href="https://decodingml.substack.com/" aria-label="Decoding ML">
        <img src="https://github.com/user-attachments/assets/f2f2f9c0-54b7-4ae3-bf8d-23a359c86982" alt="Decoding ML Logo" width="150"/>
      </a>
    </td>
    <td width="80%" style="border: none;">
      <div>
        <h2>📬 保持更新</h2>
        <p><b><a href="https://decodingml.substack.com/">加入 Decoding ML</a></b>，獲取關於設計、編碼和部署生產級 AI 系統的實證內容，結合軟體工程和 MLOps 的最佳實踐，助您成功交付 AI 應用。每週，直接送到您的收件匣。</p>
      </div>
    </td>
  </tr>
</table>

<p align="center">
  <a href="https://decodingml.substack.com/">
    <img src="https://img.shields.io/static/v1?label&logo=substack&message=立即訂閱&style=for-the-badge&color=black&scale=2" alt="立即訂閱" height="40">
  </a>
</p>

## 🛠️ 常用指令參考

本專案使用 `Makefile` 來簡化常見的開發操作，同時也提供了一些常用的 `docker` 指令，方便您直接與容器互動。

### Make 指令 (在專案根目錄執行)

這些指令定義在專案根目錄的 `Makefile` 中，用於自動化常見任務。

*   **`make infrastructure-build`**
    *   **描述**：建置 Docker 映像。在第一次啟動或 `Dockerfile` 有變更時需要執行。
    *   **用途**：確保所有服務的 Docker 映像是最新的。

*   **`make infrastructure-up`**
    *   **描述**：啟動所有 Docker 服務（遊戲 UI, API, MongoDB）。
    *   **用途**：啟動整個專案的運行環境。

*   **`make infrastructure-stop`**
    *   **描述**：停止所有 Docker 服務。
    *   **用途**：關閉整個專案的運行環境。

*   **`make create-long-term-memory`**
    *   **描述**：填充 AI 代理的長期記憶（從維基百科和史丹佛哲學百科下載資料並寫入 MongoDB）。
    *   **用途**：為 AI 代理提供知識庫，使其能夠進行有意義的對話。

*   **`make delete-long-term-memory`**
    *   **描述**：刪除 MongoDB 中的長期記憶資料。
    *   **用途**：清除長期記憶，例如在需要重新載入資料或重置狀態時。

*   **`make call-agent`**
    *   **描述**：直接呼叫 AI 代理，繞過後端和 UI 邏輯。
    *   **用途**：用於測試 AI 代理的單獨功能。

*   **`make generate-evaluation-dataset`**
    *   **描述**：生成用於評估 AI 代理的資料集。
    *   **用途**：用於 LLMOps 流程中的代理評估。

*   **`make evaluate-agent`**
    *   **描述**：評估 AI 代理的表現。
    *   **用途**：用於 LLMOps 流程中的代理評估。

### Docker 指令 (在終端機執行)

這些是通用的 Docker 命令，用於直接管理容器。

*   **`docker ps`**
    *   **描述**：列出所有正在運行的 Docker 容器。
    *   **用途**：查看容器的狀態、埠映射、名稱等資訊。

*   **`docker ps -a`**
    *   **描述**：列出所有 Docker 容器，包括已停止的。
    *   **用途**：查看所有容器的歷史記錄。

*   **`docker logs [容器名稱或ID]`**
    *   **描述**：查看指定 Docker 容器的日誌輸出。
    *   **範例**：`docker logs philoagents-api`
    *   **用途**：排查容器運行時的錯誤或查看應用程式輸出。

*   **`docker exec [容器名稱或ID] [命令]`**
    *   **描述**：在正在運行的 Docker 容器內部執行命令。
    *   **範例**：`docker exec philoagents-api ls -l /app` (在 `philoagents-api` 容器中列出 `/app` 目錄)
    *   **用途**：在容器內部執行診斷命令、修改配置或運行腳本。

*   **`docker stop [容器名稱或ID]`**
    *   **描述**：停止一個或多個正在運行的 Docker 容器。
    *   **用途**：手動停止特定服務。

*   **`docker start [容器名稱或ID]`**
    *   **描述**：啟動一個或多個已停止的 Docker 容器。
    *   **用途**：手動啟動特定服務。

*   **`docker rm [容器名稱或ID]`**
    *   **描述**：刪除一個或多個 Docker 容器（必須先停止）。
    *   **用途**：清理不再需要的容器。

*   **`docker rmi [映像名稱或ID]`**
    *   **描述**：刪除一個或多個 Docker 映像。
    *   **用途**：清理不再需要的映像。

*   **`docker system prune -a`**
    *   **描述**：刪除所有停止的容器、未使用的網路、懸空映像和（可選）所有未使用的映像。
    *   **用途**：清理 Docker 佔用的磁碟空間。**請謹慎使用此命令，它會刪除所有未使用的 Docker 資源。**