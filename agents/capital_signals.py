"""Capital Signals: monitors funding opportunities and investment signals for SAF projects.

Tracks climate finance, grants, concessional debt, and blended finance opportunities
relevant to sustainable aviation fuel development in Africa.
"""
from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "capital_signals.json"

# Funding types
FUNDING_TYPES = ["Grant", "Concessional Loan", "Equity", "Blended Finance", "Technical Assistance"]

# Mock funding opportunities
MOCK_SIGNALS = [
    {
        "source": "Green Climate Fund",
        "title": "GCF Readiness Support for SAF Project Development in West Africa",
        "amount_usd": 2500000,
        "funding_type": "Grant",
        "url": "https://www.greenclimate.fund/project/readiness-saf-west-africa",
        "deadline": "2025-06-30",
        "eligibility": ["Nigeria", "Ghana", "Senegal"],
        "focus_areas": ["SAF", "biofuels", "climate mitigation"],
    },
    {
        "source": "African Development Bank",
        "title": "AfDB SEFA Grant for Sustainable Aviation Feasibility Studies",
        "amount_usd": 1000000,
        "funding_type": "Technical Assistance",
        "url": "https://www.afdb.org/sefa-saf-feasibility",
        "deadline": "2025-04-15",
        "eligibility": ["African Union Member States"],
        "focus_areas": ["feasibility study", "SAF", "aviation decarbonization"],
    },
    {
        "source": "EU Global Gateway",
        "title": "Team Europe Initiative: African Green Hydrogen and SAF Corridor",
        "amount_usd": 50000000,
        "funding_type": "Blended Finance",
        "url": "https://ec.europa.eu/global-gateway/africa-saf-corridor",
        "deadline": "2025-09-01",
        "eligibility": ["ECOWAS countries"],
        "focus_areas": ["green hydrogen", "SAF", "infrastructure"],
    },
    {
        "source": "USAID Power Africa",
        "title": "Off-Grid Bioenergy for SAF Feedstock Processing",
        "amount_usd": 5000000,
        "funding_type": "Grant",
        "url": "https://www.usaid.gov/powerafrica/bioenergy-saf",
        "deadline": "2025-05-20",
        "eligibility": ["Nigeria", "Kenya", "South Africa"],
        "focus_areas": ["bioenergy", "feedstock processing", "rural electrification"],
    },
    {
        "source": "Climate Investment Funds",
        "title": "CIF Accelerating Coal Transition - Biofuels Alternative Track",
        "amount_usd": 15000000,
        "funding_type": "Concessional Loan",
        "url": "https://www.cif.org/act-biofuels",
        "deadline": "2025-08-15",
        "eligibility": ["CIF eligible countries"],
        "focus_areas": ["just transition", "biofuels", "SAF"],
    },
    {
        "source": "Shell Foundation",
        "title": "Cassava-to-SAF Value Chain Development Grant",
        "amount_usd": 750000,
        "funding_type": "Grant",
        "url": "https://shellfoundation.org/cassava-saf",
        "deadline": "Rolling",
        "eligibility": ["Nigeria", "Tanzania", "Mozambique"],
        "focus_areas": ["cassava", "value chain", "SAF"],
    },
    {
        "source": "IFC",
        "title": "IFC Upstream: Early-Stage SAF Project Preparation Facility",
        "amount_usd": 3000000,
        "funding_type": "Technical Assistance",
        "url": "https://www.ifc.org/upstream-saf",
        "deadline": "2025-07-01",
        "eligibility": ["IDA countries"],
        "focus_areas": ["project preparation", "SAF", "bankability"],
    },
]


def generate_mock_signals(count: int = 4) -> list[dict]:
    """Generate mock capital signals."""
    selected = random.sample(MOCK_SIGNALS, min(count, len(MOCK_SIGNALS)))
    signals = []

    for signal in selected:
        # Generate discovery timestamp
        days_ago = random.randint(0, 14)
        timestamp = datetime.now(timezone.utc) - timedelta(days=days_ago)

        signals.append({
            "timestamp": timestamp.isoformat(),
            "source": signal["source"],
            "title": signal["title"],
            "amount_usd": signal["amount_usd"],
            "funding_type": signal["funding_type"],
            "url": signal["url"],
            "deadline": signal["deadline"],
            "eligibility": signal["eligibility"],
            "focus_areas": signal["focus_areas"],
            "relevance_score": random.randint(70, 99),
            "mode": "mock",
        })

    return signals


def load_existing_signals(path: Path) -> list[dict]:
    """Load existing signals from file."""
    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except json.JSONDecodeError:
            return []
    return []


def persist_signals(new_signals: list[dict], path: Path) -> None:
    """Persist new signals to file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = load_existing_signals(path)

    # Append new signals
    all_signals = existing + new_signals

    # Keep only the most recent 30 signals
    all_signals = sorted(all_signals, key=lambda x: x["timestamp"], reverse=True)[:30]

    with path.open("w", encoding="utf-8") as handle:
        json.dump(all_signals, handle, ensure_ascii=False, indent=2)


def run(mock: bool = True) -> list[dict]:
    """Run the capital signals agent."""
    if not mock:
        raise NotImplementedError("Live funding monitoring is not implemented yet.")

    count = random.randint(3, 5)
    signals = generate_mock_signals(count)
    persist_signals(signals, DATA_PATH)

    return signals


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Capital Signals Agent")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Attempt live monitoring (not implemented; defaults to mock).",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()
    signals = run(mock=not args.live)
    print(json.dumps(signals, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
