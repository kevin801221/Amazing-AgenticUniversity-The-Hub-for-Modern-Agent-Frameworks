from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi import Request
from fastapi.templating import Jinja2Templates
from dotenv import load_dotenv
from config.config_loader import ConfigLoader
from rag_graphs.news_rag_graph.ingestion import DocumentSyncManager
from rest_api.routes import stock_routes, news_routes
from utils.logger import logger
from scraper.scraper_factory import StockScraperFactory, NewsScraperFactory
from datetime import datetime

import asyncio
import os

# Load .env
load_dotenv()

# Initialize FastAPI
app = FastAPI()
templates = Jinja2Templates(directory="templates")

# Initialize ConfigLoader
config_loader = ConfigLoader(config_file="config/config.json")

# Load configurations
SCRAPE_TICKERS = config_loader.get("SCRAPE_TICKERS")
SCRAPING_INTERVAL = config_loader.get("SCRAPING_INTERVAL", 3600)

if not SCRAPE_TICKERS:
    raise ValueError("No tickers found in config.json. Please check the configuration.")

async def run_scrapers_in_background():
    """
    Run news_scraper and stock_scraper in parallel in the background.
    """
    loop = asyncio.get_event_loop()

    stock_factory = StockScraperFactory()
    stock_scraper = stock_factory.create_scraper()

    news_factory = NewsScraperFactory()
    news_scraper = news_factory.create_scraper(collection_name=os.getenv("COLLECTION_NAME"),
                                               scrape_num_articles=int(os.getenv("SCRAPE_NUM_ARTICLES", 1)))

    # Run both scrapers concurrently
    await asyncio.gather(
        loop.run_in_executor(None, news_scraper.scrape_all_tickers, SCRAPE_TICKERS),
        loop.run_in_executor(None, stock_scraper.scrape_all_tickers, SCRAPE_TICKERS)
    )
    # Sync scraped docs in Vector DB
    DocumentSyncManager().sync_documents()

@app.on_event("startup")
async def start_scraping_task():
    """
    Start the background task to scrape data at regular intervals when the server starts.
    """
    asyncio.create_task(scrape_in_interval(SCRAPING_INTERVAL))

async def scrape_in_interval(interval: int):
    """
    Runs the scraping task at regular intervals.
    """
    while True:
        app.state.last_scrape_start = datetime.now()
        logger.info(f"Starting scraping at {app.state.last_scrape_start}")

        # Run scrapers in parallel
        await run_scrapers_in_background()

        app.state.last_scrape_end = datetime.now()
        hours = interval / 3600  # Convert seconds to hours
        logger.info(f"Scraping completed at {app.state.last_scrape_end}. Next run in {hours:.2f} hours.")
        # Wait for the specified interval
        await asyncio.sleep(interval)


# Include routes
app.include_router(stock_routes.router, prefix="/stock", tags=["Stock Data"])
app.include_router(news_routes.router, prefix="/news", tags=["News Articles"])

@app.get("/")
def root():
 return {"message": "Welcome to the Financial Data API"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

@app.get("/dashboard", response_class=HTMLResponse)
def dashboard(request: Request):
    """Render dashboard showing DB stats and agent status."""
    from db.mongo_db import MongoDBClient
    mongo_client = MongoDBClient()
    news_col = mongo_client.get_collection()
    total_news = news_col.count_documents({})
    unsynced_news = news_col.count_documents({"synced": False})

    from db.postgres_db import PostgresDBClient
    import os
    host = os.getenv("POSTGRES_HOST")
    dbname = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER") or os.getenv("POSTGRES_USERNAME")
    pwd = os.getenv("POSTGRES_PASSWORD")
    port = os.getenv("POSTGRES_PORT", 5432)
    pg_client = PostgresDBClient(host, dbname, user, pwd, port)
    result, _ = pg_client.fetch_query("SELECT COUNT(*) FROM stock_data;")
    total_stock = result[0][0] if result else 0

    return templates.TemplateResponse("dashboard.html", {
        "request": request,
        "last_scrape_start": getattr(app.state, "last_scrape_start", None),
        "last_scrape_end": getattr(app.state, "last_scrape_end", None),
        "total_news": total_news,
        "unsynced_news": unsynced_news,
        "total_stock": total_stock,
    })


@app.get("/app", response_class=HTMLResponse)
def frontend_app(request: Request):
    """
    前端介面：提供股票統計、圖表與新聞查詢等功能。
    """
    return templates.TemplateResponse("index.html", {"request": request})