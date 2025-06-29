from dotenv import load_dotenv
from sqlalchemy import create_engine, Column, Integer, String, Date, Float, BigInteger
from sqlalchemy.ext.declarative import declarative_base
import os

load_dotenv()

# Define the base class for declarative models
Base = declarative_base()


# Define the StockData model
class StockData(Base):
    __tablename__ = "stock_data"  # Replace with a static name

    # __tablename__ = os.getenv('STOCK_TABLE')

    id = Column(Integer, primary_key=True, autoincrement=True)
    ticker = Column(String(10), nullable=False)
    date = Column(Date, nullable=False)
    open = Column(Float)
    high = Column(Float)
    low = Column(Float)
    close = Column(Float)
    volume = Column(BigInteger)
