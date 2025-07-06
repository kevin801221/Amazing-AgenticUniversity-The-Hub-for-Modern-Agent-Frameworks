from unittest.mock import patch
from fastapi.testclient import TestClient
from rest_api.main import app

client = TestClient(app)

@patch("rag_graphs.news_rag_graph.graph.graph.app.invoke")
def test_news_by_topic(mock_invoke):
    mock_invoke.return_value = {"generation": ["News about AI for AAPL"]}

    response = client.get("/news/AAPL", params={"topic": "AI"})
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "AAPL"
    assert data["topic"] == "AI"
    assert "News about AI for AAPL" in data["result"]

@patch("rag_graphs.news_rag_graph.graph.graph.app.invoke")
def test_news_no_topic(mock_invoke):
    mock_invoke.return_value = {"generation": ["General news about AAPL"]}

    response = client.get("/news/AAPL")
    assert response.status_code == 200
    data = response.json()
    assert data["ticker"] == "AAPL"
    assert data["topic"] is None
    assert "General news about AAPL" in data["result"]

def test_news_route_error_handling():
    response = client.get("/news/AAPL", params={"topic": "InvalidTopic"})
    assert response.status_code in {400, 500}  # Assuming exception leads to 500
