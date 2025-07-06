from pprint import pprint

from dotenv import load_dotenv

from graph.chains.retrieval_grader import GradeDocuments, retrieval_grader
from graph.chains.generation import generation_chain
from ingestion import retriever

load_dotenv()


def test_retrieval_grader_answer_yes()->None:
    question    = "agent memory"
    docs        = retriever.invoke(question)
    doc_txt     = docs[0].page_content

    res: GradeDocuments = retrieval_grader.invoke(
        {"question": question, "document": doc_txt}
    )

    assert res.binary_score=="yes"

def test_retrieval_grader_answer_no()->None:
    question    = "agent memory"
    docs        = retriever.invoke(question)
    doc_txt     = docs[0].page_content

    res: GradeDocuments = retrieval_grader.invoke(
        {"question": "How to make pizza", "document": doc_txt}
    )

    assert res.binary_score=="no"

def test_generation_chain():
    question    = "agent memory"
    docs        = retriever.invoke(question)
    res         = generation_chain.invoke({
        "context": docs,
        "question": question

    })
    pprint(res)
    assert True
