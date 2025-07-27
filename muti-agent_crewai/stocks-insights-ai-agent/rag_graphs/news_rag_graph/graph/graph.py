from dotenv import load_dotenv
from langgraph.graph import StateGraph,END
from rag_graphs.news_rag_graph.graph.constants import RETRIEVE_NEWS, GENERATE_RESULT, GRADE_DOCUMENT, WEB_SEARCH
from rag_graphs.news_rag_graph.graph.nodes import retrieve, generate, grade_documents, web_search
from rag_graphs.news_rag_graph.graph.state import GraphState
from utils.logger import logger

load_dotenv()

def decide_to_generate(state):
    logger.info("---ASSESS GRADED DOCUMENTS---")
    if state["web_search"]:
        logger.info("""---DECISION: NOT ALL DOCUMENTS ARE RELEVANT TO THE QUESTION, INCLUDE WEB SEARCH---""")
        return WEB_SEARCH
    else:
        logger.info("---DECISION: GENERATE---")
        return GENERATE_RESULT

graph_builder  = StateGraph(state_schema=GraphState)

graph_builder.add_node(RETRIEVE_NEWS, retrieve)
graph_builder.add_node(GRADE_DOCUMENT, grade_documents)
graph_builder.add_node(WEB_SEARCH, web_search)
graph_builder.add_node(GENERATE_RESULT, generate)

graph_builder.add_edge(RETRIEVE_NEWS, GRADE_DOCUMENT)
graph_builder.add_conditional_edges(
    GRADE_DOCUMENT,
    decide_to_generate,
    path_map={
        WEB_SEARCH: WEB_SEARCH,
        GENERATE_RESULT: GENERATE_RESULT
    }
)
graph_builder.add_edge(WEB_SEARCH, GENERATE_RESULT)
graph_builder.add_edge(GENERATE_RESULT, END)

graph_builder.set_entry_point(RETRIEVE_NEWS)

app = graph_builder.compile()
app.get_graph().draw_mermaid_png(output_file_path="news-rag-graph.png")