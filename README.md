# InsightAI — Mini AI Business Intelligence Assistant

## Overview

InsightAI is an AI-powered Business Intelligence Assistant that allows users to ask questions about sales data in natural language and receive meaningful business insights.

The project combines natural-language interpretation with predefined Python analytics functions and SQL queries to calculate business metrics from a SQLite database.

## Features

- Natural-language business queries
- Total revenue calculation
- Highest-revenue product identification
- Highest-revenue region identification
- Monthly revenue trend analysis
- Revenue comparison between two months
- Local question classification with Gemini fallback
- Interactive Streamlit dashboard
- FastAPI backend for analytics requests

## Technology Stack

- **Language:** Python
- **Frontend:** Streamlit
- **Backend:** FastAPI
- **Database:** SQLite
- **Query Language:** SQL
- **AI Integration:** Google Gemini API

## How It Works

1. The user enters a business question in the Streamlit dashboard.
2. FastAPI receives the question.
3. The interpreter attempts local classification and uses Gemini when needed.
4. The backend selects the appropriate predefined analytics function.
5. SQL queries calculate the requested business metrics.
6. The results are returned to the dashboard.

## Example Questions

- What is the total revenue?
- Which product generated the highest revenue?
- Which region generated the highest revenue?
- Show me the monthly revenue trend.
- Compare revenue between April 2026 and May 2026.

## Project Structure

```text
mini_assistant/
├── app/
│   ├── analytics.py
│   ├── database.py
│   ├── interpreter.py
│   ├── main.py
│   └── streamlit_app.py
├── data/
│   └── sales_data.csv
├── tests/
├── .env.example
├── .gitignore
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd mini_assistant
```

### 2. Create a virtual environment

On Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
pip install -r requirements.txt
```

### 4. Configure the Gemini API key

Create a `.env` file in the project root:

```text
GEMINI_API_KEY=your_gemini_api_key
```

Use your own API key. Never commit the real `.env` file to GitHub.

### 5. Start the backend

```powershell
uvicorn app.main:app --reload
```

API documentation: http://127.0.0.1:8000/docs

### 6. Start the Streamlit dashboard

Open a second terminal in the project root:

```powershell
python -m streamlit run app/streamlit_app.py
```

## Security

API credentials are stored in environment variables. The `.env` file, virtual environment, and local database should remain excluded from version control.

## Future Enhancements

- Interactive charts and visual analytics
- Additional business performance metrics
- Broader natural-language query support
- Automated testing and deployment
