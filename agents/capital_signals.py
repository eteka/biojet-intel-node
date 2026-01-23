"""Capital Signals: monitors funding opportunities and investment signals for SAF projects.

Tracks climate finance, grants, concessional debt, and blended finance opportunities
relevant to sustainable aviation fuel development in Africa.

Data Sources:
- Green Climate Fund: data.greenclimate.fund
- African Development Bank: dataportal.opendataforafrica.org
- World Bank Projects API: api.worldbank.org/v2/projects
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
    from data_sources import CAPITAL_SOURCES
except ImportError:
    CAPITAL_SOURCES = {}

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "capital_signals.json"

# Live API endpoints
LIVE_SOURCES = {
    "gcf": {
        "name": "Green Climate Fund",
        "api_url": "https://data.greenclimate.fund/public/api/",
        "base_url": "https://data.greenclimate.fund",
    },
    "afdb": {
        "name": "African Development Bank",
        "api_url": "https://dataportal.opendataforafrica.org/api/1.0/data",
        "base_url": "https://projects.afdb.org",
    },
    "world_bank": {
        "name": "World Bank",
        "api_url": "https://api.worldbank.org/v2/projects",
        "format": "json",
    }
}

# Keywords to filter relevant projects
SAF_KEYWORDS = [
    "biofuel", "bioenergy", "SAF", "sustainable aviation",
    "biomass", "ethanol", "renewable fuel", "cassava",
    "agricultural waste", "clean energy", "aviation"
]

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


def fetch_world_bank_projects() -> list[dict]:
    """
    Fetch climate-related projects from World Bank API.

    Filters for Nigeria and energy/climate sectors.
    """
    if not REQUESTS_AVAILABLE:
        raise ImportError("requests library required for live mode")

    signals = []
    try:
        # Query World Bank API for Nigeria climate projects
        params = {
            "format": "json",
            "countrycode": "NG",  # Nigeria
            "sector": "Energy",
            "per_page": 50,
        }

        response = requests.get(
            LIVE_SOURCES["world_bank"]["api_url"],
            params=params,
            timeout=30
        )
        response.raise_for_status()
        data = response.json()

        # Parse projects (World Bank returns array with metadata + data)
        if isinstance(data, list) and len(data) > 1:
            projects = data[1] if len(data) > 1 else []

            for project in projects[:20]:
                # Check if project relates to our keywords
                project_name = project.get("project_name", "")
                sector = project.get("sector1", {}).get("Name", "") if isinstance(project.get("sector1"), dict) else ""
                content = f"{project_name} {sector}".lower()

                if any(kw.lower() in content for kw in SAF_KEYWORDS):
                    signals.append({
                        "timestamp": datetime.now(timezone.utc).isoformat(),
                        "source": "World Bank",
                        "title": project_name,
                        "amount_usd": project.get("totalcommamt", 0),
                        "funding_type": "Loan/Grant",
                        "url": f"https://projects.worldbank.org/en/projects-operations/project-detail/{project.get('id', '')}",
                        "deadline": "Ongoing",
                        "eligibility": ["Nigeria"],
                        "focus_areas": [sector] if sector else ["Energy"],
                        "relevance_score": 75,
                        "mode": "live",
                    })

    except requests.RequestException as e:
        print(f"Warning: Failed to fetch World Bank data: {e}")

    return signals


def fetch_gcf_projects() -> list[dict]:
    """
    Fetch projects from Green Climate Fund.

    Note: GCF API structure may vary - this is a simplified implementation.
    """
    if not REQUESTS_AVAILABLE:
        raise ImportError("requests library required for live mode")

    signals = []
    try:
        # GCF Open Data Library
        response = requests.get(
            f"{LIVE_SOURCES['gcf']['base_url']}/api/projects",
            params={"country": "Nigeria"},
            timeout=30
        )

        if response.status_code == 200:
            try:
                data = response.json()
                projects = data if isinstance(data, list) else data.get("results", [])

                for project in projects[:10]:
                    title = project.get("title", project.get("name", ""))
                    if title:
                        signals.append({
                            "timestamp": datetime.now(timezone.utc).isoformat(),
                            "source": "Green Climate Fund",
                            "title": title,
                            "amount_usd": project.get("funding_amount", project.get("amount", 0)),
                            "funding_type": project.get("type", "Grant"),
                            "url": project.get("url", LIVE_SOURCES["gcf"]["base_url"]),
                            "deadline": project.get("deadline", "See website"),
                            "eligibility": project.get("countries", ["Nigeria"]),
                            "focus_areas": project.get("sectors", ["Climate"]),
                            "relevance_score": 80,
                            "mode": "live",
                        })
            except json.JSONDecodeError:
                pass

    except requests.RequestException as e:
        print(f"Warning: Failed to fetch GCF data: {e}")

    return signals


def fetch_live_signals() -> list[dict]:
    """
    Fetch funding signals from all live sources.

    Returns:
        Combined list of funding signals from all sources
    """
    all_signals = []

    # Fetch World Bank projects
    wb_signals = fetch_world_bank_projects()
    all_signals.extend(wb_signals)

    # Fetch GCF projects
    gcf_signals = fetch_gcf_projects()
    all_signals.extend(gcf_signals)

    return all_signals


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
        # Live mode: fetch from real APIs
        if not REQUESTS_AVAILABLE:
            raise ImportError("requests library required for live mode. Run: pip install requests")

        signals = fetch_live_signals()

        if signals:
            persist_signals(signals, DATA_PATH)
            return signals
        else:
            # Fallback to mock if no live data retrieved
            print("Warning: No live funding signals retrieved, falling back to mock mode")
            return run(mock=True)

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
