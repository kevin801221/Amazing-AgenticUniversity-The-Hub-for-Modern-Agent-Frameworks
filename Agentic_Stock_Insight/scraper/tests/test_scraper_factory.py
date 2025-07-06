from scraper.scraper_factory import StockScraperFactory, NewsScraperFactory
from scraper.news_scraper import NewsScraper
from scraper.stock_data_scraper import StockDataScraper

def test_stock_scraper_factory():
    factory = StockScraperFactory()
    scraper = factory.create_scraper()
    assert isinstance(scraper, StockDataScraper)

def test_news_scraper_factory():
    factory = NewsScraperFactory()
    scraper = factory.create_scraper(collection_name="test_collection", scrape_num_articles=5)
    assert isinstance(scraper, NewsScraper)
    assert scraper.collection_name == "test_collection"
    assert scraper.scrape_num_articles == 5
