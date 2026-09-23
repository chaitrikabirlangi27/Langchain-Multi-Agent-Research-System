# LangChain Multi-Agent Research System

A Streamlit-based multi-agent research application that searches the web, reads relevant online content, generates a structured research report, and critiques the final report.

## Overview

The system follows this research pipeline:

```text
User Topic
    ↓
Search Agent
    ↓
Tavily Web Search
    ↓
Reader Agent
    ↓
URL Scraping & Content Extraction
    ↓
Writer Chain
    ↓
Research Report
    ↓
Critic Chain
    ↓
Review & Score
```

The project demonstrates how multiple AI components can be combined into a practical research workflow using LangChain, Groq, Tavily, web scraping, and Streamlit.

## Features

- Web research using Tavily
- Search Agent for finding recent and relevant information
- Reader Agent for selecting and scraping a relevant URL
- Multiple web-content extraction strategies
- Structured research report generation
- Critic Chain for reviewing and scoring the generated report
- Streamlit web interface
- Download generated research reports as Markdown files
- Environment-variable based API key configuration

## System Architecture

### 1. Search Agent

The Search Agent receives the user's research topic and uses the `web_search` tool.

The Tavily search tool returns:

- Title
- URL
- Search snippet

The search is configured to return up to three results using Tavily's basic search depth.

### 2. Reader Agent

The Reader Agent receives the search results and selects a relevant URL.

It uses the `scrape_url` tool to retrieve and extract readable content from the selected webpage.

The scraper uses multiple extraction strategies:

1. Trafilatura
2. Readability
3. BeautifulSoup fallback extraction

### 3. Writer Chain

The Writer Chain combines the search results and scraped content and generates a professional research report containing:

- Introduction
- Key Findings
- Conclusion
- Sources

The Writer is implemented as a LangChain chain rather than an agent.

### 4. Critic Chain

The Critic Chain reviews the generated research report.

It returns:

- Score
- Strengths
- Areas to Improve
- One-line verdict

The Critic is implemented as a LangChain chain rather than an agent.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Application development |
| LangChain | Agent and chain orchestration |
| LangGraph | Agent execution infrastructure used by LangChain agents |
| Groq | Large language model provider |
| Tavily | Web search |
| Streamlit | Web application interface |
| Requests | HTTP requests for webpage retrieval |
| Trafilatura | Main webpage content extraction |
| Readability | Alternative webpage content extraction |
| BeautifulSoup | HTML parsing and fallback extraction |
| python-dotenv | Environment variable loading |
| Rich | Logging/debugging support |

## Models

The project uses different Groq model configurations for different tasks.

### Search and Reader Agents

```python
ChatGroq(
    model="openai/gpt-oss-20b",
    temperature=0,
    reasoning_effort="low",
    max_tokens=500
)
```

### Writer Chain

```python
ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    reasoning_effort="low",
    max_tokens=1500
)
```

### Critic Chain

```python
ChatGroq(
    model="openai/gpt-oss-120b",
    temperature=0,
    reasoning_effort="low",
    max_tokens=700
)
```

## Project Structure

```text
Langchain-Multi-Agent-Research-System/
│
├── src/
│   ├── agents/
│   │   ├── __init__.py
│   │   └── agents.py
│   │
│   ├── pipelines/
│   │   ├── __init__.py
│   │   └── pipeline.py
│   │
│   └── tools/
│       ├── __init__.py
│       └── tools.py
│
├── app.py
├── requirements.txt
├── README.md
├── LICENSE
├── demo.excalidraw
├── .gitignore
└── .env
```

> `.env` should remain local and should not be committed to GitHub.

## How the Application Works

### Step 1 — Enter a Research Topic

The user enters a topic in the Streamlit interface.

Example:

```text
Latest AI tools for developers
```

### Step 2 — Search Agent

The Search Agent uses Tavily to search for recent and reliable information.

The application keeps the actual search-tool results so that URLs can be passed to the Reader Agent.

### Step 3 — Reader Agent

The Reader Agent receives the search results and chooses a relevant URL.

The selected webpage is passed to the scraping tool.

### Step 4 — Content Extraction

The scraper requests the webpage and attempts to extract clean readable content.

Extraction order:

```text
Webpage
   ↓
Trafilatura
   ↓
Readability
   ↓
BeautifulSoup fallback
```

Extracted content is limited before being passed to later stages to keep model requests manageable.

### Step 5 — Writer Chain

The Writer Chain receives:

```text
Search Results
+
Detailed Scraped Content
```

It then creates the final research report.

### Step 6 — Critic Chain

The generated report is passed to the Critic Chain.

The critic evaluates the report and provides structured feedback.

## Installation

### 1. Clone the repository

```bash
git clone https://github.com/chaitrikabirlangi27/Langchain-Multi-Agent-Research-System.git
```

### 2. Open the project

```bash
cd Langchain-Multi-Agent-Research-System
```

### 3. Create and activate the environment

Example using Conda:

```bash
conda create -n langagent python=3.11 -y
conda activate langagent
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```



## Run the Application

Start the Streamlit application with:

```bash
streamlit run app.py
```

Streamlit will provide a local URL, normally similar to:

```text
http://localhost:8501
```

## Example Query

```text
Latest AI tools for developers
```

Other suitable research topics include:

```text
How Generative AI is Transforming Software Development in 2026
```

```text
How AI is used in cybersecurity
```

## Output

After running the pipeline, the application displays:

```text
01  Search Agent    ✓ DONE
02  Reader Agent    ✓ DONE
03  Writer Chain    ✓ DONE
04  Critic Chain    ✓ DONE
```

### Research Results

The application provides expandable sections for:

- Search Results
- Scraped Content

### Final Research Report

The generated report contains:

- Introduction
- Key Findings
- Conclusion
- Sources

The report can also be downloaded as a Markdown file using the application's download button.

### Critic Feedback

The Critic Chain provides:

```text
Score: X/10

Strengths:
- ...

Areas to Improve:
- ...

One line verdict:
...
```

## API Keys and Security

API keys are loaded from environment variables.

Never place API keys directly in Python source files or commit them to GitHub.

The `.gitignore` file should include:

```text
.env
__pycache__/
*.pyc
```

## Future Improvements

Possible future improvements include:

- Better URL selection between multiple search results
- More robust handling of websites that block automated requests
- Parallel research agents
- Additional research tools
- Persistent agent memory
- More advanced report evaluation
- Deployment to a cloud platform
- More detailed source validation

## License

This project includes a `LICENSE` file. See the repository's license file for the applicable license terms.

## Project Workflow

```text
                    USER TOPIC
                        │
                        ▼
                ┌───────────────┐
                │  Search Agent │
                └───────┬───────┘
                        │
                        ▼
                 Tavily Web Search
                        │
                        ▼
                 Search Results
                 (Titles + URLs)
                        │
                        ▼
                ┌───────────────┐
                │  Reader Agent │
                └───────┬───────┘
                        │
                        ▼
                  scrape_url()
                        │
                        ▼
                Scraped Content
                        │
                        ▼
                ┌───────────────┐
                │  Writer Chain │
                └───────┬───────┘
                        │
                        ▼
                Research Report
                        │
                        ▼
                ┌───────────────┐
                │  Critic Chain │
                └───────┬───────┘
                        │
                        ▼
                 Critic Feedback
```

## Project Status

This project demonstrates a multi-stage AI research workflow using two tool-using agents followed by two LangChain chains:

- Search Agent — Web research
- Reader Agent — Web content extraction
- Writer Chain — Report generation
- Critic Chain — Report evaluation
