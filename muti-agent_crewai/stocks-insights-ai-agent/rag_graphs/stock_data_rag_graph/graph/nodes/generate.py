from dotenv import load_dotenv
from typing import Any, Dict
from rag_graphs.stock_data_rag_graph.graph.chains.results_generation import generation_chain
from rag_graphs.stock_data_rag_graph.graph.state import GraphState
from utils.logger import logger

load_dotenv()

def generate(state: GraphState) -> Dict[str, Any]:
    logger.info("---GENERATE RESULTS---")
    question    = state["question"]
    sql_results = state["sql_results"]

    generation  = generation_chain.invoke({
        "context": sql_results,
        "question": question,
    })

    return {
        "sql_results": sql_results,
        "question": question,
        "generation": generation
    }