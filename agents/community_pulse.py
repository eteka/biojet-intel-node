"""Community Pulse: monitors stakeholder sentiment and generates editorial content.

Tracks farmer/aggregator sentiment, local news, and generates editorial pieces
on the SAF industry in relation to developing countries.

Includes an Editor sub-agent that writes thought pieces on SAF opportunities
and challenges for developing nations, particularly in Africa.

Data Sources:
- AllAfrica Nigeria Agriculture: allafrica.com/nigeria/agriculture/
- Guardian Nigeria Agro-Care: guardian.ng/business-services/agro-care/
- Nairaland Forums Agriculture: nairaland.com/agriculture
"""
from __future__ import annotations

import argparse
import json
import random
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
    from data_sources import COMMUNITY_SOURCES
except ImportError:
    COMMUNITY_SOURCES = {}

DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "community_pulse.json"

# Live data source URLs
LIVE_SOURCES = {
    "allafrica": {
        "name": "AllAfrica Nigeria Agriculture",
        "rss_url": "https://allafrica.com/tools/headlines/rdf/nigeria/agriculture/headlines.rdf",
        "base_url": "https://allafrica.com/nigeria/agriculture/",
    },
    "guardian_ng": {
        "name": "Guardian Nigeria Agro-Care",
        "base_url": "https://guardian.ng/business-services/agro-care/",
    }
}

# Keywords for filtering relevant content
AGRICULTURE_KEYWORDS = [
    "cassava", "biofuel", "ethanol", "farmers", "feedstock",
    "agriculture", "crop", "harvest", "price", "cooperative",
    "processing", "waste", "biomass"
]

# Sentiment categories
SENTIMENT_LEVELS = ["Very Positive", "Positive", "Neutral", "Concerned", "Negative"]

# Mock community signals
MOCK_COMMUNITY_SIGNALS = [
    {
        "source": "Cassava Farmers Association of Nigeria",
        "signal_type": "Survey Result",
        "title": "80% of Cassava Farmers Open to Biomass Aggregation Schemes",
        "sentiment": "Very Positive",
        "region": "South-South Nigeria",
        "stakeholder_type": "Farmers",
        "key_insight": "Price guarantees and consistent offtake are primary motivators",
    },
    {
        "source": "Nigerian Tribune",
        "signal_type": "News Coverage",
        "title": "Oyo State Explores Cassava Waste-to-Fuel Initiative",
        "sentiment": "Positive",
        "region": "South-West Nigeria",
        "stakeholder_type": "Government",
        "key_insight": "State government showing interest in circular economy models",
    },
    {
        "source": "IITA Ibadan",
        "signal_type": "Research Publication",
        "title": "Study: Cassava Processing Residue Volumes Exceed Previous Estimates",
        "sentiment": "Positive",
        "region": "Nigeria National",
        "stakeholder_type": "Research",
        "key_insight": "Available feedstock may be 40% higher than current estimates",
    },
    {
        "source": "Aggregator Network WhatsApp Group",
        "signal_type": "Informal Signal",
        "title": "Logistics Costs Remain Primary Barrier for Rural Biomass Collection",
        "sentiment": "Concerned",
        "region": "North-Central Nigeria",
        "stakeholder_type": "Aggregators",
        "key_insight": "Transportation infrastructure gaps limiting collection efficiency",
    },
    {
        "source": "Premium Times",
        "signal_type": "News Coverage",
        "title": "Aviation Stakeholders Call for SAF Policy Framework in Nigeria",
        "sentiment": "Positive",
        "region": "Nigeria National",
        "stakeholder_type": "Industry",
        "key_insight": "Growing awareness of SAF opportunity among aviation sector",
    },
    {
        "source": "Rural Women Farmers Network",
        "signal_type": "Community Feedback",
        "title": "Women-Led Cooperatives Seek Training on Biomass Quality Standards",
        "sentiment": "Positive",
        "region": "South-East Nigeria",
        "stakeholder_type": "Farmers",
        "key_insight": "Strong interest but capacity building needed",
    },
]

# Editorial templates for the Editor sub-agent
EDITORIAL_TEMPLATES = [
    {
        "theme": "Opportunity",
        "title": "Why Africa Could Become the World's SAF Breadbasket",
        "hook": "As global aviation races to decarbonize, African nations hold an unexpected trump card: abundant agricultural residues that could fuel the jets of tomorrow.",
        "key_points": [
            "Africa produces over 200 million tonnes of cassava annually, with significant processing residues",
            "The continent's young population and agricultural base create a unique value chain opportunity",
            "Book-and-claim mechanisms allow African producers to supply global markets",
            "First-mover advantage could establish lasting market positions",
        ],
        "developing_country_angle": "Unlike industrialized nations competing with food production, developing countries can leverage existing agricultural waste streams—turning a disposal problem into an export opportunity.",
        "call_to_action": "The window for African nations to establish SAF production infrastructure is now. Those who move first will define the industry for decades.",
    },
    {
        "theme": "Challenge",
        "title": "The Infrastructure Gap: What's Really Holding Back African SAF",
        "hook": "Nigeria produces enough cassava waste to fuel every flight departing Lagos. So why isn't it happening yet?",
        "key_points": [
            "Collection logistics remain the primary bottleneck—not feedstock availability",
            "Inconsistent power supply raises production costs by 30-40%",
            "Limited access to project finance creates a chicken-and-egg problem",
            "Regulatory frameworks lag behind the technical possibilities",
        ],
        "developing_country_angle": "Developing nations face a classic infrastructure paradox: they need SAF plants to justify grid investments, but need reliable power to attract SAF investments. Breaking this cycle requires creative financing and phased development approaches.",
        "call_to_action": "Success will come to nations that address infrastructure holistically—not just building plants, but building the ecosystems around them.",
    },
    {
        "theme": "Policy",
        "title": "CORSIA and the Developing World: Opportunity or Burden?",
        "hook": "The global carbon offsetting scheme for aviation could either propel or sideline developing country participation in SAF markets.",
        "key_points": [
            "CORSIA creates guaranteed demand for certified sustainable fuels",
            "Certification costs may disadvantage smaller producers",
            "Developed country mandates (ReFuelEU, US SAF credits) drive immediate demand",
            "Africa remains largely absent from CORSIA eligible fuel production",
        ],
        "developing_country_angle": "While CORSIA was designed with environmental goals in mind, its implementation could inadvertently favor established players in wealthy nations. Developing countries must advocate for certification pathways that recognize their unique contexts.",
        "call_to_action": "African negotiators at ICAO must push for simplified certification for small-scale producers and recognition of developmental co-benefits.",
    },
    {
        "theme": "Innovation",
        "title": "Leapfrogging: Can Africa Skip Fossil Jet Fuel Entirely?",
        "hook": "Some African airports have never had reliable jet fuel supply. What if they go straight to SAF?",
        "key_points": [
            "Many regional African airports lack established fuel infrastructure",
            "Building SAF-ready facilities from scratch may be cheaper than retrofitting",
            "Distributed production models could serve underserved airports",
            "Mobile phone banking showed Africa can leapfrog traditional infrastructure",
        ],
        "developing_country_angle": "The absence of legacy infrastructure—often seen as a weakness—could become Africa's greatest strength in the SAF transition. Nations unencumbered by sunk costs in fossil fuel systems can design optimal SAF supply chains from the ground up.",
        "call_to_action": "Aviation authorities should consider SAF-first policies for new airport infrastructure rather than replicating 20th-century fossil fuel designs.",
    },
    {
        "theme": "Community",
        "title": "From Waste to Wings: How SAF Could Transform Rural African Livelihoods",
        "hook": "For millions of smallholder farmers, agricultural waste is a disposal headache. SAF could turn it into a steady income stream.",
        "key_points": [
            "Cassava processing generates 30-40% waste by weight",
            "Current disposal methods include burning or dumping—both problematic",
            "Biomass aggregation could add $200-500 annual income per farming household",
            "Women, who dominate cassava processing, stand to benefit disproportionately",
        ],
        "developing_country_angle": "SAF production in developing countries isn't just about fuel—it's about rural economic transformation. The value chain creates jobs in collection, processing, and logistics that can't be automated or offshored.",
        "call_to_action": "SAF project developers must design inclusive value chains that share benefits with farming communities—not just extract their resources.",
    },
]


def generate_mock_signals(count: int = 4) -> list[dict]:
    """Generate mock community signals."""
    selected = random.sample(MOCK_COMMUNITY_SIGNALS, min(count, len(MOCK_COMMUNITY_SIGNALS)))
    signals = []

    for signal in selected:
        days_ago = random.randint(0, 14)
        timestamp = datetime.now(timezone.utc) - timedelta(days=days_ago)

        signals.append({
            "timestamp": timestamp.isoformat(),
            "source": signal["source"],
            "signal_type": signal["signal_type"],
            "title": signal["title"],
            "sentiment": signal["sentiment"],
            "sentiment_score": SENTIMENT_LEVELS.index(signal["sentiment"]) * 25,  # 0-100 scale
            "region": signal["region"],
            "stakeholder_type": signal["stakeholder_type"],
            "key_insight": signal["key_insight"],
            "mode": "mock",
        })

    return signals


def generate_editorial() -> dict:
    """
    Editor Sub-Agent: Generate an editorial piece on SAF in developing countries.

    This simulates an AI editor that writes thought pieces on SAF opportunities
    and challenges specifically relevant to developing nations.
    """
    template = random.choice(EDITORIAL_TEMPLATES)
    timestamp = datetime.now(timezone.utc)

    # Generate word count estimate
    word_count = random.randint(800, 1200)

    editorial = {
        "timestamp": timestamp.isoformat(),
        "title": template["title"],
        "theme": template["theme"],
        "hook": template["hook"],
        "key_points": template["key_points"],
        "developing_country_angle": template["developing_country_angle"],
        "call_to_action": template["call_to_action"],
        "estimated_word_count": word_count,
        "target_audience": "SAF industry stakeholders, policymakers, investors",
        "geographic_focus": "Africa, with emphasis on West Africa",
        "author": "SAF HUB Editorial Desk",
        "status": "draft",
        "mode": "mock",
    }

    return editorial


def calculate_sentiment_summary(signals: list[dict]) -> dict:
    """Calculate overall sentiment summary from signals."""
    if not signals:
        return {"overall": "Neutral", "score": 50, "trend": "stable"}

    scores = [s.get("sentiment_score", 50) for s in signals]
    avg_score = sum(scores) / len(scores)

    if avg_score >= 75:
        overall = "Very Positive"
    elif avg_score >= 50:
        overall = "Positive"
    elif avg_score >= 25:
        overall = "Neutral"
    else:
        overall = "Concerned"

    return {
        "overall": overall,
        "score": round(avg_score),
        "signal_count": len(signals),
        "trend": random.choice(["improving", "stable", "declining"]),
    }


def load_existing_data(path: Path) -> dict:
    """Load existing data from file."""
    if path.exists():
        try:
            with path.open("r", encoding="utf-8") as handle:
                return json.load(handle)
        except json.JSONDecodeError:
            return {"signals": [], "editorials": [], "sentiment_summary": {}}
    return {"signals": [], "editorials": [], "sentiment_summary": {}}


def persist_data(new_data: dict, path: Path) -> None:
    """Persist data to file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    existing = load_existing_data(path)

    # Merge signals
    all_signals = existing.get("signals", []) + new_data.get("signals", [])
    all_signals = sorted(all_signals, key=lambda x: x["timestamp"], reverse=True)[:30]

    # Merge editorials (keep more history)
    all_editorials = existing.get("editorials", []) + new_data.get("editorials", [])
    all_editorials = sorted(all_editorials, key=lambda x: x["timestamp"], reverse=True)[:20]

    output = {
        "signals": all_signals,
        "editorials": all_editorials,
        "sentiment_summary": new_data.get("sentiment_summary", {}),
        "last_updated": datetime.now(timezone.utc).isoformat(),
    }

    with path.open("w", encoding="utf-8") as handle:
        json.dump(output, handle, ensure_ascii=False, indent=2)


def run(mock: bool = True) -> dict:
    """Run the community pulse agent with editor sub-agent."""
    if not mock:
        raise NotImplementedError("Live community monitoring is not implemented yet.")

    # Generate community signals
    count = random.randint(3, 5)
    signals = generate_mock_signals(count)

    # Generate editorial content (Editor sub-agent)
    editorial = generate_editorial()

    # Calculate sentiment summary
    sentiment = calculate_sentiment_summary(signals)

    data = {
        "signals": signals,
        "editorials": [editorial],
        "sentiment_summary": sentiment,
    }

    persist_data(data, DATA_PATH)

    return data


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(description="Community Pulse Agent with Editor")
    parser.add_argument(
        "--live",
        action="store_true",
        help="Attempt live monitoring (not implemented; defaults to mock).",
    )
    parser.add_argument(
        "--editorial-only",
        action="store_true",
        help="Generate only editorial content without community signals.",
    )
    return parser.parse_args()


def main() -> None:
    """Main entry point."""
    args = parse_args()
    result = run(mock=not args.live)
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
