import os
from dotenv import load_dotenv
from db.mongo_db import MongoDBClient

# 載入環境變量
# Load environment variables from .env in project root
load_dotenv()

# 連接到 MongoDB 數據庫
mongo_client = MongoDBClient()
news_collection = mongo_client.get_collection()

# 從 news_articles 集合中獲取 AAPL 的新聞
news_articles = list(news_collection.find({'ticker': 'AAPL'}).limit(5))

# 打印新聞數量
print(f'總新聞數量: {news_collection.count_documents({})}')
print(f'蘋果公司新聞數量: {news_collection.count_documents({"ticker": "AAPL"})}')

# 打印前 5 篇新聞
print(f'\n前 5 篇蘋果公司新聞:')
for article in news_articles:
    print(f"標題: {article.get('title', 'N/A')}")
    print(f"日期: {article.get('date', 'N/A')}")
    print(f"描述: {article.get('description', 'N/A')[:100]}...")
    print('-' * 50)
