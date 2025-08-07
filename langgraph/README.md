<picture class="github-only">
  <source media="(prefers-color-scheme: light)" srcset="https://langchain-ai.github.io/langgraph/static/wordmark_dark.svg">
  <source media="(prefers-color-scheme: dark)" srcset="https://langchain-ai.github.io/langgraph/static/wordmark_light.svg">
  <img alt="LangGraph Logo" src="https://langchain-ai.github.io/langgraph/static/wordmark_dark.svg" width="80%">
</picture>

<div>
<br>
</div>

[![Version](https://img.shields.io/pypi/v/langgraph.svg)](https://pypi.org/project/langgraph/)
[![Downloads](https://static.pepy.tech/badge/langgraph/month)](https://pepy.tech/project/langgraph)
[![Open Issues](https://img.shields.io/github/issues-raw/langchain-ai/langgraph)](https://github.com/langchain-ai/langgraph/issues)
[![Docs](https://img.shields.io/badge/docs-latest-blue)](https://langchain-ai.github.io/langgraph/)

受到塑造智能代理未來的公司信賴 – 包括 Klarna、Replit、Elastic 等 – LangGraph 是一個低階編排框架，用於建構、管理和部署長時間運行的有狀態智能代理。

## 快速開始

安裝 LangGraph：

```bash
pip install -U langgraph
```

然後，[使用預建組件](https://langchain-ai.github.io/langgraph/agents/agents/)創建一個智能代理：

```python
# 執行 pip install -qU "langchain[anthropic]" 來呼叫模型

from langgraph.prebuilt import create_react_agent

def get_weather(city: str) -> str:
    """取得指定城市的天氣資訊。"""
    return f"{city} 總是陽光普照！"

# 創建智能代理
agent = create_react_agent(
    model="anthropic:claude-3-7-sonnet-latest",
    tools=[get_weather],
    prompt="你是一個有用的助手"
)

# 運行智能代理
agent.invoke(
    {"messages": [{"role": "user", "content": "舊金山的天氣如何？"}]}
)
```

更多資訊請參閱[快速入門指南](https://langchain-ai.github.io/langgraph/agents/agents/)。或者，要學習如何建構具有可自訂架構、長期記憶和其他複雜任務處理能力的[智能代理工作流程](https://langchain-ai.github.io/langgraph/concepts/low_level/)，請參閱 [LangGraph 基礎教學](https://langchain-ai.github.io/langgraph/tutorials/get-started/1-build-basic-chatbot/)。

## 核心優勢

LangGraph 為*任何*長時間運行的有狀態工作流程或智能代理提供低階支援基礎設施。LangGraph 不會抽象化提示詞或架構，並提供以下核心優勢：

- [持久化執行](https://langchain-ai.github.io/langgraph/concepts/durable_execution/)：建構能夠在故障中持續運行並可長時間執行的智能代理，能自動從中斷點恢復執行。
- [人機協作循環](https://langchain-ai.github.io/langgraph/concepts/human_in_the_loop/)：通過在執行過程中的任何時點檢查和修改代理狀態，無縫整合人工監督。
- [全面記憶系統](https://langchain-ai.github.io/langgraph/concepts/memory/)：創建真正有狀態的智能代理，具備用於持續推理的短期工作記憶和跨會話的長期持久記憶。
- [使用 LangSmith 除錯](http://www.langchain.com/langsmith)：通過視覺化工具深入了解複雜的代理行為，追蹤執行路徑、捕獲狀態轉換並提供詳細的運行時指標。
- [生產就緒部署](https://langchain-ai.github.io/langgraph/concepts/deployment_options/)：使用專為處理有狀態長時間運行工作流程獨特挑戰而設計的可擴展基礎設施，自信地部署複雜的代理系統。

## LangGraph 生態系統

雖然 LangGraph 可以獨立使用，但它也能與任何 LangChain 產品無縫整合，為開發者提供完整的工具套件來建構智能代理。為了改善您的 LLM 應用程式開發，請將 LangGraph 與以下工具搭配使用：

- [LangSmith](http://www.langchain.com/langsmith) — 有助於代理評估和可觀測性。除錯性能不佳的 LLM 應用程式運行、評估代理軌跡、獲得生產環境的可見性，並隨時間改善性能。
- [LangGraph Platform](https://langchain-ai.github.io/langgraph/concepts/langgraph_platform/) — 使用專為長時間運行有狀態工作流程而構建的部署平台，輕鬆部署和擴展智能代理。在團隊間發現、重用、配置和共享代理 — 並在 [LangGraph Studio](https://langchain-ai.github.io/langgraph/concepts/langgraph_studio/) 中通過視覺化原型快速迭代。
- [LangChain](https://python.langchain.com/docs/introduction/) – 提供整合和可組合的組件，簡化 LLM 應用程式開發。

> [!NOTE]
> 尋找 LangGraph 的 JavaScript 版本？請參閱 [JS 儲存庫](https://github.com/langchain-ai/langgraphjs) 和 [JS 文檔](https://langchain-ai.github.io/langgraphjs/)。

## 其他資源

- [指南](https://langchain-ai.github.io/langgraph/how-tos/)：針對串流、添加記憶與持久化、設計模式（如分支、子圖等）等主題的快速、可操作程式碼片段。
- [參考文檔](https://langchain-ai.github.io/langgraph/reference/graphs/)：核心類別、方法、如何使用圖形和檢查點 API，以及高階預建組件的詳細參考。
- [範例](https://langchain-ai.github.io/langgraph/examples/)：LangGraph 入門的指導範例。
- [LangChain 論壇](https://forum.langchain.com/)：與社群聯繫，分享您所有的技術問題、想法和回饋。
- [LangChain 學院](https://academy.langchain.com/courses/intro-to-langgraph)：在我們免費的結構化課程中學習 LangGraph 基礎知識。
- [模板](https://langchain-ai.github.io/langgraph/concepts/template_applications/)：常見代理工作流程（如 ReAct 代理、記憶、檢索等）的預建參考應用程式，可以複製和調整。
- [案例研究](https://www.langchain.com/built-with-langgraph)：了解行業領導者如何使用 LangGraph 大規模部署 AI 應用程式。

## 致謝

LangGraph 的靈感來自 [Pregel](https://research.google/pubs/pub37252/) 和 [Apache Beam](https://beam.apache.org/)。公共介面的設計靈感來自 [NetworkX](https://networkx.org/documentation/latest/)。LangGraph 由 LangChain Inc（LangChain 的創建者）開發，但也可以在不使用 LangChain 的情況下獨立使用。