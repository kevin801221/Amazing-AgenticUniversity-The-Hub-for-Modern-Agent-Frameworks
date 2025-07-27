import asyncio
from unittest.mock import patch
from rest_api.main import run_scrapers_in_background, scrape_in_interval
import pytest

@patch("scraper.scraper_factory.StockScraperFactory.create_scraper")
@patch("scraper.scraper_factory.NewsScraperFactory.create_scraper")
@patch("rag_graphs.news_rag_graph.ingestion.DocumentSyncManager.sync_documents")
@pytest.mark.asyncio
async def test_run_scrapers_in_background(mock_sync, mock_news_scraper, mock_stock_scraper):
    mock_news_scraper().scrape_all_tickers = lambda x: None
    mock_stock_scraper().scrape_all_tickers = lambda x: None

    await run_scrapers_in_background()
    mock_sync.assert_called_once()

@patch("main.run_scrapers_in_background")
@pytest.mark.asyncio
async def test_scrape_in_interval(mock_run_scrapers):
    mock_run_scrapers.return_value = None
    interval = 2
    task = asyncio.create_task(scrape_in_interval(interval))
    await asyncio.sleep(3)  # Allow the interval to trigger
    task.cancel()
    mock_run_scrapers.assert_called()
