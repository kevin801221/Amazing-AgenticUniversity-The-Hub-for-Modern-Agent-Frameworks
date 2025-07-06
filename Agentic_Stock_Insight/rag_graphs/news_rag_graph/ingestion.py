from dotenv import load_dotenv
from langchain_chroma import Chroma
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from db.mongo_db import MongoDBClient
import os
from typing import List
from utils.logger import logger

load_dotenv()

# Retrieve documents from Chroma
news_articles_retriever = Chroma(
    collection_name=os.getenv('VECTOR_DB_COLLECTION'),
    persist_directory=os.getenv("VECTOR_DB_DIRECTORY"),
    embedding_function=OpenAIEmbeddings()
).as_retriever()

class DocumentSyncManager:
    def __init__(self):
        self.mongo_client = MongoDBClient()
        self.news_collection = self.mongo_client.get_collection()
        self.vector_db_collection = os.getenv('VECTOR_DB_COLLECTION')
        self.vector_db_directory = os.getenv('VECTOR_DB_DIRECTORY')

    def fetch_unsynced_documents(self):
        """
        Fetches documents from the database where 'synced' is set to False.
        """
        return self.news_collection.find({'synced': False}, {'_id': 1, 'description': 1})

    def mark_documents_as_synced(self, document_ids: List):
        """
        Marks the provided document IDs as synced in the database.
        """
        result = self.news_collection.update_many(
            {'_id': {'$in': document_ids}},
            {'$set': {'synced': True}}
        )
        logger.info(f"Marked {result.modified_count} documents as synced.")

    def process_content(self, contents: List[str]):
        """
        Processes content into chunks using a text splitter.
        """
        text_splitter = RecursiveCharacterTextSplitter.from_tiktoken_encoder(
            chunk_size=250, chunk_overlap=0
        )
        documents = [Document(page_content=content) for content in contents]
        return text_splitter.split_documents(documents)

    def store_documents_in_chroma(self, doc_splits: List[Document]):
        """
        Stores processed document chunks as embeddings in Chroma.
        """
        vectorstore = Chroma.from_documents(
            documents=doc_splits,
            collection_name=self.vector_db_collection,
            embedding=OpenAIEmbeddings(),
            persist_directory=self.vector_db_directory
        )
        logger.info("Documents stored in Chroma.")

    def sync_documents(self):
        """
        Orchestrates the process of syncing unsynced documents:
        - Fetches unsynced documents
        - Processes their content
        - Stores them in Chroma
        - Marks them as synced in the database
        """
        unsynced_articles = list(self.fetch_unsynced_documents())
        if not unsynced_articles:
            logger.info("No unsynced documents found in MongoDB!")
            return

        descriptions = [article['description'] for article in unsynced_articles if 'description' in article]
        document_ids = [article['_id'] for article in unsynced_articles]

        if descriptions:
            doc_splits = self.process_content(descriptions)
            self.store_documents_in_chroma(doc_splits)
            self.mark_documents_as_synced(document_ids)
            logger.info("Documents processed, stored, and marked as synced.")

if __name__ == '__main__':
    DocumentSyncManager().sync_documents()