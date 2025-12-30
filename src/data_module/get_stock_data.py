##################################################
# Module A - Stock Data Fetcher (yfinance)
# Author: Simon Schaller
# Python version: 3.13.x (project standard)
#
# Note: GitHub Copilot was used for coding efficiency,
# structure, coherence, and layout.
#
# Description:
# Fetches historical stock data from Yahoo Finance for a ticker
# and specified period/interval.
# Returns a pandas DataFrame with OHLCV data.
#
# Requirements:
# - pip install yfinance pandas
##################################################

import yfinance as yf
import pandas as pd


def stock_data(ticker, period, interval):
    # fetching the data from yahoo finance
    df = yf.download(
        tickers=ticker,
        period=period,
        interval=interval,
        auto_adjust=False,
        progress=False,
    )
    # handling error cases, e.g. when nothing is returned
    if df.empty:
        raise ValueError(
            f"No data available for ticker '{ticker}' with period='{period}' and interval='{interval}'."
        )

    # Converting dataframe to DatetimeIndex
    df.index = pd.to_datetime(df.index)

    # Dropping rows with missing values
    df = df.dropna(how="any")

    # if values for "Adj Close" are missing, take values from column "Close"
    if "Adj Close" not in df.columns and "Close" in df.columns:
        df["Adj Close"] = df["Close"]

    # filtering for the relevant columns
    expected_cols = ["Open", "High", "Low", "Close", "Adj Close", "Volume"]
    available_cols = [c for c in expected_cols if c in df.columns]
    df = df[available_cols]

    # Indexing the column according to the column "Date"
    df = df.reset_index().rename(columns={"index": "Date"})

    # Standardizing column order
    cols_order = ["Date"] + [c for c in expected_cols if c in df.columns]
    df = df[cols_order]

    # Fetching the corresponding currency from metadata
    ticker_obj = yf.Ticker(ticker)
    currency = ticker_obj.info.get("currency", "UNKNOWN")

    # Add column "Currency"
    df["Currency"] = currency

    # Flattening the MultiIndex so "Price" and Ticker won't be shown in the Dataframe
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
        df.columns.name = None

    # final order of the Dataframe
    cols_order = [
        "Date",
        "Open",
        "High",
        "Low",
        "Close",
        "Adj Close",
        "Volume",
        "Currency",
    ]
    df = df[[c for c in cols_order if c in df.columns]]

    return df


##################################################
# Simple test block
##################################################

if __name__ == "__main__":

    print("Running simple test for Module A with yfinance (new path)")

    test_ticker = "AAPL"
    test_period = "5d"
    test_interval = "1d"

    try:
        result = stock_data(test_ticker, test_period, test_interval)
        print(f"\nSuccessfully fetched {test_ticker} data")
        print(f"Shape: {result.shape}")
        print(f"Columns: {list(result.columns)}")
        print(f"\nFirst few rows:")
        print(result.head())
        print("\nModule A test run completed successfully.")
    except Exception as e:
        print(f"Error during test: {e}")
