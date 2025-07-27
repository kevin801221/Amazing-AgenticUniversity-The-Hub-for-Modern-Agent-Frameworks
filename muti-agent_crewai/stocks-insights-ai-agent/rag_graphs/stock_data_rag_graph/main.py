from dotenv import load_dotenv
from rag_graphs.stock_data_rag_graph.graph.graph import app
from utils.logger import logger

load_dotenv()

if __name__=='__main__':
    logger.info("--STOCK DATA CHAIN--")
    res = app.invoke({"question": "What is the lowest price of AAPL over last 7 days?"})
    print(res)