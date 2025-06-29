from fastapi import APIRouter, HTTPException, Query
from rag_graphs.news_rag_graph.graph.graph import app
router = APIRouter()

@router.get("/{ticker}")
def news_by_topic(
    ticker: str,
    # Optional query parameter
    topic: str  = Query(None, description="Topic"),
):
    """
    Get news a specific ticker.

    Args:
        ticker (str): Stock ticker symbol.
        topic (str): Topic to fetch news for a specific stock.

    Returns:
        dict: Relevant news for a speicific ticker.
    """

    try:

        if topic:
            human_query = f"News related to {topic} for {ticker}"
        else:
            human_query = f"News related to {ticker}"

        res         = app.invoke({"question": human_query})
        return {
            "ticker": ticker,
            "topic": topic,
            "result": res["generation"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))