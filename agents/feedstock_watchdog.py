"""Feedstock Watchdog: monitors cassava and agricultural residue prices.

Runs in mock mode (default) to simulate cassava peel price movements.
In live mode, fetches data from WFP HDX and NBS Nigeria APIs.

Data Sources:
- WFP Nigeria Food Price Dataset (HDX): data.humdata.org/dataset/wfp-food-prices-for-nigeria
- NBS Selected Food Price Watch: nigeria.opendataforafrica.org/gjskat/selected-food-prices-watch
"""
from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timezone
from pathlib import Path

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Import data sources configuration
try:
    from data_sources import FEEDSTOCK_SOURCES
except ImportError:
    FEEDSTOCK_SOURCES = {}

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "prices.json"

# Live data source URLs
LIVE_SOURCES = {
    "wfp_hdx": {
        "name": "WFP Nigeria Food Prices",
        "api_url": "https://data.humdata.org/api/3/action/package_show?id=wfp-food-prices-for-nigeria",
        "data_url": "https://data.humdata.org/dataset/wfp-food-prices-for-nigeria",
    },
    "nbs_nigeria": {
        "name": "NBS Selected Food Price Watch",
        "api_url": "https://nigeria.opendataforafrica.org/api/1.0/data",
        "base_url": "https://nigeria.opendataforafrica.org/gjskat/selected-food-prices-watch",
    },
    "fao_fpma": {
        "name": "FAO Food Price Monitoring",
        "base_url": "https://fpma.fao.org/giews/fpmat4/#/dashboard/tool/domestic",
    }
}

# Cassava-related commodities to filter for
CASSAVA_KEYWORDS = ["cassava", "garri", "gari", "fufu", "tapioca"]


def generate_mock_price(lower: int = 15000, upper: int = 25000) -> int:
    """Generate a mock cassava peel price within the provided range."""
    return random.randint(lower, upper)


def fetch_wfp_hdx_data() -> list[dict]:
    """
    Fetch latest food price data from WFP Humanitarian Data Exchange.

    Returns list of price records for cassava-related commodities.
    """
    if not REQUESTS_AVAILABLE:
        raise ImportError("requests library required for live mode. Run: pip install requests")

    records = []
    try:
        # Get dataset metadata
        response = requests.get(
            LIVE_SOURCES["wfp_hdx"]["api_url"],
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        # Find CSV resource URL
        if data.get("success") and data.get("result", {}).get("resources"):
            for resource in data["result"]["resources"]:
                if resource.get("format", "").upper() == "CSV":
                    csv_url = resource.get("url")
                    if csv_url:
                        # Fetch and parse CSV (simplified - in production use pandas)
                        csv_response = requests.get(csv_url, timeout=60)
                        csv_response.raise_for_status()

                        # Parse CSV lines (basic parsing)
                        lines = csv_response.text.strip().split('\n')
                        if len(lines) > 1:
                            headers = lines[0].lower().split(',')

                            # Find relevant columns
                            commodity_idx = next((i for i, h in enumerate(headers) if 'commodity' in h), -1)
                            price_idx = next((i for i, h in enumerate(headers) if 'price' in h), -1)
                            date_idx = next((i for i, h in enumerate(headers) if 'date' in h), -1)
                            market_idx = next((i for i, h in enumerate(headers) if 'market' in h), -1)

                            # Get last 100 rows and filter for cassava
                            for line in lines[-100:]:
                                cols = line.split(',')
                                if commodity_idx >= 0 and len(cols) > commodity_idx:
                                    commodity = cols[commodity_idx].lower()
                                    if any(kw in commodity for kw in CASSAVA_KEYWORDS):
                                        try:
                                            price = float(cols[price_idx]) if price_idx >= 0 else 0
                                            records.append({
                                                "timestamp": datetime.now(timezone.utc).isoformat(),
                                                "commodity": cols[commodity_idx] if commodity_idx >= 0 else "cassava",
                                                "currency": "NGN",
                                                "price_per_tonne": int(price * 1000),  # Convert to per tonne
                                                "market": cols[market_idx] if market_idx >= 0 else "Nigeria",
                                                "source": "WFP HDX",
                                                "mode": "live",
                                            })
                                        except (ValueError, IndexError):
                                            continue
                    break

    except requests.RequestException as e:
        print(f"Warning: Failed to fetch WFP HDX data: {e}")

    return records


def fetch_nbs_data() -> list[dict]:
    """
    Fetch latest food price data from Nigeria Bureau of Statistics.

    Returns list of price records for cassava-related commodities.
    """
    if not REQUESTS_AVAILABLE:
        raise ImportError("requests library required for live mode. Run: pip install requests")

    records = []
    try:
        # NBS OpenDataForAfrica API endpoint
        # Note: This is a simplified example - actual API may require specific parameters
        response = requests.get(
            LIVE_SOURCES["nbs_nigeria"]["base_url"],
            timeout=30,
            headers={"Accept": "application/json"}
        )

        # If JSON API available, parse it
        if response.status_code == 200:
            # For now, return empty - full implementation would parse the API response
            # The NBS portal may require specific SDMX queries
            pass

    except requests.RequestException as e:
        print(f"Warning: Failed to fetch NBS data: {e}")

    return records


def load_existing_records(path: Path) -> list[dict]:
    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except json.JSONDecodeError:
            return []
    return []


def persist_price(record: dict | list[dict], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    records = load_existing_records(path)

    if isinstance(record, list):
        records.extend(record)
    else:
        records.append(record)

    # Keep only last 50 records to prevent bloat
    records = sorted(records, key=lambda x: x.get("timestamp", ""), reverse=True)[:50]

    with path.open("w", encoding="utf-8") as handle:
        json.dump(records, handle, ensure_ascii=False, indent=2)


def run(mock: bool = True) -> dict | list[dict]:
    """Run the watchdog and return the generated record(s)."""
    if not mock:
        # Live mode: fetch from real APIs
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library required for live mode. Run: pip install requests")

        all_records = []

        # Try WFP HDX first
        wfp_records = fetch_wfp_hdx_data()
        all_records.extend(wfp_records)

        # Try NBS data
        nbs_records = fetch_nbs_data()
        all_records.extend(nbs_records)

        if all_records:
            persist_price(all_records, DATA_PATH)
            return all_records
        else:
            # Fallback to mock if no live data retrieved
            print("Warning: No live data retrieved, falling back to mock mode")
            return run(mock=True)

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
