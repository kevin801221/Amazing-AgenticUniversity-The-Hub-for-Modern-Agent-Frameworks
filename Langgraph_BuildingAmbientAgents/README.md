# Introduction
Welcome to LangChain Academy's Building Ambient Agents course! This course is divided into five modules that walk you through understanding LangGraph, building your **email agent**, evaluating its performance, and deploying it.

Each module includes a video lesson to walk you through key concepts, along with corresponding notebooks.

# Setup
Here's our recommended setup to get started with the course. We'll be using the set of notebooks located [here](https://github.com/langchain-ai/agents-from-scratch/tree/main). 

## Python version
Ensure you're using Python 3.11 or later. This version is required for optimal compatibility with LangGraph.
    
```bash
python3 --version
```

## Clone repo
```bash
git clone https://github.com/langchain-ai/agents-from-scratch.git
cd agents-from-scratch
```

## Running notebooks

If you don't have Jupyter set up, follow installation instructions [here](https://jupyter.org/install).

```bash
jupyter notebook
```

## Sign up for LangSmith

Sign up [here](https://smith.langchain.com). You can reference LangSmith docs [here](https://smith.langchain.com/docs).

Navigate to the Settings page, and generate an API key in LangSmith.

Create a .env file that mimics the provided .env.example. Set

## Set up OpenAI API key

If you don’t have an OpenAI API key, you can sign up here.

Then, set `OPENAI_API_KEY` in the .env file.

## Set environment variables

Create a .env file in the root directory:

```bash
# Copy the .env.example file to .env
cp .env.example .env
```

Edit the .env file with the following:

```
LANGSMITH_API_KEY=your_langsmith_api_key
LANGSMITH_TRACING=true
LANGSMITH_PROJECT="interrupt-workshop"
OPENAI_API_KEY=your_openai_api_key
```

You can also set the environment variables in your terminal:

```bash
export LANGSMITH_API_KEY=your_langsmith_api_key
export LANGSMITH_TRACING=true
export OPENAI_API_KEY=your_openai_api_key
```

## Package Installation

### Recommended: Using uv (faster and more reliable)

```bash
# Install uv if you haven't already
pip install uv

# Install the package with development dependencies
uv sync --extra dev

# Activate the virtual environment
source .venv/bin/activate
```

### Alternative: Using pip

```bash
python3 -m venv .venv
source .venv/bin/activate

# Ensure you have a recent version of pip (required for editable installs with pyproject.toml)
python3 -m pip install --upgrade pip

# Install the package in editable mode
pip install -e .
```

⚠️ **IMPORTANT**: Do not skip the package installation step! This editable install is required for the notebooks to work correctly. The package is installed as interrupt_workshop with import name email_assistant, allowing you to import from anywhere with `from email_assistant import ...`