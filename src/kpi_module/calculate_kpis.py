##################################################
# Module B - KPI Engine
# Author: Moritz Marty
# Python version: 3.13.x (project standard)
#
# Description:
# Calculates Key Performance Indicators (KPIs) from stock data.
# Takes a DataFrame from Module A and returns metrics dictionary
# and a new DataFrame with technical indicators.
#
# Functions:
# - compute_kpis(df): calculates daily returns, SMAs, and volatility
#
# Returns:
# tuple: (metrics_dict, metrics_df)
#
# Requirements:
# - pip install pandas
##################################################

import pandas as pd


def compute_kpis(df):
    # calculates KPIs from stock data
    # metrics_dict contains: avg_close, max_close, min_close, volatility
    # metrics_df contains: Close, Daily_Returns, SMA_20, SMA_50

    # 1. Create a copy to avoid changing the original data

    metrics_df = df.copy()

    # 2. Compute Daily Returns

    metrics_df['Daily_Returns'] = metrics_df['Close'].pct_change()

    # 3. Compute Simple Moving Averages (SMA) with adaptive windows
    # Use smaller windows if dataset is too small (e.g., 5-day period)
    
    data_length = len(metrics_df)
    
    # Adaptive SMA windows: use up to 20/50, but not more than available data
    sma_20_window = min(20, max(2, data_length // 2))
    sma_50_window = min(50, max(3, data_length - 1))
    
    metrics_df['SMA_20'] = metrics_df['Close'].rolling(window=sma_20_window).mean()
    metrics_df['SMA_50'] = metrics_df['Close'].rolling(window=sma_50_window).mean()

    # 4. Compute Scalar Metrics (Single numbers for the Cards)

    avg_close = df['Close'].mean()
    max_close = df['Close'].max()
    min_close = df['Close'].min()

    volatility = metrics_df['Daily_Returns'].std()

    metrics_dict = {
        "avg_close": round(avg_close, 2),
        "max_close": round(max_close, 2),
        "min_close": round(min_close, 2),
        "volatility": round(volatility, 4)
    }

    # 5. Clean up the DataFrame for Module C

    final_df = metrics_df[['Close', 'Daily_Returns', 'SMA_20', 'SMA_50']].copy()

    return metrics_dict, final_df


##################################################
# Simple test block
##################################################

if __name__ == "__main__":
    print("Running simple test for Module B KPI calculations (new path)")

    # Create sample data (as if it came from Module A)
    test_data = pd.DataFrame({
        "Date": pd.date_range(start="2024-01-01", periods=100, freq="D"),
        "Open": [100 + i * 0.5 for i in range(100)],
        "High": [102 + i * 0.5 for i in range(100)],
        "Low": [99 + i * 0.5 for i in range(100)],
        "Close": [101 + i * 0.5 for i in range(100)],
        "Adj Close": [101 + i * 0.5 for i in range(100)],
        "Volume": [1000000 + i * 10000 for i in range(100)],
        "Currency": ["USD"] * 100
    })

    try:
        metrics_dict, metrics_df = compute_kpis(test_data)

        print(f"\nKPI Metrics calculated:")
        for key, value in metrics_dict.items():
            print(f"  {key}: {value}")

        print(f"\nMetrics DataFrame shape: {metrics_df.shape}")
        print(f"Columns: {list(metrics_df.columns)}")
        print(f"\nFirst few rows:")
        print(metrics_df.head())

        print("\nModule B test run completed successfully.")
    except Exception as e:
        print(f"Error during test: {e}")
