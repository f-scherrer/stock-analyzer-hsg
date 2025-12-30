##################################################
# Market Metrics - Streamlit Web UI
# Author: Florian Scherrer
# Python version: 3.13.x (project standard)
#
# Description:
# Main application entry point. Provides a modern web interface
# for stock market analytics using Streamlit.
#
# Features:
# - Stock ticker search
# - Module 1: Stock data (yfinance)
# - Module 2: KPI calculations
# - Module 3: Charts & visualizations
# - Module 4: Company news (Finnhub)
# - Module 5: Sentiment analysis
#
# Requirements:
# - pip install streamlit pandas yfinance requests python-dotenv
# - pip install transformers torch matplotlib
##################################################

import streamlit as st
import pandas as pd
from datetime import datetime, timedelta

# Import modules using standard names (no numeric prefixes)
from data_module.get_stock_data import stock_data
from kpi_module.calculate_kpis import compute_kpis
from charting_module.make_charts import (
    plot_price,
    plot_sma,
    plot_daily_returns,
)
from news_module.get_news import fetch_news
from sentiment_module.get_sentiment import analyze_articles

# Try to load environment variables from .env
try:
    from dotenv import load_dotenv
    import os
    load_dotenv()
except Exception:
    pass

# Set page config
st.set_page_config(
    page_title="Market Metrics - Stock Analytics Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================================
# SIDEBAR - Configuration & Search
# ============================================================================
st.sidebar.title("Configuration")

ticker = st.sidebar.text_input(
    "Search Ticker Symbol",
    value="AAPL",
    placeholder="e.g., AAPL, GOOGL, MSFT",
    help="Enter a valid stock ticker symbol"
)

# Date range selector
st.sidebar.markdown("### Date Range")
period_options = {
    "5 Days": "5d",
    "1 Month": "1mo",
    "3 Months": "3mo",
    "6 Months": "6mo",
    "1 Year": "1y",
    "2 Years": "2y",
    "5 Years": "5y",
    "Max": "max"
}
selected_period = st.sidebar.selectbox("Period", list(period_options.keys()), index=1)
period = period_options[selected_period]

# Interval selector
st.sidebar.markdown("### Interval")
interval_options = {
    "1 Minute": "1m",
    "5 Minutes": "5m",
    "15 Minutes": "15m",
    "30 Minutes": "30m",
    "1 Hour": "1h",
    "1 Day": "1d",
    "1 Week": "1wk",
    "1 Month": "1mo"
}
selected_interval = st.sidebar.selectbox("Interval", list(interval_options.keys()), index=5)
interval = interval_options[selected_interval]

# Module toggles
st.sidebar.markdown("### Modules")
show_data = st.sidebar.checkbox("Market Data", value=True)
show_kpi = st.sidebar.checkbox("Key Metrics", value=True)
show_charts = st.sidebar.checkbox("Technical Analysis", value=True)
show_news = st.sidebar.checkbox("Market News", value=True)
show_sentiment = st.sidebar.checkbox("Market Sentiment", value=True)

# ============================================================================
# MAIN CONTENT
# ============================================================================
st.title(f"Market Metrics - {ticker}")

st.markdown(f"""
**Configuration:**  
Period: `{selected_period}` | Interval: `{selected_interval}`  
Last Updated: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`
""")

# Store data in session state to avoid refetching
# Use cache key to invalidate when ticker/period/interval changes
cache_key = f"{ticker}_{period}_{interval}"

if "last_cache_key" not in st.session_state:
    st.session_state.last_cache_key = None
if "stock_df" not in st.session_state:
    st.session_state.stock_df = None
if "metrics_dict" not in st.session_state:
    st.session_state.metrics_dict = None
if "metrics_df" not in st.session_state:
    st.session_state.metrics_df = None
if "news_articles" not in st.session_state:
    st.session_state.news_articles = None
if "sentiment_articles" not in st.session_state:
    st.session_state.sentiment_articles = None

# Clear cache if ticker/period/interval changed
if st.session_state.last_cache_key != cache_key:
    st.session_state.stock_df = None
    st.session_state.metrics_dict = None
    st.session_state.metrics_df = None
    st.session_state.news_articles = None
    st.session_state.sentiment_articles = None
    st.session_state.last_cache_key = cache_key

# ============================================================================
# MODULE 1: Stock Data
# ============================================================================
if show_data:
    st.markdown("---")
    st.subheader("Market Data")
    
    try:
        # Fetch stock data
        if st.session_state.stock_df is None or st.session_state.stock_df.empty:
            with st.spinner(f"Loading stock data for {ticker}..."):
                st.session_state.stock_df = stock_data(ticker, period, interval)
        
        stock_df = st.session_state.stock_df
        
        with st.expander("Show Stock Data Table", expanded=False):
            st.dataframe(stock_df, width="stretch")
            st.info(f"Loaded {len(stock_df)} rows of data")
        
    except Exception as e:
        st.error(f"Error loading stock data: {str(e)}")
        stock_df = None

# ============================================================================
# MODULE 2: KPI Metrics
# ============================================================================
if show_kpi and show_data:
    st.markdown("---")
    st.subheader("Key Metrics")
    
    try:
        if st.session_state.stock_df is not None and not st.session_state.stock_df.empty:
            if st.session_state.metrics_dict is None:
                st.session_state.metrics_dict, st.session_state.metrics_df = compute_kpis(
                    st.session_state.stock_df
                )
            
            metrics_dict = st.session_state.metrics_dict
            metrics_df = st.session_state.metrics_df
            
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Avg Close", f"${metrics_dict['avg_close']:.2f}")
            
            with col2:
                st.metric("Max Close", f"${metrics_dict['max_close']:.2f}")
            
            with col3:
                st.metric("Min Close", f"${metrics_dict['min_close']:.2f}")
            
            with col4:
                st.metric("Volatility", f"{metrics_dict['volatility']:.4f}")
            
            st.info("KPI metrics calculated successfully")
        else:
            st.info("Load Module 1 data first to calculate KPIs")
            
    except Exception as e:
        st.error(f"Error calculating KPIs: {str(e)}")

# ============================================================================
# MODULE 3: Charts & Visualizations
# ============================================================================
if show_charts and show_data and show_kpi:
    st.markdown("---")
    st.subheader("Technical Analysis")
    
    try:
        if st.session_state.metrics_df is not None and not st.session_state.metrics_df.empty:
            # Need to add Date column for charts
            metrics_df_with_date = st.session_state.metrics_df.copy()
            metrics_df_with_date["Date"] = st.session_state.stock_df["Date"].values
            
            chart_tab1, chart_tab2, chart_tab3 = st.tabs(
                ["Closing Price", "Moving Averages", "Daily Returns"]
            )
            
            with chart_tab1:
                fig_price = plot_price(metrics_df_with_date)
                st.pyplot(fig_price)
            
            with chart_tab2:
                fig_sma = plot_sma(metrics_df_with_date)
                st.pyplot(fig_sma)
            
            with chart_tab3:
                fig_returns = plot_daily_returns(metrics_df_with_date)
                st.pyplot(fig_returns)
            
            st.info("Charts rendered successfully")
        else:
            st.info("Calculate Module 2 KPIs first to display charts")
            
    except Exception as e:
        st.error(f"Error rendering charts: {str(e)}")

# ============================================================================
# MODULE 4: Company News
# ============================================================================
if show_news:
    st.markdown("---")
    st.subheader("Market News")
    
    news_col1, news_col2 = st.columns([3, 1])
    
    with news_col2:
        max_news_items = st.slider("Max News Items", 1, 20, 5)
    
    with news_col1:
        pass
    
    try:
        if st.session_state.news_articles is None:
            with st.spinner(f"Loading news for {ticker}..."):
                # Set date range based on selected period
                end_date = datetime.now().strftime("%Y-%m-%d")
                period_days_map = {
                    "5d": 5, "1mo": 30, "3mo": 90, "6mo": 180,
                    "1y": 365, "2y": 730, "5y": 1825, "max": 3650
                }
                days_back = period_days_map.get(period, 30)
                start_date = (datetime.now() - timedelta(days=days_back)).strftime("%Y-%m-%d")
                
                st.session_state.news_articles = fetch_news(
                    ticker, start_date, end_date, max_items=max_news_items
                )
        
        news_articles = st.session_state.news_articles
        
        if news_articles:
            st.info(f"Found {len(news_articles)} news articles")
            
            for idx, article in enumerate(news_articles):
                published_date = article['published'].split(' ')[0]
                with st.expander(f"[{published_date}] {article['title'][:50]}..."):
                    st.markdown(f"**Date:** {article['published']}")
                    st.markdown(f"**Publisher:** {article['publisher']}")
                    st.markdown(f"**Summary:** {article['summary']}")
                    st.markdown(f"[Read full article]({article['link']})")
        else:
            st.info("No news articles found for this ticker")
            
    except Exception as e:
        st.error(f"Error loading news: {str(e)}")

# ============================================================================
# MODULE 5: Sentiment Analysis
# ============================================================================
if show_sentiment and show_news:
    st.markdown("---")
    st.subheader("Market Sentiment")
    
    try:
        if st.session_state.news_articles is not None and st.session_state.news_articles:
            if st.session_state.sentiment_articles is None:
                with st.spinner("Analyzing sentiment..."):
                    st.session_state.sentiment_articles = analyze_articles(
                        st.session_state.news_articles
                    )
            
            sentiment_articles = st.session_state.sentiment_articles
            
            # Calculate sentiment distribution
            buy_count = sum(1 for a in sentiment_articles if a.get("sentiment") == "BUY")
            hold_count = sum(1 for a in sentiment_articles if a.get("sentiment") == "HOLD")
            sell_count = sum(1 for a in sentiment_articles if a.get("sentiment") == "SELL")
            total = len(sentiment_articles)
            
            col1, col2, col3 = st.columns(3)
            
            with col1:
                st.metric("BUY", f"{buy_count} ({100*buy_count//total}%)")
            
            with col2:
                st.metric("HOLD", f"{hold_count} ({100*hold_count//total}%)")
            
            with col3:
                st.metric("SELL", f"{sell_count} ({100*sell_count//total}%)")
            
            st.info("Sentiment analysis completed")
            
            # Show detailed sentiment for each article
            st.markdown("#### Detailed Sentiment Analysis")
            for article in sentiment_articles:
                published_date = article['published'].split(' ')[0]
                with st.expander(f"[{published_date}] {article['title'][:50]}... ({article['sentiment']})"):
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"**Date:** {article['published']}")
                        st.markdown(f"**Sentiment:** {article['sentiment']}")
                        st.markdown(f"**Confidence:** {article['score']:.2%}")
                        st.markdown(f"**Raw Label:** {article['raw_label']}")
                    with col2:
                        st.metric("Score", f"{article['score']:.4f}")
        else:
            st.info("Load Module 4 news first to perform sentiment analysis")
            
    except Exception as e:
        st.error(f"Error analyzing sentiment: {str(e)}")

# ============================================================================
# FOOTER
# ============================================================================
st.markdown("---")
st.caption("Market Metrics | Data powered by yfinance, Finnhub, and custom analysis")
