from dotenv import load_dotenv
from rag_graphs.news_rag_graph.graph.graph import app
from utils.logger import logger

load_dotenv()

if __name__=='__main__':
    logger.info("--STOCK NEWS GRAPH--")
    res = app.invoke({"question": "Documents related to Apple"})
