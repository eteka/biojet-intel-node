"""Feedstock Watchdog: mock cassava peel price generator.

Runs in mock mode (default) to simulate cassava peel price movements
and writes the time-stamped series to data/prices.json.
"""
from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timezone
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "prices.json"


def generate_mock_price(lower: int = 15000, upper: int = 25000) -> int:
    """Generate a mock cassava peel price within the provided range."""
    return random.randint(lower, upper)


def load_existing_records(path: Path) -> list[dict]:
    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except json.JSONDecodeError:
            return []
    return []


def persist_price(record: dict, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    records = load_existing_records(path)
    records.append(record)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(records, handle, ensure_ascii=False, indent=2)


def run(mock: bool = True) -> dict:
    """Run the watchdog in mock mode and return the generated record."""
    if not mock:
        raise NotImplementedError("Live scraping mode is not implemented yet.")

    price = generate_mock_price()
    record = {
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "commodity": "cassava_peel",
        "currency": "NGN",
        "price_per_tonne": price,
        "mode": "mock",
    }
    persist_price(record, DATA_PATH)
    return record


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Feedstock Watchdog")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Attempt live scrape (not implemented; defaults to mock).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    record = run(mock=not args.live)
    print(json.dumps(record, ensure_ascii=False))


if __name__ == "__main__":
    main()
