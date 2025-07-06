from dotenv import load_dotenv
from typing import Any, Dict
from rag_graphs.news_rag_graph.graph.chains.generation import generation_chain
from rag_graphs.news_rag_graph.graph.state import GraphState
from utils.logger import logger

load_dotenv()

def generate(state: GraphState) -> Dict[str, Any]:
    logger.info("---GENERATE---")
    question    = state["question"]
    documents   = state["documents"]

    generation  = generation_chain.invoke({
        "context": documents,
        "question": question,
    })

    return {
        "documents": documents,
        "question": question,
        "generation": generation
    }