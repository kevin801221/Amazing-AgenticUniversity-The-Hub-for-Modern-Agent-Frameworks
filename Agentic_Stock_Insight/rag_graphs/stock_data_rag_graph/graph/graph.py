from dotenv import load_dotenv
from langgraph.graph import StateGraph,END
from rag_graphs.stock_data_rag_graph.graph.constants import GENERATE_SQL, EXECUTE_SQL, GENERATE_RESULTS
from rag_graphs.stock_data_rag_graph.graph.state import GraphState
from rag_graphs.stock_data_rag_graph.graph.nodes.generate_sql import generate_sql
from rag_graphs.stock_data_rag_graph.graph.nodes.sql_search import sql_fetch_query
from rag_graphs.stock_data_rag_graph.graph.nodes.generate import generate


load_dotenv()


graph_builder  = StateGraph(state_schema=GraphState)

graph_builder.add_node(GENERATE_SQL, generate_sql)
graph_builder.add_node(EXECUTE_SQL, sql_fetch_query)
graph_builder.add_node(GENERATE_RESULTS, generate)

graph_builder.set_entry_point(GENERATE_SQL)
graph_builder.add_edge(GENERATE_SQL, EXECUTE_SQL)
graph_builder.add_edge(EXECUTE_SQL, GENERATE_RESULTS)
graph_builder.add_edge(GENERATE_RESULTS, END)


app = graph_builder.compile()
app.get_graph().draw_mermaid_png(output_file_path="stock-data-rag-graph.png")