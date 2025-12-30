"""Regulatory Sentry: monitors aviation regulatory feeds for SAF/CORSIA updates.

Runs in mock mode (default) to simulate regulatory alerts from ICAO, EASA, and NCAA.
In live mode, monitors RSS feeds and web pages for SAF-related keywords.
"""
from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "regulatory_alerts.json"

# Keywords to monitor
KEYWORDS = [
    "SAF",
    "sustainable aviation fuel",
    "CORSIA",
    "LCAF",
    "carbon offset",
    "aviation emissions",
    "alternative fuel",
]

# Mock data for testing
MOCK_ALERTS = [
    {
        "source": "ICAO",
        "title": "CORSIA Implementation Update: New SAF Sustainability Criteria",
        "url": "https://www.icao.int/environmental-protection/corsia/saf-criteria-2025",
        "keywords_matched": ["CORSIA", "SAF", "sustainable aviation fuel"],
    },
    {
        "source": "EASA",
        "title": "ReFuelEU Aviation: Updated Guidance on SAF Blending Mandates",
        "url": "https://www.easa.europa.eu/refueleu-aviation-saf-guidance",
        "keywords_matched": ["SAF", "sustainable aviation fuel", "alternative fuel"],
    },
    {
        "source": "NCAA",
        "title": "NCAA Publishes Draft SAF Certification Framework for Nigerian Operators",
        "url": "https://www.ncaa.gov.ng/saf-certification-draft-2025",
        "keywords_matched": ["SAF", "sustainable aviation fuel"],
    },
    {
        "source": "ICAO",
        "title": "LCAF Forum Announces New Aviation Emissions Monitoring Protocols",
        "url": "https://www.icao.int/environmental-protection/lcaf-emissions-protocols",
        "keywords_matched": ["LCAF", "aviation emissions", "carbon offset"],
    },
    {
        "source": "EASA",
        "title": "European SAF Registry Launch: Tracking Alternative Fuel Production",
        "url": "https://www.easa.europa.eu/saf-registry-launch",
        "keywords_matched": ["SAF", "alternative fuel"],
    },
]


def generate_mock_alerts(count: int = 3) -> list[dict]:
    """Generate mock regulatory alerts."""
    selected = random.sample(MOCK_ALERTS, min(count, len(MOCK_ALERTS)))
    alerts = []

    for i, alert in enumerate(selected):
        # Generate timestamps spread over the past few days
        days_ago = random.randint(0, 7)
        hours_ago = random.randint(0, 23)
        timestamp = datetime.now(timezone.utc) - timedelta(days=days_ago, hours=hours_ago)

        alerts.append({
            "timestamp": timestamp.isoformat(),
            "source": alert["source"],
            "title": alert["title"],
            "url": alert["url"],
            "keywords_matched": alert["keywords_matched"],
            "mode": "mock",
        })

    return alerts


def load_existing_alerts(path: Path) -> list[dict]:
    """Load existing alerts from file."""
    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except json.JSONDecodeError:
            return []
    return []


def persist_alerts(new_alerts: list[dict], path: Path) -> None:
    """Persist new alerts to file (appending to existing)."""
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = load_existing_alerts(path)

    # Append new alerts
    all_alerts = existing + new_alerts

    # Keep only the most recent 50 alerts to prevent file bloat
    all_alerts = sorted(all_alerts, key=lambda x: x["timestamp"], reverse=True)[:50]

    with path.open("w", encoding="utf-8") as handle:
        json.dump(all_alerts, handle, ensure_ascii=False, indent=2)


def run(mock: bool = True) -> list[dict]:
    """Run the regulatory sentry and return generated alerts."""
    if not mock:
        raise NotImplementedError("Live monitoring mode is not implemented yet.")

    # Generate 2-3 mock alerts
    count = random.randint(2, 3)
    alerts = generate_mock_alerts(count)
    persist_alerts(alerts, DATA_PATH)

    return alerts


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Regulatory Sentry")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Attempt live monitoring (not implemented; defaults to mock).",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()
    alerts = run(mock=not args.live)
    print(json.dumps(alerts, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
