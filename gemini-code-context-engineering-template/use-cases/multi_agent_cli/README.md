# Multi-Agent CLI

This project demonstrates a multi-agent system where a primary "Research Agent" uses a secondary "Email Agent" as a tool.

## Project Structure

```
multi_agent_cli/
├── .env.example
├── README.md
├── cli.py
├── email_agent.py
├── email_tools.py
├── research_agent.py
├── research_tools.py
└── requirements.txt
```

## Setup

1.  **Create and activate virtual environment using `uv`**:
    ```bash
    uv venv
    source .venv/bin/activate
    ```

2.  **Install dependencies**:
    ```bash
    uv pip install -r requirements.txt
    ```

3.  **Configure Environment Variables**:
    -   Create a `.env` file from the example: `cp .env.example .env`
    -   **Brave Search API**:
        -   Go to [https://brave.com/search/api/](https://brave.com/search/api/) to get your free API key.
        -   Add it to your `.env` file: `BRAVE_API_KEY=YOUR_KEY`

4.  **Configure Gmail API**:
    -   This is the most complex part. You need to enable the Gmail API and get OAuth 2.0 credentials.
    -   Go to the [Google Cloud Console](https://console.cloud.google.com/).
    -   Create a new project.
    -   Go to "APIs & Services" > "Enabled APIs & services", click "+ ENABLE APIS AND SERVICES", search for "Gmail API" and enable it.
    -   Go to "APIs & Services" > "OAuth consent screen". Choose "External" and create an app. You can use dummy information for the app name, support email, etc. You don't need to submit it for verification for this personal use case. Add your Google account as a test user.
    -   Go to "APIs & Services" > "Credentials". Click "+ CREATE CREDENTIALS" > "OAuth client ID".
    -   Choose "Desktop app" as the application type.
    -   After creation, a modal will appear. Click "DOWNLOAD JSON".
    -   **Rename the downloaded file to `credentials.json` and place it in the root of the `multi_agent_cli` directory.**

5.  **First Run & Authentication**:
    -   The first time you run the application, it will open a web browser and ask you to log in with your Google account and grant permission.
    -   After you approve, it will create a `token.json` file in the same directory. This file will be used for all subsequent API calls, so you won't have to log in every time.

## Usage

```bash
python multi_agent_cli/cli.py "Your research query here"
```

**Example:**
```bash
python multi_agent_cli/cli.py "What are the main new features in Pydantic V2? Summarize them and draft an email to the team at team@example.com"
```
