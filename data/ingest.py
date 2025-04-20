import argparse
import datetime
from pathlib import Path

import pandas as pd
import yfinance as yf

# Directories for raw and processed data
BASE_DIR = Path(__file__).resolve().parents[2]
RAW_DIR = BASE_DIR / "data" / "raw"
PROCESSED_DIR = BASE_DIR / "data" / "processed"


def fetch_data(ticker: str,
               start: str = "2020-01-01",
               end: str = None,
               interval: str = "1d") -> pd.DataFrame:
    """
    Fetch historical OHLCV data for a given ticker from Yahoo Finance.
    """
    if end is None:
        end = datetime.date.today().isoformat()
    df = yf.download(ticker, start=start, end=end, interval=interval)
    df.dropna(inplace=True)
    return df


def save_raw_data(df: pd.DataFrame, ticker: str) -> Path:
    """
    Save the raw DataFrame to a CSV in the raw data directory.
    """
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    file_path = RAW_DIR / f"{ticker}_{datetime.date.today().isoformat()}.csv"
    df.to_csv(file_path)
    print(f"[Data Ingest] Saved raw data to {file_path}")
    return file_path


def load_raw_data(file_path: Path) -> pd.DataFrame:
    """
    Load raw CSV data into a DataFrame.
    """
    return pd.read_csv(file_path, index_col=0, parse_dates=True)


def clean_data(df: pd.DataFrame) -> pd.DataFrame:
    """
    Perform basic cleaning: remove duplicates, sort index, fill missing values.
    """
    df = df.drop_duplicates()
    df = df.sort_index()
    df = df.ffill().bfill()
    return df


def save_processed_data(df: pd.DataFrame, ticker: str) -> Path:
    """
    Save the cleaned DataFrame to a CSV in the processed data directory.
    """
    PROCESSED_DIR.mkdir(parents=True, exist_ok=True)
    file_path = PROCESSED_DIR / f"{ticker}_{datetime.date.today().isoformat()}_cleaned.csv"
    df.to_csv(file_path)
    print(f"[Data Ingest] Saved processed data to {file_path}")
    return file_path


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Fetch and clean market data")
    parser.add_argument("ticker", type=str, help="Ticker symbol, e.g. SPY")
    parser.add_argument("--start", type=str, default="2020-01-01", help="Start date (YYYY-MM-DD)")
    parser.add_argument("--end", type=str, help="End date (YYYY-MM-DD). Defaults to today.")
    parser.add_argument("--interval", type=str, default="1d", help="Data interval (e.g. 1d, 1h)")
    args = parser.parse_args()

    # Fetch raw data
    raw_df = fetch_data(args.ticker, args.start, args.end, args.interval)
    raw_path = save_raw_data(raw_df, args.ticker)

    # Clean and save processed data
    cleaned_df = clean_data(raw_df)
    save_processed_data(cleaned_df, args.ticker)
