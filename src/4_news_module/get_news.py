##################################################
# Module D - News Fetcher (simple version)
# Python version: 3.13.2
# Author: Yanick Meier
# Description:
# Gets news about a stock ticker using yfinance
# and returns them in a simple standard format.
#
# Notes:
# - The function checks that start_date and end_date have the correct format.
# - The function fetches the latest news items from yfinance.
# - The function builds a clean list of article dictionaries.
#
# Important:
# yfinance news items in this environment only contain "id" and "content".
# This means:
# - We cannot filter by date.
# - We cannot use real titles or publishers.
# - We use simple placeholder values instead.
##################################################

import yfinance as yf
from datetime import datetime


def fetch_news(ticker, start_date, end_date, max_items=50):

    print("Starting news fetch process")

    # Check date format (just to validate input)
    try:
        print("Checking date strings format")
        datetime.strptime(start_date, "%Y-%m-%d")
        datetime.strptime(end_date, "%Y-%m-%d")
    except ValueError:
        print("Error - invalid date format, please use YYYY-MM-DD")
        return []

    # Load ticker object
    print(f"Loading ticker object for: {ticker}")
    stock = yf.Ticker(ticker)

    # Fetch raw news
    print("Fetching raw news list")
    raw_news = stock.news or []

    print(f"Found {len(raw_news)} raw news items")

    if len(raw_news) > 0:
        print("Example raw news keys:", list(raw_news[0].keys()))

    articles = []

    # Take latest news (we cannot filter by date)
    for item in raw_news[:max_items]:

        # Get the nested content dict if available
        content_raw = item.get("content", {})

        # If content is a dict, we can read fields like "title"
        if isinstance(content_raw, dict):
            title = content_raw.get("title") or "No title available"
            summary = (
                content_raw.get("summary")
                or content_raw.get("body")
                or "No summary available"
            )
        else:
            # Fallback: treat content as plain text
            content_text = str(content_raw)
            title = content_text[:80] + "..." if content_text else "No title available"
            summary = content_text or "No summary available"

        # Default publisher
        publisher = "Yahoo Finance"

        # Build link using ID if possible
        if "id" in item:
            link = f"https://finance.yahoo.com/news/{item['id']}"
        else:
            link = "No link available"

        # No publish date in yfinance output
        published_str = "Unknown date"

        # Final article dictionary
        article = {
            "title": title,
            "publisher": publisher,
            "summary": summary,
            "link": link,
            "published": published_str
        }

        articles.append(article)

    print(f"News fetch process finished, returning {len(articles)} items")
    return articles


##################################################
# Simple test block
##################################################

if __name__ == "__main__":

    print("Running simple test for Module D")

    test_ticker = "AAPL"
    test_start = "2023-01-01"
    test_end = "2025-01-01"

    result = fetch_news(test_ticker, test_start, test_end, max_items=5)

    print("\nTest results:")
    for a in result:
        print(a["published"], "|", a["publisher"], "|", a["title"])
