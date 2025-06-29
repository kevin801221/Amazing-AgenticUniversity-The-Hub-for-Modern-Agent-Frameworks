# Code for retrieval node
from typing import Any, Dict
from rag_graphs.stock_data_rag_graph.graph.state import GraphState
from rag_graphs.stock_data_rag_graph.graph.chains.sql_generation_chain import sql_generation_chain
from utils.logger import logger
import re


def clean_sql_string(input_sql_query):
    input_sql_query = input_sql_query.replace('\n', ' ')

    # Extract the SQL query
    match = re.search(r"```sql\s+(.*?)\s+```", input_sql_query, re.DOTALL)
    if match:
        sql_query = match.group(1)
        return (sql_query)
    else:
        return input_sql_query


def generate_sql(state:GraphState)->Dict[str, Any]:
    logger.info("---GENERATE SQL---")
    question    = state['question']
    generated_sql   = sql_generation_chain.invoke(question)
    clean_sql_query = clean_sql_string(generated_sql)
    return {"sql_query": clean_sql_query, "question": question}