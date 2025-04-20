# Algo‑Trading Project

## 📌 Overview
A machine‑learning‑driven trading pipeline that ingests market data, engineers features, trains models, backtests strategies, and (optionally) trades live via broker APIs.

## 🚀 Quickstart
```bash
git clone <repo-url>
cd algo-trading-project
conda env create -f environment.yml
conda activate trading-env
make fetch-data
jupyter lab notebooks/01-data-ingest.ipynb
