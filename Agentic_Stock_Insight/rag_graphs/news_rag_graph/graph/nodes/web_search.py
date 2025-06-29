from typing import Any, Dict
from dotenv import load_dotenv
from langchain_community.tools import TavilySearchResults
from rag_graphs.news_rag_graph.graph.state import GraphState
from langchain.schema import Document
from utils.logger import logger

load_dotenv()

web_search_tool = TavilySearchResults(max_results=3)

def web_search(state:GraphState) -> Dict[str, Any]:
    logger.info("---WEB SEARCH---")
    question    = state["question"]
    documents   = state["documents"]

    tavily_results = web_search_tool.invoke({"query": question})
    joined_tavily_result    = "\n".join(
        [tavily_result["content"] for tavily_result in tavily_results]
    )

    web_results = Document(page_content=joined_tavily_result)
    if documents is not None:
        documents.append(web_results)
    else:
        documents   = [web_results]

    return {"documents": documents, "question": question}

if __name__ == "__main__":
    web_search(state={"question":"agent memory", "documents":None})
