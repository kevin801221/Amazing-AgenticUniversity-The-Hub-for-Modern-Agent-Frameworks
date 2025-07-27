   <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/"><img alt="Creative Commons License" style="border-width:0" src="https://i.creativecommons.org/l/by-nc-sa/4.0/88x31.png" /></a><br />This work is licensed under a <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/4.0/">Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International License</a>.
   

# Stock Data Insights Application

This project demonstrates the use of Agentic Retrieval-Augmented Generation (RAG) workflows to extract insights from news and financial data pertaining to specific companies and the broader stock market. It leverages Large Language Models (LLMs), ChromaDB as a vector database, LangChain, LangChain Expression Language (LCEL), and LangGraph to provide comprehensive analyses.

## Features

- **Stock Performance Visualization**: Displays graphs and charts illustrating the historical performance of selected stocks.
- **Attribute-Specific Data Retrieval**: Fetches detailed information related to specific attributes of a particular stock.
- **News Aggregation**: Presents general news or topic-specific articles related to a particular stock or company.

## High Level Architecture
![High Level Design](documentation/high_level_design.png)

## Approach

### Asynchronous Scraping

1. **News Data**: Asynchronously scrapes news data for a predefined set of stocks at regular intervals, storing the information in MongoDB. The documents are synchronized with ChromaDB to enable LLMs to perform semantic searches, facilitating the retrieval of relevant information specific to a particular stock or company.
2. **Financial Data**: Asynchronously scrapes financial data for selected stocks at regular intervals, storing the information in PostgreSQL.

### LangGraph Workflows

#### News Data RAG Graph
An Agentic RAG Graph designed to search news data for a stock either in the vector database (synced documents from MongoDB) or perform a web search if relevant documents are not found.

![News RAG Graph](images/news-rag-graph.png)

This graph comprises the following nodes:

- **Retrieve News from DB (`retrieve_news`)**: Utilizes LLMs, LangChain, and a Retriever Tool to perform semantic searches in the vector database for documents related to a specific stock topic.
- **Grade Documents (`grade_documents`)**: Evaluates the quality of documents retrieved in the previous step, assigning a score to determine their relevance. A conditional edge decides whether to generate results or perform an additional web search if the documents are not pertinent.
- **Web Search (`web_search`)**: Conducts a web search using TavilySearch tooling integrated with LangChain and LLM calls.
- **Generate Results (`generate_results`)**: Produces results based on the user query and the documents retrieved in prior steps.

#### Stock Data RAG Graph

![News RAG Graph](images/stock-data-rag-graph.png)

An Agentic RAG Graph that searches financial data for a stock in the SQL database (PostgreSQL).

This graph includes the following nodes:

- **Generate SQL (`generate_sql`)**: Employs LLMs and LangChain to generate an SQL query based on user input.
- **Execute SQL (`execute_sql`)**: Executes the SQL query generated in the previous step to fetch data from the database.
- **Generate Results (`generate_results`)**: Utilizes LLMs to generate results according to the user query and the data retrieved in the preceding step.

#### Stock Data Charts RAG Graph

![News RAG Graph](images/stock-charts-rag-graph.png)

An Agentic RAG Graph that retrieves financial data for a stock from the SQL database (PostgreSQL) and generates visual charts.

This graph consists of the following nodes:

- **Generate SQL (`generate_sql`)**: Uses LLMs and LangChain to create an SQL query based on user input.
- **Execute SQL (`execute_sql`)**: Runs the SQL query generated earlier to fetch data from the database.

## APIs
For detailed API specifications, refer to the attached `openapi.json` file.


### Price Stats (GET `/stock/{ticker}/price-stats`)

Get stock price statistics for a specific ticker.

Args:
    ticker (str): Stock ticker symbol.
    operation (str): Operation to perform (e.g., 'highest', 'lowest', 'average').
    price_type (str): Type of price (e.g., 'open', 'close', 'low', 'high').
    duration (int): Number of days

Returns:
    dict: Stock data with the requested statistics.

#### Parameters:
- `ticker`: string - Stock ticker symbol
- `operation`: string - Operation to perform: 'highest', 'lowest', 'average'
- `price_type`: string - Price type: 'open', 'close', 'low', 'high'
- `duration`: string - Duration (days): '1', '7', '14', '30'

### Chart (GET `/stock/{ticker}/chart`)

Get stock price statistics and return a histogram/chart for a specific ticker.

Args:
    ticker (str): Stock ticker symbol.
    price_type (str): Type of price (e.g., 'open', 'close', 'low', 'high').
    duration (int): Number of days

Returns:
    dict: Stock data with the requested statistics.

#### Parameters:
- `ticker`: string - Stock ticker symbol
- `price_type`: string - Price type: 'open', 'close', 'low', 'high'
- `duration`: string - Duration (days): '1', '7', '14', '30'

### News By Topic (GET `/news/{ticker}`)

Get news a specific ticker.

Args:
    ticker (str): Stock ticker symbol.
    topic (str): Topic to fetch news for a specific stock.

Returns:
    dict: Relevant news for a speicific ticker.

#### Parameters:
- `ticker`: string - Stock ticker symbol
- `topic`: string - Topic

### Root (GET `/`)

Root/home page of the application

#### Parameters:
No parameters


## Class Diagrams

![Class Diagram](images/classes_stock_proj.png)
## Images

For visual representations, refer to the images in the `images/` directory.

## Testing Framework
The project employs the pytest framework for automated testing. This ensures that all modules are thoroughly tested to maintain reliability and robustness. Key features of the testing setup include:

Comprehensive Test Cases: Test cases are written for every module, ensuring complete coverage of the application.
Ease of Use: Simply run the following command to execute all tests:
```bash
pytest
```
Test Reports: The framework generates detailed reports for each test run, highlighting successes and failures.
This testing setup ensures that the application remains stable and functional as new features are added or existing features are updated.

## Observability and Tracing
To monitor the application's performance and debug LLM-related processes, the project integrates LangSmith tracing. This enables detailed tracing of all LLM calls, providing insights into the application's execution flow.

Key Features:
LLM Call Tracing: Tracks all interactions with Large Language Models, including inputs, outputs, and execution times.
Debugging Assistance: Helps in identifying bottlenecks or errors in LLM workflows.
LangSmith Dashboard: Offers a user-friendly interface to visualize and analyze traces.
How It Works:
LangSmith tracing is seamlessly integrated into the application. All RAG workflows, including News RAG Graph, Stock Data RAG Graph, and Stock Data Charts RAG Graph, utilize LangSmith to provide actionable observability insights.


## References

- **LangGraph**: A library for building stateful, multi-actor applications with LLMs, facilitating the creation of agent and multi-agent workflows.
- **LangChain Expression Language (LCEL)**: A declarative approach to composing chains, enabling seamless integration and optimization of complex workflows.

This project exemplifies the integration of advanced AI workflows to provide insightful analyses of financial and news data, offering users a comprehensive tool for stock market evaluation.
