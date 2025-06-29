#!/usr/bin/env python3
"""
Environment health check script:
- Validate OpenAI API key
- Check MongoDB connection
- Check PostgreSQL connection
"""

import os
import sys
from dotenv import load_dotenv

load_dotenv()

def check_openai():
    try:
        import openai
    except ImportError:
        print("openai package is not installed")
        return False
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("OPENAI_API_KEY is not set")
        return False
    openai.api_key = api_key
    try:
        # List models using new 1.x OpenAI API
        resp = openai.models.list()
        # resp is a SyncPage; access data attribute
        models = getattr(resp, "data", [])
        print(f"OpenAI API key is valid. Models available: {len(models)}")
        return True
    except Exception as e:
        print(f"OpenAI API key validation failed: {e}")
        return False

def check_mongo():
    try:
        from pymongo import MongoClient
    except ImportError:
        print("pymongo package is not installed")
        return False
    uri = os.getenv("MONGO_URI")
    dbname = os.getenv("DATABASE_NAME")
    if not uri or not dbname:
        print("MONGO_URI or DATABASE_NAME is not set")
        return False
    try:
        client = MongoClient(uri)
        client[dbname].command("ping")
        print("MongoDB connection successful")
        return True
    except Exception as e:
        print(f"MongoDB connection failed: {e}")
        return False

def check_postgres():
    try:
        import psycopg2
    except ImportError:
        print("psycopg2 package is not installed")
        return False
    host = os.getenv("POSTGRES_HOST")
    db = os.getenv("POSTGRES_DB")
    user = os.getenv("POSTGRES_USER") or os.getenv("POSTGRES_USERNAME")
    pwd = os.getenv("POSTGRES_PASSWORD")
    port = os.getenv("POSTGRES_PORT", 5432)
    if not all([host, db, user]):
        print("PostgreSQL environment variables are not fully set")
        return False
    try:
        conn = psycopg2.connect(host=host, database=db, user=user, password=pwd, port=port)
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        cur.fetchone()
        cur.close()
        conn.close()
        print("PostgreSQL connection successful")
        return True
    except Exception as e:
        print(f"PostgreSQL connection failed: {e}")
        return False

def main():
    ok = True
    print("Starting environment health check...\n")
    for fn in (check_openai, check_mongo, check_postgres):
        if not fn():
            ok = False
    if ok:
        print("\nAll checks passed 🎉")
        sys.exit(0)
    else:
        print("\nSome checks failed. Please review the messages above.")
        sys.exit(1)

if __name__ == '__main__':
    main()