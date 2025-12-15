#!/usr/bin/env python3
"""
Biojet Nigeria - Feedstock Watchdog Agent
Monitors cassava peel and biomass prices across Nigerian markets
"""

import json
import random
import datetime
from typing import Dict, List
from dataclasses import dataclass, asdict


@dataclass
class MarketPrice:
    """Represents a feedstock price observation"""
    market_name: str
    location: str
    price_per_tonne: float
    currency: str
    timestamp: str
    feedstock_type: str
    quality_grade: str
    availability: str  # "High", "Medium", "Low"


class FeedstockWatchdog:
    """Monitors feedstock prices across Nigerian markets"""

    # Nigerian markets for cassava processing
    MARKETS = [
        {"name": "Aba Market", "location": "Abia State"},
        {"name": "Bodija Market", "location": "Oyo State"},
        {"name": "Kuto Market", "location": "Ogun State"},
        {"name": "Wuse Market", "location": "FCT Abuja"},
        {"name": "Owerri Market", "location": "Imo State"},
        {"name": "Enugu Main Market", "location": "Enugu State"},
        {"name": "Warri Market", "location": "Delta State"},
        {"name": "Benin City Market", "location": "Edo State"},
        {"name": "Calabar Market", "location": "Cross River State"},
        {"name": "Kaduna Market", "location": "Kaduna State"},
        {"name": "Kano Sabon Gari", "location": "Kano State"},
        {"name": "Lafia Market", "location": "Nasarawa State"},
    ]

    FEEDSTOCK_TYPES = [
        "Cassava Peel",
        "Cassava Stem",
        "Mixed Agricultural Waste",
        "Palm Kernel Shell",
    ]

    def __init__(self, mock_mode: bool = True):
        """
        Initialize the Feedstock Watchdog

        Args:
            mock_mode: If True, generates synthetic data. If False, attempts real data collection.
        """
        self.mock_mode = mock_mode
        self.last_scan_time = None
        self.price_history = []

    def generate_mock_price(self, market: Dict[str, str], feedstock_type: str) -> MarketPrice:
        """Generate a realistic mock price observation"""

        # Base prices (in Naira per tonne) - realistic ranges
        base_prices = {
            "Cassava Peel": 18500,
            "Cassava Stem": 15000,
            "Mixed Agricultural Waste": 12000,
            "Palm Kernel Shell": 22000,
        }

        base_price = base_prices.get(feedstock_type, 15000)

        # Add realistic variation (+/- 15%)
        variation = random.uniform(-0.15, 0.15)
        price = base_price * (1 + variation)

        # Round to nearest 100
        price = round(price / 100) * 100

        # Determine availability based on region and season
        availability_choices = ["High", "Medium", "Low"]
        availability_weights = [0.5, 0.35, 0.15]  # Most markets have good availability
        availability = random.choices(availability_choices, weights=availability_weights)[0]

        # Quality grades
        quality_grades = ["Premium", "Standard", "Economy"]
        quality = random.choice(quality_grades)

        return MarketPrice(
            market_name=market["name"],
            location=market["location"],
            price_per_tonne=price,
            currency="NGN",
            timestamp=datetime.datetime.now().isoformat(),
            feedstock_type=feedstock_type,
            quality_grade=quality,
            availability=availability
        )

    def scan_markets(self) -> List[MarketPrice]:
        """
        Scan all markets for current feedstock prices

        Returns:
            List of MarketPrice observations
        """
        if self.mock_mode:
            return self._scan_markets_mock()
        else:
            return self._scan_markets_real()

    def _scan_markets_mock(self) -> List[MarketPrice]:
        """Generate mock market data"""
        observations = []

        for market in self.MARKETS:
            # Each market typically has 1-2 main feedstock types available
            num_feedstocks = random.randint(1, 2)
            available_feedstocks = random.sample(self.FEEDSTOCK_TYPES, num_feedstocks)

            for feedstock in available_feedstocks:
                observation = self.generate_mock_price(market, feedstock)
                observations.append(observation)

        self.last_scan_time = datetime.datetime.now()
        self.price_history.extend(observations)

        return observations

    def _scan_markets_real(self) -> List[MarketPrice]:
        """
        Scan real market data sources

        TODO: Implement real data collection from:
        - Agricultural commodity exchanges
        - Market surveys
        - Direct supplier networks
        - Government agricultural databases
        """
        print("⚠️  Real market scanning not yet implemented")
        print("   Falling back to mock mode...")
        return self._scan_markets_mock()

    def calculate_average_price(self, feedstock_type: str = "Cassava Peel") -> float:
        """Calculate the average price for a specific feedstock type"""
        if not self.price_history:
            return 0.0

        relevant_prices = [
            obs.price_per_tonne
            for obs in self.price_history
            if obs.feedstock_type == feedstock_type
        ]

        if not relevant_prices:
            return 0.0

        return sum(relevant_prices) / len(relevant_prices)

    def get_price_index(self) -> Dict:
        """Generate a price index summary"""
        cassava_avg = self.calculate_average_price("Cassava Peel")

        return {
            "feedstock_type": "Cassava Peel",
            "average_price": round(cassava_avg, 2),
            "currency": "NGN",
            "unit": "per tonne",
            "period": "7-day average",
            "last_updated": datetime.datetime.now().isoformat(),
            "markets_surveyed": len(self.MARKETS),
            "total_observations": len(self.price_history)
        }

    def export_to_json(self, filename: str = "feedstock_data.json") -> None:
        """Export price observations to JSON file"""
        data = {
            "metadata": {
                "agent": "Feedstock Watchdog",
                "mode": "mock" if self.mock_mode else "live",
                "last_scan": self.last_scan_time.isoformat() if self.last_scan_time else None,
            },
            "price_index": self.get_price_index(),
            "observations": [asdict(obs) for obs in self.price_history]
        }

        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"✅ Data exported to {filename}")

    def print_summary(self) -> None:
        """Print a summary of current market conditions"""
        print("\n" + "="*60)
        print("🌾 BIOJET NIGERIA - FEEDSTOCK WATCHDOG REPORT")
        print("="*60)

        if not self.price_history:
            print("No data available. Run scan_markets() first.")
            return

        price_index = self.get_price_index()

        print(f"\n📊 PRICE INDEX SUMMARY")
        print(f"   Feedstock: {price_index['feedstock_type']}")
        print(f"   Average Price: ₦{price_index['average_price']:,.2f} {price_index['unit']}")
        print(f"   Period: {price_index['period']}")
        print(f"   Markets Surveyed: {price_index['markets_surveyed']}")
        print(f"   Total Observations: {price_index['total_observations']}")

        print(f"\n📍 MARKET BREAKDOWN (Recent Scan)")
        recent_obs = self.price_history[-12:]  # Last 12 observations

        for obs in recent_obs:
            availability_icon = {
                "High": "🟢",
                "Medium": "🟡",
                "Low": "🔴"
            }.get(obs.availability, "⚪")

            print(f"   {availability_icon} {obs.market_name:20s} | ₦{obs.price_per_tonne:>8,.0f} | {obs.feedstock_type}")

        print("\n" + "="*60)
        print(f"Mode: {'🔧 MOCK DATA' if self.mock_mode else '🌐 LIVE DATA'}")
        print(f"Last Scan: {self.last_scan_time.strftime('%Y-%m-%d %H:%M:%S') if self.last_scan_time else 'Never'}")
        print("="*60 + "\n")


def main():
    """Main execution function"""
    print("\n🚀 Initializing Feedstock Watchdog Agent...")

    # Initialize in mock mode
    watchdog = FeedstockWatchdog(mock_mode=True)

    print("📡 Scanning markets...")
    observations = watchdog.scan_markets()
    print(f"✅ Collected {len(observations)} price observations")

    # Print summary
    watchdog.print_summary()

    # Export data
    watchdog.export_to_json("feedstock_data.json")

    print("\n💡 TIP: To use real data mode, set mock_mode=False")
    print("   (requires implementation of data source connectors)\n")


if __name__ == "__main__":
    main()
