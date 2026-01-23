"""Technology Diligence: monitors SAF production pathways and technical developments.

Tracks HEFA, ETJ, AtJ, FT, and other SAF production pathway economics,
certifications, and technological breakthroughs.

Data Sources:
- RSB Certification Database: rsb.org/certification/rsb-certificates/
- ICAO CORSIA Eligible Fuels: icao.int/CORSIA/corsia-certified-fuels
- NREL Annual Technology Baseline: atb.nrel.gov
- CAAFI Updates: caafi.org
"""
from __future__ import annotations

import argparse
import json
import random
from datetime import datetime, timezone, timedelta
from pathlib import Path

try:
    import requests
    REQUESTS_AVAILABLE = True
except ImportError:
    REQUESTS_AVAILABLE = False

# Import data sources configuration
try:
    from data_sources import TECHNOLOGY_SOURCES
except ImportError:
    TECHNOLOGY_SOURCES = {}

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "technology_updates.json"

# Live data source URLs
LIVE_SOURCES = {
    "rsb": {
        "name": "RSB Certification Database",
        "base_url": "https://rsb.org/certification/rsb-certificates/",
    },
    "icao_corsia": {
        "name": "ICAO CORSIA Eligible Fuels",
        "base_url": "https://www.icao.int/CORSIA/corsia-certified-fuels",
    },
    "nrel_atb": {
        "name": "NREL Annual Technology Baseline",
        "base_url": "https://atb.nrel.gov",
    },
    "caafi": {
        "name": "CAAFI",
        "base_url": "https://www.caafi.org/",
    }
}

# SAF Pathways
PATHWAYS = {
    "HEFA": "Hydroprocessed Esters and Fatty Acids",
    "ETJ": "Ethanol-to-Jet",
    "AtJ": "Alcohol-to-Jet",
    "FT": "Fischer-Tropsch",
    "CHJ": "Catalytic Hydrothermolysis",
    "HC-HEFA": "Hydroprocessed Hydrocarbons",
    "Co-processing": "Refinery Co-processing",
}

# Mock technology updates
MOCK_UPDATES = [
    {
        "source": "ASTM International",
        "title": "ASTM D7566 Annex 7 Updated: Increased ETJ Blend Limit to 50%",
        "pathway": "ETJ",
        "update_type": "Certification",
        "url": "https://www.astm.org/d7566-annex7-update",
        "significance": "Major regulatory milestone enabling higher ETJ blending",
        "impact_score": 95,
    },
    {
        "source": "Neste",
        "title": "Neste Singapore Expansion: 1.3M Tonnes SAF Capacity by 2026",
        "pathway": "HEFA",
        "update_type": "Capacity Expansion",
        "url": "https://www.neste.com/singapore-expansion",
        "significance": "Largest SAF production facility globally",
        "impact_score": 88,
    },
    {
        "source": "LanzaJet",
        "title": "LanzaJet Georgia Plant Achieves First Commercial ATJ Production",
        "pathway": "AtJ",
        "update_type": "Commercial Milestone",
        "url": "https://www.lanzajet.com/georgia-commercial",
        "significance": "First commercial-scale ATJ facility in the Americas",
        "impact_score": 92,
    },
    {
        "source": "ICAO CORSIA",
        "title": "CORSIA Eligible Fuels: New Cassava Ethanol Pathway Approved",
        "pathway": "ETJ",
        "update_type": "Certification",
        "url": "https://www.icao.int/corsia/eligible-fuels-cassava",
        "significance": "Opens pathway for African cassava-based SAF",
        "impact_score": 97,
    },
    {
        "source": "Argonne National Lab",
        "title": "GREET Model Update: Revised LCA for Tropical Feedstocks",
        "pathway": "ETJ",
        "update_type": "Research",
        "url": "https://greet.es.anl.gov/tropical-feedstocks",
        "significance": "Improved carbon intensity calculations for cassava and sugarcane",
        "impact_score": 75,
    },
    {
        "source": "World Energy",
        "title": "World Energy Achieves 100% SAF Production at Paramount Facility",
        "pathway": "HEFA",
        "update_type": "Commercial Milestone",
        "url": "https://www.worldenergy.net/paramount-100-saf",
        "significance": "First facility producing neat SAF at commercial scale",
        "impact_score": 90,
    },
    {
        "source": "RSB",
        "title": "Roundtable on Sustainable Biomaterials: New African Certification Scheme",
        "pathway": "Multiple",
        "update_type": "Certification",
        "url": "https://rsb.org/africa-certification",
        "significance": "Simplified sustainability certification for African producers",
        "impact_score": 82,
    },
    {
        "source": "Gevo",
        "title": "Gevo Net-Zero 1 Project Secures Final Investment Decision",
        "pathway": "AtJ",
        "update_type": "Investment",
        "url": "https://gevo.com/net-zero-1-fid",
        "significance": "Major AtJ project advancement in the US",
        "impact_score": 85,
    },
]

# Pathway economics benchmarks ($/gallon production cost estimates)
PATHWAY_ECONOMICS = {
    "HEFA": {"min": 3.50, "max": 5.00, "trend": "stable"},
    "ETJ": {"min": 4.00, "max": 6.50, "trend": "declining"},
    "AtJ": {"min": 4.50, "max": 7.00, "trend": "declining"},
    "FT": {"min": 5.00, "max": 8.00, "trend": "stable"},
    "Co-processing": {"min": 2.50, "max": 4.00, "trend": "stable"},
}


def generate_mock_updates(count: int = 3) -> list[dict]:
    """Generate mock technology updates."""
    selected = random.sample(MOCK_UPDATES, min(count, len(MOCK_UPDATES)))
    updates = []

    for update in selected:
        days_ago = random.randint(0, 21)
        timestamp = datetime.now(timezone.utc) - timedelta(days=days_ago)

        updates.append({
            "timestamp": timestamp.isoformat(),
            "source": update["source"],
            "title": update["title"],
            "pathway": update["pathway"],
            "pathway_full": PATHWAYS.get(update["pathway"], update["pathway"]),
            "update_type": update["update_type"],
            "url": update["url"],
            "significance": update["significance"],
            "impact_score": update["impact_score"],
            "mode": "mock",
        })

    return updates


def generate_pathway_snapshot() -> dict:
    """Generate current pathway economics snapshot."""
    snapshot = {}
    for pathway, economics in PATHWAY_ECONOMICS.items():
        current_cost = round(random.uniform(economics["min"], economics["max"]), 2)
        snapshot[pathway] = {
            "name": PATHWAYS[pathway],
            "cost_per_gallon_usd": current_cost,
            "cost_range": f"${economics['min']:.2f} - ${economics['max']:.2f}",
            "trend": economics["trend"],
            "jet_fuel_parity_gap": round(current_cost - 2.50, 2),  # Assuming $2.50/gal conventional
        }
    return snapshot


def load_existing_updates(path: Path) -> list[dict]:
    """Load existing updates from file."""
    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except json.JSONDecodeError:
            return []
    return []


def persist_updates(new_updates: list[dict], path: Path) -> None:
    """Persist updates to file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = load_existing_updates(path)

    # Append new updates
    all_updates = existing + new_updates

    # Keep only the most recent 40 updates
    all_updates = sorted(all_updates, key=lambda x: x["timestamp"], reverse=True)[:40]

    with path.open("w", encoding="utf-8") as handle:
        json.dump(all_updates, handle, ensure_ascii=False, indent=2)


def run(mock: bool = True) -> dict:
    """Run the technology diligence agent."""
    if not mock:
        raise NotImplementedError("Live technology monitoring is not implemented yet.")

    count = random.randint(2, 4)
    updates = generate_mock_updates(count)
    persist_updates(updates, DATA_PATH)

    return {
        "updates": updates,
        "pathway_economics": generate_pathway_snapshot(),
    }


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Technology Diligence Agent")
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
