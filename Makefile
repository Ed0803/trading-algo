.PHONY: fetch-data preprocess train backtest test clean

fetch-data:
    python -m src.data.fetch --ticker SPY

preprocess:
    python -m src.data.clean

train:
    python -m src.models.train --config config/train.yaml

backtest:
    python -m src.backtest.run --strategy MACrossover

test:
    pytest --maxfail=1 --disable-warnings -q

clean:
    rm -rf data/processed models/*.pkl reports/figures/*
