
# AI Research Assistant

An intelligent multi-agent research platform that
automates web research, information analysis and
structured research report generation.

## Overview

The AI Research Assistant uses three specialized
agents working together to simplify the research
process.

Users enter a research topic and receive an
AI-generated research summary and structured report
with source references.

## Features

- Automated web research
- AI-powered summarization
- Multi-agent architecture
- Structured research report generation
- Source references and clickable links
- Interactive Gradio interface
- PDF report generation and download
- Example research topics

## System Architecture

### Agent 1: Web Research Agent
Uses DuckDuckGo to collect relevant web search results.

### Agent 2: Summarization Agent
Uses Groq-powered LLM inference to analyze research
findings and identify important information.

### Agent 3: Report Generation Agent
Converts summarized findings into a structured
research report.

## Workflow

User Input
    |
Web Research Agent
    |
Summarization Agent
    |
Report Generation Agent
    |
Research Report + PDF

## Tech Stack

- Python
- Groq API
- GPT-OSS 20B
- DuckDuckGo Search
- Gradio
- ReportLab

## Project Structure

AI_Research_Assistant/
|
|-- app.py
|-- research_agent.py
|-- summarizer_agent.py
|-- report_agent.py
|-- requirements.txt
|-- .env
|-- .gitignore
|-- README.md

## Installation

Clone the repository:

git clone YOUR_REPOSITORY_URL

Navigate into the project:

cd AI_Research_Assistant

Create a virtual environment:

python -m venv venv

Activate it on Windows:

venv\Scripts\activate

Install dependencies:

pip install -r requirements.txt

Create a .env file:

GROQ_API_KEY=your_api_key

Run the application:

python app.py

## Future Enhancements

- Research history and database integration
- Full webpage content extraction
- Fact verification agent
- Multiple LLM providers
- PDF customization
- Export reports to DOCX

## Security

API keys are stored in environment variables.
Never upload your .env file to GitHub.

## Author

Vidya
