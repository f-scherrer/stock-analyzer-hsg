##################################################
# Module C - Charting Module
# Author: Abel Korcsog
# Python version: 3.13.x (project standard)
#
# Note: GitHub Copilot was used for coding efficiency,
# structure, coherence, and layout.
#
# Description:
# Receives time-series KPI data from Module B (metrics_df)
# and creates charts using matplotlib.
# Does not fetch or modify data.
#
# Functions:
# - plot_price(metrics_df): closing price over time
# - plot_sma(metrics_df): price and moving averages
# - plot_daily_returns(metrics_df): daily returns
#
# Each function returns a matplotlib Figure object
# that can be displayed by Streamlit.
#
# Requirements:
# - pip install matplotlib pandas
##################################################

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt


##################################################
# Price chart: closing price over time
##################################################

def plot_price(metrics_df):
    # metrics_df must contain:
    # - "Date" column
    # - "Close" column

    fig, ax = plt.subplots()

    # Closing price line
    ax.plot(metrics_df["Date"], metrics_df["Close"], label="Close Price")

    ax.set_xlabel("Date")
    ax.set_ylabel("Closing Price")
    ax.set_title("Stock Closing Price Over Time")
    ax.legend()

    fig.autofmt_xdate()
    return fig


##################################################
# SMA chart: price with 20- and 50-day averages
##################################################

def plot_sma(metrics_df):
    # metrics_df must contain:
    # - "Date"
    # - "Close"
    # - "SMA_20"
    # - "SMA_50"

    fig, ax = plt.subplots()

    ax.plot(metrics_df["Date"], metrics_df["Close"], label="Close Price")
    ax.plot(metrics_df["Date"], metrics_df["SMA_20"], label="SMA 20")
    ax.plot(metrics_df["Date"], metrics_df["SMA_50"], label="SMA 50")

    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.set_title("Price with 20-day and 50-day SMAs")
    ax.legend()

    fig.autofmt_xdate()
    return fig


##################################################
# Daily returns chart
##################################################

def plot_daily_returns(metrics_df):
    # metrics_df must contain:
    # - "Date"
    # - "Daily_Returns"

    fig, ax = plt.subplots()

    ax.plot(metrics_df["Date"], metrics_df["Daily_Returns"], label="Daily Returns")

    ax.set_xlabel("Date")
    ax.set_ylabel("Daily Return")
    ax.set_title("Daily Returns Over Time")
    ax.legend()

    fig.autofmt_xdate()
    return fig


##################################################
# Simple test block (manual check only)
##################################################
if __name__ == "__main__":
    import pandas as pd

    test_df = pd.DataFrame({
        "Date": pd.date_range(start="2024-01-01", periods=5, freq="D"),
        "Close": [100, 101, 102, 103, 104],
        "SMA_20": [100, 100.5, 101, 101.5, 102],
        "SMA_50": [99.5, 99.7, 99.9, 100.1, 100.3],
        "Daily_Returns": [0.0, 0.01, 0.02, 0.03, 0.04],
    })

    print("Running simple local tests for Module C charts (new path)...")

    fig_price = plot_price(test_df)
    fig_sma = plot_sma(test_df)
    fig_returns = plot_daily_returns(test_df)

    fig_price.savefig("chart_price.png")
    fig_sma.savefig("chart_sma.png")
    fig_returns.savefig("chart_daily_returns.png")

    print("Saved charts: chart_price.png, chart_sma.png, chart_daily_returns.png")
    print("Module C test run completed.")
