# 建立 MCP PRP (Create MCP PRP)

為 MCP（多重上下文提示）功能產生一份完整的 PRP。

## 功能檔案: $ARGUMENTS

## 研究與產生流程

1.  **分析需求**:
    -   閱讀功能檔案以了解需要建立什麼。
    -   特別注意 MCP 模式的具體要求，例如代理類型、工具和資料庫互動。

2.  **程式碼庫分析**:
    -   搜尋 `mcp-server` 中的現有模式。
    -   參考 `src/tools/database/` 和 `src/database/` 以了解資料庫互動。
    -   檢查 `tests/` 中的測試模式。

3.  **PRP 產生**:
    -   使用 `PRPs/templates/prp_mcp_base.md` 作為模板。
    -   **關鍵上下文**:
        -   包含 `ai_docs/mcp_patterns.md` 的參考。
        -   提供 `examples/database-tools.ts` 的程式碼片段。
        -   記錄要遵循的現有模式。
    -   **實作藍圖**:
        -   清晰地定義要建立的工具 (`@agent.tool`)。
        -   說明資料庫互動的邏輯。
        -   列出需要完成的具體任務。
    -   **驗證關卡**:
        -   提供可執行的 `vitest` 指令來驗證實作。

## 輸出
儲存為: `PRPs/{feature-name}.md`

## 品質檢查清單
- [ ] 是否包含了所有必要的 MCP 上下文？
- [ ] 驗證指令是否可由 Gemini 執行？
- [ ] 是否引用了現有的資料庫和工具模式？
- [ ] 實作路徑是否清晰？

記住：目標是透過全面的上下文，讓 Gemini 能夠一次性成功實作。