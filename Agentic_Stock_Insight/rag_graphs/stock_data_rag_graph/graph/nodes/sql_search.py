from typing import Any, Dict
from dotenv import load_dotenv
from db.postgres_db import PostgresDBClient
from rag_graphs.stock_data_rag_graph.graph.state import GraphState
# from sqlalchemy import create_engine, text
import os
import pandas as pd
from utils.logger import logger

load_dotenv()

def initialize_db_client():
    """
    Initialize the PostgresDBClient using .env credentials.
    """
    user = os.getenv("POSTGRES_USERNAME")
    password = os.getenv("POSTGRES_PASSWORD")
    host = os.getenv("POSTGRES_HOST")
    port = os.getenv("POSTGRES_PORT", 5432)  # Default to 5432 if not specified
    db_name = os.getenv("POSTGRES_DB")

    return PostgresDBClient(
        host=host,
        database=db_name,
        user=user,
        password=password,
        port=port
    )


def execute_query(query: str, params: dict = None):
    """
    Execute a SQL query using PostgresDBClient and return results as a DataFrame.

    Args:
        query (str): The SQL query to execute.
        params (dict, optional): Parameters for the query.

    Returns:
        pd.DataFrame: The query results as a Pandas DataFrame.
    """
    db_client   = initialize_db_client()
    try:
        if "select" in query.lower():  # For SELECT queries
            results, columns = db_client.fetch_query(query, params)
            if not columns:  # Handle case where no columns are returned
                logger.warning("Query returned no columns.")
                return pd.DataFrame()  # Return an empty DataFrame
            return pd.DataFrame(results, columns=columns)
        else:  # For other queries (INSERT, UPDATE, DELETE)
            db_client.execute_query(query, params)
            return pd.DataFrame()  # Return an empty DataFrame for non-SELECT
    except Exception as e:
        logger.error(f"Error executing query: {e}")
        raise



def sql_fetch_query(state:GraphState) -> Dict[str, Any]:
    logger.info("---SQL SEARCH---")
    sql_query               = state["sql_query"]
    sql_results             = execute_query(sql_query)

    return {"sql_results": sql_results, "sql_query": sql_query}

