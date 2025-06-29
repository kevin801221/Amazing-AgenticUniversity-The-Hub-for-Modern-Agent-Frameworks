from abc import ABC, abstractmethod

class GenericScraper(ABC):
    """
    Abstract scraper interface defining common methods.
    """
    @abstractmethod
    def scrape_all_tickers(self, **kwargs):
        pass
