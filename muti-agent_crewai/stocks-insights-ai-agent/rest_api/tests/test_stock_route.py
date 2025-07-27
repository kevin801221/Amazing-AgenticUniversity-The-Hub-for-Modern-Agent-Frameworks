from unittest.mock import patch
from fastapi.testclient import TestClient
from rest_api.main import app

client = TestClient(app)

@patch("rag_graphs.stock_data_rag_graph.graph.graph.app.invoke")
def test_stock_price_stats(mock_invoke):
    mock_invoke.return_value = {"generation": ["The highest close price is 150"]}

    response = client.get(
        "/stock/AAPL/price-stats",
        params={"operation": "highest", "price_type": "close", "duration": "7"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "AAPL"
    assert data["operation"] == "highest"
    assert data["price_type"] == "close"
    assert data["duration"] == "7"
    assert "The highest close price is 150" in data["result"]

def test_stock_price_stats_error_handling():
    response = client.get(
        "/stock/INVALID/price-stats",
        params={"operation": "highest", "price_type": "close", "duration": "7"}
    )
    assert response.status_code in {400, 500}  # Assuming exception leads to 500
