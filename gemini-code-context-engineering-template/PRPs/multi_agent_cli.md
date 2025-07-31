{
  "name": "PRPs/multi_agent_cli.md",
  "confidence_score": "8/10 (Gmail API 的 OAuth 流程是主要複雜點，但透過詳細指引可以克服)",
  "purpose": "建立一個 Pydantic AI 代理，該代理使用另一個 Pydantic AI 代理作為其工具。主代理負責研究，子代理負責起草電子郵件。提供一個 CLI 介面與主代理互動。",
  "core_principles": [
    "Gemini Optimized: 專為 Google Gemini 模型設計。",
    "`uv` for Environments: 強制使用 `uv` 管理 Python 環境。",
    "Multi-Agent Pattern: 實作一個代理作為另一個代理工具的模式。",
    "External API Integration: 整合 Brave Search API 和 Gmail API。",
    "Clear Documentation: 提供完整的 `README.md`，包含設定和使用說明。"
  ],
  "goal": "使用者可以透過 CLI 下達一個複雜指令，例如「研究 Pydantic V2 的新功能，並草擬一封郵件給團隊介紹這些功能」。主代理將使用 Brave API 進行研究，然後呼叫子代理，使用 Gmail API 將研究結果草擬成一封電子郵件。",
  "why": "這個專案旨在展示一個更進階的 AI 代理使用案例，即代理之間的協作。這能解決需要多個獨立技能來完成的複雜任務，並將不同功能（如搜尋和通訊）解耦。",
  "what": {
    "agent_type_classification": [
      "Tool-Enabled Agent (工具型代理)",
      "Workflow Agent (工作流代理)"
    ],
    "model_provider_requirements": [
      "Google: `gemini-1.5-pro` (預設)"
    ],
    "external_integrations": [
      "Brave Search API: 用於網路研究。",
      "Gmail API: 用於草擬電子郵件。"
    ],
    "success_criteria": [
      "專案結構已建立，並使用 `uv` 設定好環境。",
      "Brave Search API 工具能成功執行並回傳搜尋結果。",
      "Gmail API 工具能成功在使用者帳戶中建立一封草稿郵件。",
      "主代理能成功呼叫子代理作為工具。",
      "CLI 介面能接收使用者輸入，並成功觸發整個工作流程。",
      "`README.md` 包含清晰的設定指南，特別是關於如何取得 Brave API 金鑰和設定 Gmail OAuth 2.0。"
    ]
  },
  "all_needed_context": {
    "pydantic_ai_documentation_research": [
      {
        "url": "https://ai.pydantic.dev/",
        "why": "官方文件，包含代理建立、模型提供商和工具整合的基礎知識。"
      },
      {
        "url": "https://brave.com/search/api/",
        "why": "Brave Search API 的官方文件，了解如何取得 API 金鑰和進行查詢。"
      },
      {
        "url": "https://developers.google.com/gmail/api/quickstart/python",
        "why": "Gmail API 的 Python 快速入門指南。這是最重要的參考，因为它解釋了 OAuth 2.0 的設定流程。"
      },
      {
        "url": "https://developers.google.com/gmail/api/guides/drafts",
        "why": "關於如何使用 Gmail API 建立和管理草稿的具體文件。"
      },
      {
        "path": "examples/main_agent_reference/",
        "why": "這是建立 Pydantic AI 代理的最佳實踐參考，展示了如何處理設定、依賴和工具。"
      },
      {
        "path": "examples/cli.py",
        "why": "作為建立此專案 CLI 介面的模板和靈感來源。"
      }
    ],
    "agent_architecture_research": {
      "agent_structure": {
        "main_agent_research_agent": {
          "description": "接收使用者指令，進行研究，並呼叫郵件代理來草擬郵件。",
          "tools": [
            "brave_search(query: str) -> str",
            "draft_email(to: str, subject: str, body: str) -> str  # 這個工具會觸發子代理"
          ]
        },
        "sub_agent_email_agent": {
          "description": "一個專門用來草擬 Gmail 郵件的代理。",
          "tools": [
            "create_gmail_draft(to: str, subject: str, body: str) -> str"
          ]
        }
      },
      "implementation_gotchas": {
        "gmail_oauth": {
          "issue": "Gmail API 不像 Brave 那樣使用簡單的 API 金鑰。它需要 OAuth 2.0 授權。",
          "solution": "必須引導使用者從 Google Cloud Console 取得 `credentials.json`。\n首次執行時，應用程式會打開瀏覽器要求使用者授權，並產生一個 `token.json` 檔案用於後續的 API 呼叫。\n這個流程必須在 `README.md` 中詳細說明，並在程式碼中妥善處理。"
        }
      }
    }
  },
  "implementation_blueprint": [
    "Implementation Task 1 - 專案與環境設定: CREATE project directory `use-cases/multi_agent_cli/`. CREATE `requirements.txt` with: pydantic-ai, google-api-python-client, google-auth-oauthlib, python-dotenv, brave-search-api-client. CREATE `.env.example` with `BRAVE_API_KEY=YOUR_API_KEY_HERE`. INITIALIZE environment with `uv venv` and `uv pip install -r requirements.txt`.",
    "Implementation Task 2 - Gmail 工具與設定: CREATE `multi_agent_cli/gmail_tools.py`. IMPLEMENT a function `get_gmail_service()` to handle the OAuth 2.0 flow (reading `credentials.json` and creating/reading `token.json`). IMPLEMENT a tool function `create_gmail_draft(service, to, subject, body)` that uses the service object to create a draft.",
    "Implementation Task 3 - 郵件草稿子代理: CREATE `multi_agent_cli/email_agent.py`. DEFINE a Pydantic AI agent `email_agent`. ADD the `create_gmail_draft` function as a tool to this agent.",
    "Implementation Task 4 - 研究工具: CREATE `multi_agent_cli/research_tools.py`. IMPLEMENT a tool function `brave_search(query)` that takes a query string and returns search results using the Brave Search API.",
    "Implementation Task 5 - 主要研究代理: CREATE `multi_agent_cli/research_agent.py`. DEFINE the main Pydantic AI agent `research_agent`. ADD the `brave_search` tool. IMPLEMENT a second tool `draft_email` which, when called, will execute the `email_agent` with the provided arguments.",
    "Implementation Task 6 - CLI 介面: CREATE `multi_agent_cli/cli.py`. REFERENCE `examples/cli.py` to build the command-line interface. The CLI should take a string input from the user, pass it to the `research_agent`, and print the final result.",
    "Implementation Task 7 - 文件: CREATE `multi_agent_cli/README.md`. DOCUMENT the project structure. PROVIDE step-by-step instructions on how to set up the `uv` environment. PROVIDE detailed instructions on how to get a Brave API key. PROVIDE very detailed instructions on how to get the `credentials.json` file from Google Cloud Console for the Gmail API."
  ],
  "validation_loop": [
    "# Level 1: 環境和結構驗證",
    "cd use-cases/multi_agent_cli",
    "uv venv && source .venv/bin/activate",
    "uv pip install -r requirements.txt",
    "test -f cli.py && echo '✅ CLI present'",
    "test -f research_agent.py && echo '✅ Research agent present'",
    "test -f email_agent.py && echo '✅ Email agent present'",
    "# Level 2: 工具單元測試 (需要 Mocking)",
    "# 建立 tests/test_tools.py",
    "# uv run pytest tests/ -v",
    "# (這一步在 PRP 執行階段實作)",
    "# Level 3: 手動端對端測試",
    "# 1. 設定好 .env 和 credentials.json",
    "# 2. 執行 CLI",
    "python multi_agent_cli/cli.py \"Research the latest news on Gemini 1.5 Pro and draft an email to test@example.com summarizing the key points.\"",
    "# 預期：CLI 應輸出成功訊息，並在 Gmail 中看到一封新的草稿郵件。"
  ]
}