from scraper.scraper_factory import StockScraperFactory, NewsScraperFactory

def test_stock_scraper_factory_integration():
    factory = StockScraperFactory()
    scraper = factory.create_scraper()
    scraper.scrape_all_tickers(["AAPL", "GOOG"])

def test_news_scraper_factory_integration():
    factory = NewsScraperFactory()
    scraper = factory.create_scraper(collection_name="test_collection", scrape_num_articles=2)
    scraper.scrape_all_tickers(["AAPL", "MSFT"])
