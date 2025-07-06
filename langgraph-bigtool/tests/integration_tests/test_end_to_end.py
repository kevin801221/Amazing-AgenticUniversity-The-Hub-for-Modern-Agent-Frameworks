from langchain.chat_models import init_chat_model
from langchain.embeddings import init_embeddings

from tests.unit_tests.test_end_to_end import run_end_to_end_test


def test_end_to_end() -> None:
    llm = init_chat_model("openai:gpt-4o")
    embeddings = init_embeddings("openai:text-embedding-3-small")
    run_end_to_end_test(llm, embeddings)
