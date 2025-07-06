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
    generation: str
    web_seach: bool
    documents: List[str]
