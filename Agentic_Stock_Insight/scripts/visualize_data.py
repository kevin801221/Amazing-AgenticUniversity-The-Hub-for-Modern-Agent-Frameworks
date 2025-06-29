import os
import matplotlib.pyplot as plt
import pandas as pd
from dotenv import load_dotenv
from db.postgres_db import PostgresDBClient
from db.mongo_db import MongoDBClient
import matplotlib.dates as mdates

# 載入環境變量
# Load environment variables from .env in project root
load_dotenv()

# 連接到 PostgreSQL 數據庫
postgres_client = PostgresDBClient(
    host=os.getenv('POSTGRES_HOST'),
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD')
)

# 連接到 MongoDB 數據庫
mongo_client = MongoDBClient()
news_collection = mongo_client.get_collection()

# 從 PostgreSQL 獲取股票數據
def get_stock_data(ticker, limit=30):
    result, columns = postgres_client.read('stock_data', {'ticker': ticker})
    df = pd.DataFrame(result, columns=columns)
    df = df.sort_values(by='date')  # 按日期排序
    return df.tail(limit)  # 返回最近的 limit 條記錄

# 從 MongoDB 獲取新聞數據
def get_news_data(ticker, limit=5):
    news_articles = list(news_collection.find({'ticker': ticker}).limit(limit))
    return news_articles

# 可視化股票數據
def visualize_stock_data(ticker):
    plt.figure(figsize=(12, 6))
    
    # 獲取股票數據
    df = get_stock_data(ticker)
    
    # 繪製收盤價走勢圖
    plt.subplot(2, 1, 1)
    plt.plot(df['date'], df['close'], label='收盤價', color='blue', linewidth=2)
    plt.title(f'{ticker} 股票價格走勢圖')
    plt.ylabel('價格')
    plt.grid(True)
    plt.legend()
    
    # 格式化日期軸
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    plt.xticks(rotation=45)
    
    # 繪製成交量柱狀圖
    plt.subplot(2, 1, 2)
    plt.bar(df['date'], df['volume'], label='成交量', color='green', alpha=0.7)
    plt.title(f'{ticker} 成交量')
    plt.ylabel('成交量')
    plt.grid(True)
    plt.legend()
    
    # 格式化日期軸
    plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m-%d'))
    plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator(interval=1))
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    plt.savefig(f'{ticker}_stock_chart.png')
    print(f'已保存 {ticker} 股票圖表到 {ticker}_stock_chart.png')

# 打印新聞數據
def print_news_data(ticker):
    news_articles = get_news_data(ticker)
    print(f'\n{ticker} 相關新聞:')
    for article in news_articles:
        print(f"標題: {article.get('title', 'N/A')}")
        print(f"日期: {article.get('date', 'N/A')}")
        print(f"描述: {article.get('description', 'N/A')[:100]}..." if article.get('description') else "描述: N/A")
        print('-' * 50)

# 主函數
def main():
    # 要分析的股票代碼
    tickers = ['AAPL', 'MSFT', 'GOOG', 'AMZN', 'TSLA']
    
    for ticker in tickers:
        try:
            print(f'\n分析 {ticker} 的數據...')
            visualize_stock_data(ticker)
            print_news_data(ticker)
        except Exception as e:
            print(f'分析 {ticker} 時出錯: {e}')

if __name__ == '__main__':
    main()
