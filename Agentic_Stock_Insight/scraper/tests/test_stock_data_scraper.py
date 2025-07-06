from scraper.stock_data_scraper import StockDataScraper
from unittest.mock import patch

@patch("scraper.stock_data_scraper.yf.Ticker")
def test_fetch_stock_data_sync(mock_ticker):
    mock_ticker().history.return_value = {"Open": 150, "Close": 155}
    scraper = StockDataScraper()
    data = scraper.fetch_stock_data_sync("AAPL")
    assert data["Open"] == 150
    assert data["Close"] == 155

@patch("scraper.stock_data_scraper.StockDataScraper.insert_data_into_db_sync")
def test_scrape_all_tickers(mock_insert):
    scraper = StockDataScraper()
    scraper.scrape_all_tickers(["AAPL", "MSFT"])
    assert mock_insert.call_count == 2
