"""Regulatory Sentry: monitors aviation regulatory feeds for SAF/CORSIA updates.

Runs in mock mode (default) to simulate regulatory alerts from ICAO, EASA, and NCAA.
In live mode, monitors RSS feeds and web pages for SAF-related keywords.

Data Sources:
- ICAO Newsroom: icao.int/newsroom
- EASA Newsroom RSS: easa.europa.eu/en/rss
- IATA Sustainability: iata.org/en/publications/newsletters/sustainability-economics-insights/
- NCAA Nigeria: ncaa.gov.ng/media/news/
"""
from __future__ import annotations

import argparse
import json
import random
import re
import xml.etree.ElementTree as ET
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Import data sources configuration
try:
    from data_sources import REGULATORY_SOURCES
except ImportError:
    REGULATORY_SOURCES = {}

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "regulatory_alerts.json"

# Live RSS feed URLs
LIVE_SOURCES = {
    "easa": {
        "name": "EASA Newsroom",
        "rss_url": "https://www.easa.europa.eu/en/rss",
        "base_url": "https://www.easa.europa.eu/en/newsroom",
    },
    "iata": {
        "name": "IATA Sustainability",
        "rss_url": "https://www.iata.org/en/publications/newsletters/sustainability-economics-insights/feed/",
        "base_url": "https://www.iata.org/en/publications/newsletters/sustainability-economics-insights/",
    },
    "icao": {
        "name": "ICAO Environmental",
        "base_url": "https://www.icao.int/environmental-protection/Pages/default.aspx",
        "corsia_url": "https://www.icao.int/CORSIA",
    },
    "ncaa": {
        "name": "NCAA Nigeria",
        "base_url": "https://ncaa.gov.ng/media/news/",
    }
}

# Keywords to monitor
KEYWORDS = [
    "SAF",
    "sustainable aviation fuel",
    "CORSIA",
    "LCAF",
    "carbon offset",
    "aviation emissions",
    "alternative fuel",
    "ReFuelEU",
    "biofuel",
    "net zero",
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


def fetch_rss_feed(url: str, source_name: str) -> list[dict]:
    """
    Fetch and parse an RSS feed for SAF-related content.

    Args:
        url: RSS feed URL
        source_name: Name of the source (e.g., "EASA", "IATA")

    Returns:
        List of alert dictionaries
    """
    if not REQUESTS_AVAILABLE:
        raise ImportError("requests library required for live mode. Run: pip install requests")

    alerts = []
    try:
        response = requests.get(url, timeout=30, headers={
            "User-Agent": "SAF-HUB-Bot/1.0 (Biojet Intelligence Platform)"
        })
        response.raise_for_status()

        # Parse RSS XML
        root = ET.fromstring(response.content)

        # Handle both RSS 2.0 and Atom feeds
        items = root.findall(".//item") or root.findall(".//{http://www.w3.org/2005/Atom}entry")

        for item in items[:20]:  # Limit to 20 most recent
            # Extract title
            title_elem = item.find("title") or item.find("{http://www.w3.org/2005/Atom}title")
            title = title_elem.text if title_elem is not None else ""

            # Extract link
            link_elem = item.find("link") or item.find("{http://www.w3.org/2005/Atom}link")
            if link_elem is not None:
                link = link_elem.text or link_elem.get("href", "")
            else:
                link = ""

            # Extract description
            desc_elem = item.find("description") or item.find("{http://www.w3.org/2005/Atom}summary")
            description = desc_elem.text if desc_elem is not None else ""

            # Extract pub date
            date_elem = item.find("pubDate") or item.find("{http://www.w3.org/2005/Atom}published")
            pub_date = date_elem.text if date_elem is not None else ""

            # Check for keyword matches
            content = f"{title} {description}".lower()
            matched_keywords = [kw for kw in KEYWORDS if kw.lower() in content]

            if matched_keywords:
                alerts.append({
                    "timestamp": datetime.now(timezone.utc).isoformat(),
                    "source": source_name,
                    "title": title.strip() if title else "Untitled",
                    "url": link.strip() if link else "",
                    "keywords_matched": matched_keywords,
                    "pub_date": pub_date,
                    "mode": "live",
                })

    except requests.RequestException as e:
        print(f"Warning: Failed to fetch RSS from {source_name}: {e}")
    except ET.ParseError as e:
        print(f"Warning: Failed to parse RSS from {source_name}: {e}")

    return alerts


def fetch_live_alerts() -> list[dict]:
    """
    Fetch alerts from all live sources.

    Returns:
        Combined list of alerts from all sources
    """
    all_alerts = []

    # Fetch EASA RSS
    if "easa" in LIVE_SOURCES and LIVE_SOURCES["easa"].get("rss_url"):
        easa_alerts = fetch_rss_feed(
            LIVE_SOURCES["easa"]["rss_url"],
            "EASA"
        )
        all_alerts.extend(easa_alerts)

    # Fetch IATA RSS (if available)
    if "iata" in LIVE_SOURCES and LIVE_SOURCES["iata"].get("rss_url"):
        try:
            iata_alerts = fetch_rss_feed(
                LIVE_SOURCES["iata"]["rss_url"],
                "IATA"
            )
            all_alerts.extend(iata_alerts)
        except Exception:
            pass  # IATA feed may not always be available

    return all_alerts


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
        # Live mode: fetch from real RSS feeds
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library required for live mode. Run: pip install requests")

        alerts = fetch_live_alerts()

        if alerts:
            persist_alerts(alerts, DATA_PATH)
            return alerts
        else:
            # Fallback to mock if no live data retrieved
            print("Warning: No live alerts retrieved, falling back to mock mode")
            return run(mock=True)

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
