import os
import re
import requests
from time import sleep
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from db.mongo_db import MongoDBClient
from scraper.generic_scraper import GenericScraper
from utils.logger import logger

class NewsScraper(GenericScraper):
    def __init__(self, collection_name, scrape_num_articles=1):
        """
        Initialize the NewsScraper with necessary parameters.
        """
        self.headers    = {
            'accept': '*/*',
            'accept-encoding': 'gzip, deflate, br',
            'accept-language': 'en-US,en;q=0.9',
            'referer': 'https://www.google.com',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.83 Safari/537.36 Edg/85.0.564.44'
        }

        self.collection_name        = collection_name
        self.scrape_num_articles    = scrape_num_articles
        self.mongo_client           = MongoDBClient()


    @staticmethod
    def extract_article(card):
        """
        Extract article information from the raw HTML.
        """
        headline        = card.find('h4', 's-title').text
        source          = card.find("span", 's-source').text
        posted          = card.find('span', 's-time').text.replace('·', '').strip()
        description     = card.find('p', 's-desc').text.strip()
        raw_link        = card.find('a').get('href')
        unquoted_link   = requests.utils.unquote(raw_link)
        pattern         = re.compile(r'RU=(.+)\/RK')
        clean_link      = re.search(pattern, unquoted_link).group(1)

        return {
            'headline': headline,
            'source': source,
            'posted': posted,
            'description': description,
            'link': clean_link,
            'synced': False
        }

    def scrape_articles(self, search_query):
        """
        Scrape news articles for a specific search query.
        """
        template    = 'https://news.search.yahoo.com/search?p={}'
        url         = template.format(search_query)
        articles    = []
        links       = set()
        num_search  = self.scrape_num_articles

        while num_search:
            num_search -= 1
            response    = requests.get(url, headers=self.headers)
            soup        = BeautifulSoup(response.text, 'html.parser')
            cards       = soup.find_all('div', 'NewsArticle')

            # Extract articles from the page
            for card in cards:
                article = self.extract_article(card)
                link    = article['link']
                if link not in links:
                    links.add(link)
                    articles.append(article)

            # Find the next page
            try:
                url = soup.find('a', 'next').get('href')
                sleep(1)
            except AttributeError:
                break

        # Insert articles into MongoDB
        if articles:
            self.mongo_client.insert_many(self.collection_name, articles)
            logger.info(f"Inserted {len(articles)} articles into MongoDB.")

        return articles

    def scrape_all_tickers(self, tickers):
        """
        Scrape news articles for a list of tickers.
        """
        for ticker in tickers:
            logger.info(f"Scraping news for ticker: {ticker}")
            try:
                self.scrape_articles(ticker)
            except Exception as e:
                logger.error(f"Error while scraping news for {ticker}: {e}")


if __name__ == "__main__":

    # Initialize the scraper
    scraper = NewsScraper(
        collection_name = os.getenv("COLLECTION_NAME"),
        scrape_num_articles = int(os.getenv("SCRAPE_NUM_ARTICLES", 1))
    )

    # List of tickers to scrape
    top_50_tickers = [
        "AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "BRK-B", "META",
        "UNH", "JNJ", "V", "PG", "XOM", "JPM", "WMT", "MA", "CVX", "LLY",
        "PFE", "HD", "KO", "ABBV", "PEP", "MRK", "BAC", "TMO", "AVGO",
        "COST", "DIS", "CSCO", "DHR", "TMUS", "MCD", "ADBE", "NFLX",
        "CMCSA", "TXN", "NKE", "PM", "VZ", "INTC", "ORCL", "QCOM",
        "ABT", "WFC", "LIN", "BMY", "ACN", "UPS", "RTX"
    ]

    # Scrape all tickers
    scraper.scrape_all_tickers(top_50_tickers)
