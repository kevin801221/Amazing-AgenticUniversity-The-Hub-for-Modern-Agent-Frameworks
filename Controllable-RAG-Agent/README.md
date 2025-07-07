# Sophisticated Controllable Agent for Complex RAG Tasks 🧠📚

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://opensource.org/licenses/Apache-2.0)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg?style=flat-square)](http://makeapullrequest.com)

An advanced Retrieval-Augmented Generation (RAG) solution designed to tackle complex questions that simple semantic similarity-based retrieval cannot solve. This project showcases a sophisticated deterministic graph acting as the "brain" of a highly controllable autonomous agent capable of answering non-trivial questions from your own data, such as ESG reports.

![Demo](graphs/demo.gif)

## 🌟 Key Features

- **Sophisticated Deterministic Graph**: Acts as the "brain" of the agent, enabling complex, multi-step reasoning.
- **Controllable Autonomous Agent**: Capable of answering non-trivial questions from custom datasets like ESG reports.
- **Hallucination Prevention**: Ensures answers are solely based on provided data, avoiding AI hallucinations.
- **Multi-step Reasoning**: Breaks down complex queries into manageable sub-tasks for deeper analysis.
- **Adaptive Planning**: Continuously updates its plan based on newly retrieved information.
- **Versatile Data Handling**: Processes and reasons over multiple data representations (raw chunks, summaries, direct quotes) simultaneously.

## 🧠 How It Works
![Solution Schema](graphs/final_graph_schema.jpeg)

1.  **PDF Loading and Processing**: Loads all PDF documents from a specified folder (`ESG_pdf/`).
2.  **Multi-Faceted Text Processing**: The agent processes the documents in three distinct ways to create a rich, multi-layered understanding:
    -   **Chunks**: The raw text is split into smaller, indexed chunks for detailed lookups.
    -   **Summaries**: The content is grouped (e.g., every few pages) and summarized by an LLM to provide high-level context.
    -   **Quotes**: Direct quotes or key statements are extracted and stored separately for retrieving precise information.
3.  **Vector Store Creation**: Encodes these three representations of the data into three separate FAISS vector stores.
4.  **Question Processing & Planning**:
    -   Anonymizes the user's question to create a generic, high-level plan.
    -   De-anonymizes the plan and breaks it down into concrete, executable tasks.
5.  **Task Execution & Reasoning**:
    -   For each task, the agent's "brain" decides which of the three vector stores (Chunks, Summaries, or Quotes) is most suitable for retrieving the necessary information.
    -   It can also decide to answer a sub-question based on the context it has already gathered.
6.  **Verification and Re-planning**: Verifies that generated content is grounded in the source documents and re-plans if more information is needed.
7.  **Final Answer Generation**: Produces the final, synthesized answer using the accumulated context.

## 🔍 Use Case: ESG Report Analysis

This framework is ideal for deep analysis of complex documents like Environmental, Social, and Governance (ESG) reports. Answering questions about ESG performance often requires synthesizing information from different sections of one or more reports.

### Example Question
**Q: What were the company's total Scope 1 and Scope 2 GHG emissions for the last two reported years, and what were the primary drivers for any significant changes?**

To solve this, the agent must:

1.  Identify the terms "Scope 1," "Scope 2," and "GHG emissions."
2.  Search the documents (likely using the **Chunks** store) for specific emission figures for the last two years.
3.  Search for narratives or explanations regarding changes in emissions (likely using the **Summaries** or **Chunks** stores).
4.  Synthesize the retrieved numbers and explanations into a coherent final answer.

The agent's ability to break down and solve such complex queries demonstrates its sophisticated reasoning capabilities.

## 🚀 Getting Started

### Prerequisites

-   Python 3.8+
-   Docker (for running the Streamlit app, optional but recommended)
-   An OpenAI API key

### Installation and Setup

1.  **Clone the repository**:
    ```sh
    git clone https://github.com/NirDiamant/Controllable-RAG-Agent.git
    cd Controllable-RAG-Agent
    ```
2.  **Set up environment variables**:
    Create a `.env` file by copying the `.env.example` file. Then, add your OpenAI API key:
    ```
    OPENAI_API_KEY=sk-...
    ```
3.  **Install dependencies**:
    ```sh
    pip install -r requirements.txt
    ```
4.  **Add your data**:
    Place all your ESG reports (or any other PDFs you want to analyze) into the `ESG_pdf/` directory.

5.  **Vectorize your documents**:
    Run the provided script to process your PDFs and create the necessary FAISS vector stores. This step needs to be done only once for a given set of documents.
    ```sh
    python vectorize_esg_faiss.py
    ```

### Usage

1.  **Run the Streamlit application**:
    ```sh
    streamlit run simulate_agent.py
    ```
2.  **Interact with the agent**:
    Open your browser to the local Streamlit URL (`http://localhost:8501`). You can now ask complex questions about your documents through the web interface.

## 🛠️ Technologies Used

-   LangChain / LangGraph
-   FAISS Vector Store
-   Streamlit (for visualization)
-   OpenAI (for embeddings and generation)