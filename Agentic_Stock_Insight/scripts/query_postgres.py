import os
from dotenv import load_dotenv
from db.postgres_db import PostgresDBClient

# 載入環境變量
# Load environment variables from .env in project root
load_dotenv()

# 連接到 PostgreSQL 數據庫
client = PostgresDBClient(
    host=os.getenv('POSTGRES_HOST'),
    database=os.getenv('POSTGRES_DB'),
    user=os.getenv('POSTGRES_USER'),
    password=os.getenv('POSTGRES_PASSWORD')
)

# 從 stock_data 表中獲取 AAPL 的數據
result, columns = client.read('stock_data', {'ticker': 'AAPL'})

# 打印列名
print(f'列名: {columns}')

# 打印前 5 筆數據
print(f'前 5 筆資料:')
for row in result[:5]:
    print(row)
