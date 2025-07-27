import asyncio

from db.postgres_db import PostgresDBClient
from utils.logger import logger
import yfinance as yf
from dotenv import load_dotenv
import os

class StockDataScraper:
    def __init__(self):
        self.db_client = self.initialize_db_client()

    @staticmethod
    def initialize_db_client():
        """
        Initialize the PostgresDBClient using .env credentials.
        """
        load_dotenv()  # Load environment variables
        user = os.getenv("POSTGRES_USERNAME")
        password = os.getenv("POSTGRES_PASSWORD")
        host = os.getenv("POSTGRES_HOST")
        port = os.getenv("POSTGRES_PORT", 5432)  # Default to 5432
        db_name = os.getenv("POSTGRES_DB")

        return PostgresDBClient(
            host=host,
            database=db_name,
            user=user,
            password=password,
            port=port,
        )

    def fetch_stock_data_sync(self, ticker, period='1mo'):
        """
        Synchronously fetches historical stock data for a given ticker.
        """
        ticker_data = yf.Ticker(ticker)
        return ticker_data.history(period=period)

    def insert_data_into_db(self, ticker, historical_data):
        """
        Inserts historical stock data for a given ticker into the database using PostgresDBClient.
        """
        try:
            for date, row in historical_data.iterrows():
                data = {
                    "ticker": ticker,
                    "date": date.date(),
                    "open": row["Open"],
                    "high": row["High"],
                    "low": row["Low"],
                    "close": row["Close"],
                    "volume": row["Volume"],
                }
                self.db_client.create("stock_data", data)  # Assuming table is named `stock_data`
            logger.info(f"Data for {ticker} successfully inserted into the database.")
        except Exception as e:
            logger.error(f"Error inserting data for {ticker}: {e}")
            raise

    def scrape_all_tickers(self, tickers):
        """
        Fetches and stores stock data for all tickers.
        """
        for ticker in tickers:
            try:
                logger.info(f"Scraping data for {ticker}...")
                historical_data = self.fetch_stock_data_sync(ticker)
                self.insert_data_into_db(ticker, historical_data)
            except Exception as e:
                logger.error(f"Error scraping data for {ticker}: {e}")

# Example usage
if __name__ == "__main__":
    top_50_tickers = [
        "AAPL", "MSFT", "GOOG", "AMZN", "TSLA", "NVDA", "BRK-B", "META",
        "UNH", "JNJ", "V", "PG", "XOM", "JPM", "WMT", "MA", "CVX", "LLY",
        "PFE", "HD", "KO", "ABBV", "PEP", "MRK", "BAC", "TMO", "AVGO",
        "COST", "DIS", "CSCO", "DHR", "TMUS", "MCD", "ADBE", "NFLX",
        "CMCSA", "TXN", "NKE", "PM", "VZ", "INTC", "ORCL", "QCOM",
        "ABT", "WFC", "LIN", "BMY", "ACN", "UPS", "RTX"
    ]

    scraper = StockDataScraper()
    scraper.scrape_all_tickers(top_50_tickers)
