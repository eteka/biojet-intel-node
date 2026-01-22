"""Market Access: monitors airline SAF commitments and offtake opportunities.

Tracks airline sustainability pledges, SAF purchase agreements, airport infrastructure,
and demand signals relevant to West African SAF producers.
"""
from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "market_access.json"

# Regions of interest
REGIONS = ["West Africa", "Europe", "Middle East", "Global"]

# Mock airline commitments and offtake signals
MOCK_SIGNALS = [
    {
        "airline": "Ethiopian Airlines",
        "region": "Africa",
        "signal_type": "SAF Commitment",
        "title": "Ethiopian Airlines Commits to 10% SAF by 2030",
        "volume_tonnes": 50000,
        "timeframe": "2025-2030",
        "url": "https://www.ethiopianairlines.com/sustainability/saf-commitment",
        "relevance": "Direct West African market access opportunity",
    },
    {
        "airline": "Air France-KLM",
        "region": "Europe",
        "signal_type": "Offtake RFP",
        "title": "Air France-KLM Issues RFP for African-Origin SAF Supply",
        "volume_tonnes": 100000,
        "timeframe": "2026-2030",
        "url": "https://www.airfranceklm.com/saf-rfp-africa",
        "relevance": "European carrier seeking African feedstock supply",
    },
    {
        "airline": "Kenya Airways",
        "region": "Africa",
        "signal_type": "Partnership Announcement",
        "title": "Kenya Airways Partners with SkyNRG for SAF Supply Chain Study",
        "volume_tonnes": 25000,
        "timeframe": "2025-2027",
        "url": "https://www.kenya-airways.com/skynrg-partnership",
        "relevance": "Regional carrier building SAF infrastructure",
    },
    {
        "airline": "Emirates",
        "region": "Middle East",
        "signal_type": "SAF Commitment",
        "title": "Emirates Targets 50% SAF Blend for Africa Routes by 2035",
        "volume_tonnes": 200000,
        "timeframe": "2030-2035",
        "url": "https://www.emirates.com/sustainability/saf-africa",
        "relevance": "Major hub carrier with significant West African routes",
    },
    {
        "airline": "British Airways",
        "region": "Europe",
        "signal_type": "Investment",
        "title": "IAG Invests in African Biomass-to-SAF Developer",
        "volume_tonnes": 75000,
        "timeframe": "2027-2032",
        "url": "https://www.iairgroup.com/saf-africa-investment",
        "relevance": "Direct investment in African SAF production",
    },
    {
        "airline": "Air Peace",
        "region": "West Africa",
        "signal_type": "MoU Signed",
        "title": "Air Peace Signs MoU for Nigerian-Produced SAF",
        "volume_tonnes": 15000,
        "timeframe": "2026-2028",
        "url": "https://www.flyairpeace.com/saf-mou",
        "relevance": "Nigerian carrier commitment - key local demand signal",
    },
    {
        "airline": "Qatar Airways",
        "region": "Middle East",
        "signal_type": "SAF Commitment",
        "title": "Qatar Airways Announces Net Zero Plan with African SAF Component",
        "volume_tonnes": 150000,
        "timeframe": "2028-2035",
        "url": "https://www.qatarairways.com/net-zero-saf",
        "relevance": "Major Middle Eastern carrier with Africa hub strategy",
    },
    {
        "airline": "Lufthansa Group",
        "region": "Europe",
        "signal_type": "Offtake Agreement",
        "title": "Lufthansa Signs Long-Term SAF Offtake with Book-and-Claim for Africa",
        "volume_tonnes": 80000,
        "timeframe": "2026-2031",
        "url": "https://www.lufthansagroup.com/saf-africa-offtake",
        "relevance": "Book-and-claim mechanism enables African origin supply",
    },
]

# Airport SAF infrastructure updates
AIRPORT_UPDATES = [
    {
        "airport": "Lagos Murtala Muhammed (LOS)",
        "country": "Nigeria",
        "update_type": "Feasibility Study",
        "title": "Lagos Airport Begins SAF Blending Infrastructure Study",
        "status": "Planning",
    },
    {
        "airport": "Accra Kotoka (ACC)",
        "country": "Ghana",
        "update_type": "Policy Announcement",
        "title": "Ghana Announces SAF Incentive Framework for Kotoka",
        "status": "Policy Development",
    },
    {
        "airport": "Addis Ababa Bole (ADD)",
        "country": "Ethiopia",
        "update_type": "Infrastructure Investment",
        "title": "Bole Airport to Install SAF Blending Facility by 2027",
        "status": "Approved",
    },
]


def generate_mock_signals(count: int = 4) -> list[dict]:
    """Generate mock market access signals."""
    selected = random.sample(MOCK_SIGNALS, min(count, len(MOCK_SIGNALS)))
    signals = []

    for signal in selected:
        days_ago = random.randint(0, 30)
        timestamp = datetime.now(timezone.utc) - timedelta(days=days_ago)

        signals.append({
            "timestamp": timestamp.isoformat(),
            "airline": signal["airline"],
            "region": signal["region"],
            "signal_type": signal["signal_type"],
            "title": signal["title"],
            "volume_tonnes_annual": signal["volume_tonnes"],
            "timeframe": signal["timeframe"],
            "url": signal["url"],
            "relevance": signal["relevance"],
            "confidence_score": random.randint(60, 95),
            "mode": "mock",
        })

    return signals


def generate_airport_updates() -> list[dict]:
    """Generate airport infrastructure updates."""
    updates = []
    for airport in AIRPORT_UPDATES:
        days_ago = random.randint(0, 60)
        timestamp = datetime.now(timezone.utc) - timedelta(days=days_ago)

        updates.append({
            "timestamp": timestamp.isoformat(),
            "airport": airport["airport"],
            "country": airport["country"],
            "update_type": airport["update_type"],
            "title": airport["title"],
            "status": airport["status"],
            "mode": "mock",
        })

    return updates


def load_existing_signals(path: Path) -> dict:
    """Load existing signals from file."""
    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except json.JSONDecodeError:
            return {"airline_signals": [], "airport_updates": []}
    return {"airline_signals": [], "airport_updates": []}


def persist_signals(new_data: dict, path: Path) -> None:
    """Persist signals to file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = load_existing_signals(path)

    # Merge airline signals
    all_airline = existing.get("airline_signals", []) + new_data.get("airline_signals", [])
    all_airline = sorted(all_airline, key=lambda x: x["timestamp"], reverse=True)[:25]

    # Merge airport updates
    all_airport = existing.get("airport_updates", []) + new_data.get("airport_updates", [])
    all_airport = sorted(all_airport, key=lambda x: x["timestamp"], reverse=True)[:15]

    output = {
        "airline_signals": all_airline,
        "airport_updates": all_airport,
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }

    with path.open("w", encoding="utf-8") as handle:
        json.dump(output, handle, ensure_ascii=False, indent=2)


def run(mock: bool = True) -> dict:
    """Run the market access agent."""
    if not mock:
        raise NotImplementedError("Live market monitoring is not implemented yet.")

    count = random.randint(3, 5)
    signals = generate_mock_signals(count)
    airports = generate_airport_updates()

    data = {
        "airline_signals": signals,
        "airport_updates": airports,
    }

    persist_signals(data, DATA_PATH)

    return data


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Market Access Agent")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Attempt live monitoring (not implemented; defaults to mock).",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()
    result = run(mock=not args.live)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
