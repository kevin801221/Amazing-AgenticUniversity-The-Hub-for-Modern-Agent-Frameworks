from dotenv import load_dotenv
from rag_graphs.stock_charts_graph.graph.graph import app
from utils.logger import logger

load_dotenv()

if __name__=='__main__':
    logger.info("--STOCK CHARTS CHAIN--")
    res = app.invoke({"question": "All unique values of 'Date' and 'Low' of AAPL for last 7 days"})
    print(res)