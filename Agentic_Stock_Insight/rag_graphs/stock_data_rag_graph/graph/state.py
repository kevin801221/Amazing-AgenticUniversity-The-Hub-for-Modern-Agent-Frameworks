from typing import List, TypedDict



class GraphState(TypedDict):
    """
    Represents the state of our graph

    Attributes:
        question: Qustion
        generation: LLM generation
        web_seach: Whether to search the web for additional info
        documents: List of documents
    """
    question: str
    sql_query: str
    sql_results: str
    generation: str
