# Stock Analyzer

A modular stock analytics dashboard built with Python and Streamlit. Analyze stocks with real-time data, technical indicators, company news, and AI-powered sentiment analysis in one comprehensive interface.

> **IMPORTANT DISCLAIMER:** This project was developed with extensive use of GitHub Copilot (AI-assisted coding). GitHub Copilot was instrumental in generating code structure, implementing features, ensuring coherence, optimizing layout, and improving overall code quality throughout the entire project.

## Architecture

- Module 1: Stock data (yfinance)
- Module 2: KPI calculations
- Module 3: Charts and visualizations
- Module 4: Company news (Finnhub)
- Module 5: Sentiment analysis (FinBERT)
- Streamlit UI orchestrates all modules

## Features

- Ticker search with period and interval selection
- KPIs: SMA-20, SMA-50, volatility, basic aggregates
- Charts: price, SMAs, daily returns (matplotlib)
- News: Finnhub company news (requires API key)
- Sentiment: FinBERT BUY/HOLD/SELL classification
- Session caching to reduce repeated fetches

## Installation

Requirements: Python 3.13.x, pip

```powershell
# clone
git clone https://github.com/f-scherrer/stock-analyzer-hsg.git
cd stock-analyzer-hsg

# create and activate venv (Windows PowerShell)
python -m venv .venv
.\.venv\Scripts\Activate.ps1

# install deps
pip install -r requirements.txt
```

## Configuration

Copy the template and add your Finnhub key:

```powershell
Copy-Item .env.example .env
```

Edit `.env`:

```
FINNHUB_API_KEY=your_api_key_here
# FINNHUB_BASE_URL=https://finnhub.io  # optional override
```

## Run

```powershell
streamlit run .\src\app.py
```

App opens at http://localhost:8501.

## Test Individual Modules

```powershell
python .\src\data_module\get_stock_data.py
python .\src\kpi_module\calculate_kpis.py
python .\src\charting_module\make_charts.py
python .\src\news_module\get_news.py
python .\src\sentiment_module\get_sentiment.py
```

## Project Structure

```
stock-analyzer-hsg/
├─ .env.example
├─ pyproject.toml
├─ requirements.txt
├─ README.md
└─ src/
	├─ __init__.py
	├─ app.py
	├─ data_module/
	│  ├─ __init__.py
	│  └─ get_stock_data.py
	├─ kpi_module/
	│  ├─ __init__.py
	│  └─ calculate_kpis.py
	├─ charting_module/
	│  ├─ __init__.py
	│  └─ make_charts.py
	├─ news_module/
	│  ├─ __init__.py
	│  └─ get_news.py
	└─ sentiment_module/
		├─ __init__.py
		└─ get_sentiment.py
```

## Module Notes

- Module 1 (data_module/get_stock_data.py): Fetches OHLCV data from yfinance; adds currency.
- Module 2 (kpi_module/calculate_kpis.py): Computes daily returns, SMA-20/50, volatility; returns metrics dict and metrics DataFrame.
- Module 3 (charting_module/make_charts.py): Matplotlib figures for price, SMAs, and daily returns.
- Module 4 (news_module/get_news.py): Finnhub news; needs FINNHUB_API_KEY.
- Module 5 (sentiment_module/get_sentiment.py): FinBERT sentiment; classifies BUY/HOLD/SELL with confidence.

## Authors

- Module 1: Simon Schaller
- Module 2: Moritz Marty
- Module 3: Abel Korcsog
- Module 4: Yanick Meier
- Module 5: Patric Dahinden
- app.py: Florian Scherrer

## Troubleshooting

- ModuleNotFoundError: ensure venv is active and run from repo root.
- Finnhub 403: verify FINNHUB_API_KEY in .env and network access.
- First sentiment run is slow: FinBERT downloads (~500 MB) once, then cached.
- Charts not showing: matplotlib uses Agg backend in charting_module; keep dependencies installed.

## License

See LICENSE for terms.
