from fastapi import APIRouter, HTTPException, Query
from rag_graphs.stock_data_rag_graph.graph.graph import app as stock_data_graph
from rag_graphs.stock_charts_graph.graph.graph import app as stock_charts_graph
router = APIRouter()
#

@router.get("/{ticker}/price-stats")
def price_stats(
    ticker: str,
    operation: str  = Query(..., description="Operation to perform: 'highest', 'lowest', 'average'"),
    price_type: str = Query(..., description="Price type: 'open', 'close', 'low', 'high'"),
    duration :str   = Query(..., description="Duration (days): '1', '7', '14', '30'"),
):
    """
    Get stock price statistics for a specific ticker.

    Args:
        ticker (str): Stock ticker symbol.
        operation (str): Operation to perform (e.g., 'highest', 'lowest', 'average').
        price_type (str): Type of price (e.g., 'open', 'close', 'low', 'high').
        duration (int): Number of days

    Returns:
        dict: Stock data with the requested statistics.
    """

    try:
        human_query = f"What is the {operation} value of {price_type} for '{ticker}' over last {duration} day(s) ?"

        res         = stock_data_graph.invoke({"question": human_query})
        return {
            "ticker": ticker,
            "operation": operation,
            "price_type": price_type,
            "duration": duration,
            "result": res['generation']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/{ticker}/chart")
def chart(
    ticker: str,
    price_type: str = Query(..., description="Price type: 'open', 'close', 'low', 'high'"),
    duration :str   = Query(..., description="Duration (days): '1', '7', '14', '30'"),

):
    """
    Get stock price statistics and return a histogram/chart for a specific ticker.

    Args:
        ticker (str): Stock ticker symbol.
        price_type (str): Type of price (e.g., 'open', 'close', 'low', 'high').
        duration (int): Number of days

    Returns:
        dict: Stock data with the requested statistics.
    """

    try:
        human_query = f"All unique values of 'date' and {price_type} for '{ticker}' for last {duration} day(s)"

        res         = stock_charts_graph.invoke({"question": human_query})
        return {
            "ticker": ticker,
            "price_type": price_type,
            "duration": duration,
            "result": res['sql_results']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
