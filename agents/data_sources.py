"""
SAF Market Intelligence - Data Sources Configuration

Centralized configuration for all external data sources used by intelligence agents.
Each source includes URL, access method, update frequency, and implementation notes.

Reference: docs/DATA_SOURCES.md
"""

# =============================================================================
# 1. FEEDSTOCK PRICING DATA SOURCES
# =============================================================================

FEEDSTOCK_SOURCES = {
    "wfp_hdx": {
        "name": "WFP Nigeria Food Price Dataset",
        "base_url": "https://data.humdata.org/dataset/wfp-food-prices-for-nigeria",
        "api_url": "https://data.humdata.org/api/3/action/package_show?id=wfp-food-prices-for-nigeria",
        "format": "CSV/JSON",
        "frequency": "monthly",
        "access": "public",
        "reliability": "high",
        "auth_required": False,
        "notes": "Filter for cassava/garri items. Peels not tracked separately."
    },
    "nbs_food_prices": {
        "name": "NBS Selected Food Price Watch",
        "base_url": "https://nigeria.opendataforafrica.org/gjskat/selected-food-prices-watch",
        "api_url": "https://nigeria.opendataforafrica.org/api/1.0/data",
        "format": "JSON/SDMX",
        "frequency": "monthly",
        "access": "public",
        "reliability": "high",
        "auth_required": False,
        "notes": "Official NBS data. Tracks garri, yam, grains. No residues."
    },
    "fews_net": {
        "name": "FEWS NET Nigeria Price Bulletins",
        "base_url": "https://fews.net/west-africa/nigeria/price-bulletin",
        "api_url": None,  # PDF only, requires scraping
        "format": "PDF",
        "frequency": "monthly",
        "access": "public",
        "reliability": "medium",
        "auth_required": False,
        "notes": "PDF bulletins with price graphs. Parse charts for data."
    },
    "afex": {
        "name": "AFEX Commodities Exchange (XIP Portal)",
        "base_url": "https://xip.afex.africa",
        "api_url": None,  # Proprietary, subscription required
        "format": "proprietary",
        "frequency": "daily",
        "access": "paid",
        "reliability": "high",
        "auth_required": True,
        "subscription_cost": "NGN 1,500,000/year",
        "notes": "Leading Nigerian commodities exchange. Grains, possibly cassava chips."
    },
    "ncx": {
        "name": "Nigerian Commodity Exchange",
        "base_url": "https://ncx.com.ng",
        "api_url": None,
        "format": "HTML",
        "frequency": "daily",
        "access": "registration",
        "reliability": "medium",
        "auth_required": True,
        "notes": "Government-backed. 9 crops in 12 states. Less active than AFEX."
    },
    "fao_fpma": {
        "name": "FAO Food Price Monitoring & Analysis",
        "base_url": "https://www.fao.org/giews/food-prices/home/en/",
        "api_url": "https://fpma.fao.org/giews/fpmat4/#/dashboard/tool/domestic",
        "format": "JSON/CSV",
        "frequency": "monthly",
        "access": "public",
        "reliability": "high",
        "auth_required": False,
        "notes": "International price comparisons. Occasional Nigeria data."
    }
}

# =============================================================================
# 2. REGULATORY & POLICY UPDATE SOURCES
# =============================================================================

REGULATORY_SOURCES = {
    "icao_newsroom": {
        "name": "ICAO Environmental News",
        "base_url": "https://www.icao.int/newsroom",
        "rss_url": "https://www.icao.int/newsroom/Pages/default.aspx",  # Check for RSS
        "format": "HTML/RSS",
        "frequency": "ad-hoc",
        "access": "public",
        "reliability": "high",
        "keywords": ["SAF", "CORSIA", "sustainable aviation fuel", "emissions"],
        "notes": "Official source for global aviation policy."
    },
    "icao_corsia": {
        "name": "ICAO CORSIA Updates",
        "base_url": "https://www.icao.int/CORSIA",
        "eligible_fuels_url": "https://www.icao.int/CORSIA/corsia-certified-fuels",
        "ccr_url": "https://www.icao.int/CORSIA/CCR",
        "format": "HTML/PDF",
        "frequency": "annual",
        "access": "public",
        "reliability": "high",
        "notes": "CORSIA eligible fuels list, certified producers, LCA data."
    },
    "easa_newsroom": {
        "name": "EASA Newsroom & ReFuelEU",
        "base_url": "https://www.easa.europa.eu/en/newsroom",
        "rss_url": "https://www.easa.europa.eu/en/rss",
        "format": "HTML/RSS/PDF",
        "frequency": "regular",
        "access": "public",
        "reliability": "high",
        "keywords": ["SAF", "sustainable aviation", "ReFuelEU"],
        "notes": "EU aviation safety. ReFuelEU mandate reports."
    },
    "ncaa_nigeria": {
        "name": "NCAA Nigeria Press Releases",
        "base_url": "https://ncaa.gov.ng/media/news/",
        "rss_url": None,  # No RSS - scraping required
        "format": "HTML/PDF",
        "frequency": "moderate",
        "access": "public",
        "reliability": "high",
        "keywords": ["emissions", "CORSIA", "biofuel", "environment"],
        "notes": "No RSS feed. Requires periodic scraping."
    },
    "afcac": {
        "name": "African Civil Aviation Commission",
        "base_url": "https://afcac.org",
        "format": "HTML/PDF",
        "frequency": "low",
        "access": "public",
        "reliability": "medium",
        "notes": "Regional policy updates. Often via press releases."
    },
    "iata_sustainability": {
        "name": "IATA Sustainability Updates",
        "base_url": "https://www.iata.org/pressroom",
        "newsletter_url": "https://www.iata.org/en/publications/newsletters/sustainability-economics-insights/",
        "rss_url": "https://www.iata.org/en/pressroom/",  # Check for RSS
        "format": "HTML/RSS",
        "frequency": "moderate",
        "access": "public",
        "reliability": "high",
        "notes": "Industry body. RSS for Sustainability & Economics insights."
    }
}

# =============================================================================
# 3. CAPITAL & FUNDING SIGNAL SOURCES
# =============================================================================

CAPITAL_SOURCES = {
    "gcf": {
        "name": "Green Climate Fund - Project Database",
        "base_url": "https://data.greenclimate.fund",
        "api_url": "https://data.greenclimate.fund/public/api/",
        "format": "JSON/CSV/Excel",
        "frequency": "real-time",
        "access": "public",
        "reliability": "high",
        "auth_required": False,
        "filter_params": {
            "country": "Nigeria",
            "sector": ["energy", "agriculture"],
            "keywords": ["biofuel", "bioenergy", "SAF"]
        },
        "notes": "UN climate finance. Filter by Nigeria/West Africa and energy sector."
    },
    "afdb": {
        "name": "African Development Bank - Projects",
        "base_url": "https://projects.afdb.org",
        "data_portal": "https://dataportal.opendataforafrica.org/ujcqcqf/african-development-bank-projects",
        "api_url": "https://dataportal.opendataforafrica.org/api/1.0/data",
        "format": "JSON/XML/CSV",
        "frequency": "regular",
        "access": "public",
        "reliability": "high",
        "auth_required": False,
        "filter_params": {
            "country": "1000140",  # Nigeria code
            "keywords": ["biofuel", "ethanol", "renewable energy"]
        },
        "notes": "Continental DFI. Also check MapAfrica for geocoded data."
    },
    "world_bank": {
        "name": "World Bank Climate Finance & Projects",
        "api_url": "https://api.worldbank.org/v2/projects",
        "format": "JSON/XML",
        "frequency": "real-time",
        "access": "public",
        "reliability": "high",
        "auth_required": False,
        "filter_params": {
            "country": "NG",  # Nigeria
            "theme": "climate",
            "sector": "energy"
        },
        "notes": "No API key needed. Filter by country=Nigeria, theme=climate."
    },
    "ifc": {
        "name": "IFC Project Disclosures",
        "base_url": "https://disclosures.ifc.org/",
        "format": "HTML",
        "frequency": "real-time",
        "access": "public",
        "reliability": "high",
        "keywords": ["Nigeria", "biofuel", "bioenergy"],
        "notes": "World Bank private sector arm. Scrape for Nigeria + biofuel."
    },
    "usaid_power_africa": {
        "name": "USAID Power Africa",
        "base_url": "https://www.usaid.gov/power-africa",
        "format": "HTML",
        "frequency": "ad-hoc",
        "access": "public",
        "reliability": "medium",
        "notes": "Filter RSS for Nigeria and grant keywords."
    },
    "eu_global_gateway": {
        "name": "EU Global Gateway Africa",
        "base_url": "https://europa.eu/rapid",
        "format": "HTML",
        "frequency": "periodic",
        "access": "public",
        "reliability": "medium",
        "notes": "Filter by Africa for funding announcements."
    }
}

# =============================================================================
# 4. TECHNOLOGY & PATHWAY ECONOMICS SOURCES
# =============================================================================

TECHNOLOGY_SOURCES = {
    "icao_corsia_fuels": {
        "name": "ICAO CORSIA Eligible Fuels & LCA Data",
        "base_url": "https://www.icao.int/CORSIA",
        "eligible_fuels_url": "https://www.icao.int/CORSIA/corsia-certified-fuels",
        "lca_doc_url": "https://www.icao.int/environmental-protection/CORSIA/Documents/",
        "format": "PDF",
        "frequency": "annual",
        "access": "public",
        "reliability": "high",
        "notes": "Default life-cycle emission values (gCO2/MJ) per pathway."
    },
    "rsb_certification": {
        "name": "RSB Certification Database",
        "base_url": "https://rsb.org/certification/rsb-certificates/",
        "format": "HTML table",
        "frequency": "real-time",
        "access": "public",
        "reliability": "high",
        "notes": "ICAO-recognized certifier. Scrape for African producers."
    },
    "iscc_certification": {
        "name": "ISCC Certification Database",
        "base_url": "https://www.iscc-system.org/certificates/all-certificates/",
        "format": "HTML/Excel",
        "frequency": "real-time",
        "access": "public",
        "reliability": "high",
        "notes": "Another major SAF certifier. Check for Africa entries."
    },
    "nrel_atb": {
        "name": "NREL Annual Technology Baseline",
        "base_url": "https://atb.nrel.gov",
        "data_url": "https://atb.nrel.gov/transportation/2023/data",
        "format": "CSV/Excel",
        "frequency": "annual",
        "access": "public",
        "reliability": "high",
        "notes": "Benchmark costs and efficiencies for biofuel pathways."
    },
    "greet_model": {
        "name": "Argonne GREET Model",
        "base_url": "https://greet.anl.gov/",
        "format": "Software/Excel",
        "frequency": "annual",
        "access": "public",
        "reliability": "high",
        "notes": "Run LCA scenarios for specific feedstock pathways."
    },
    "caafi": {
        "name": "CAAFI (Commercial Aviation Alternative Fuels Initiative)",
        "base_url": "https://www.caafi.org/",
        "format": "HTML",
        "frequency": "ad-hoc",
        "access": "public",
        "reliability": "high",
        "notes": "ASTM pathway approval announcements."
    }
}

# =============================================================================
# 5. MARKET ACCESS & OFFTAKE DATA SOURCES
# =============================================================================

MARKET_SOURCES = {
    "greenair_news": {
        "name": "GreenAir News - SAF Section",
        "base_url": "https://www.greenairnews.com",
        "saf_url": "https://www.greenairnews.com/?cat=sustainable-aviation-fuels",
        "rss_url": "https://www.greenairnews.com/feed/",
        "format": "HTML/RSS",
        "frequency": "weekly",
        "access": "public",
        "reliability": "medium-high",
        "keywords": ["SAF", "offtake", "airline", "agreement"],
        "notes": "Multiple SAF stories weekly. Good for deal announcements."
    },
    "advanced_biofuels_usa": {
        "name": "Advanced Biofuels USA",
        "base_url": "https://advancedbiofuelsusa.info",
        "format": "HTML",
        "frequency": "daily",
        "access": "public",
        "reliability": "medium-high",
        "notes": "Curated daily news links. SAF category available."
    },
    "iata_saf": {
        "name": "IATA SAF Resources",
        "base_url": "https://www.iata.org/en/programs/sustainability/sustainable-aviation-fuels/",
        "format": "HTML/PDF",
        "frequency": "periodic",
        "access": "public",
        "reliability": "high",
        "notes": "Aggregate SAF statistics, commitments data."
    },
    "airlines": {
        "name": "Airline Press Releases (Aggregated)",
        "sources": {
            "ethiopian": "https://www.ethiopianairlines.com/aa/news",
            "kenya_airways": "https://www.kenya-airways.com/global/en/about-us/news/",
            "air_peace": "https://www.flyairpeace.com/news/",
            "klm": "https://news.klm.com/",
            "emirates": "https://www.emirates.com/media-centre/",
            "delta": "https://news.delta.com/"
        },
        "format": "HTML",
        "frequency": "regular",
        "access": "public",
        "reliability": "high",
        "keywords": ["SAF", "sustainable", "biofuel", "carbon"],
        "notes": "Monitor for SAF usage and commitment announcements."
    },
    "atag": {
        "name": "Air Transport Action Group",
        "base_url": "https://www.atag.org/",
        "format": "HTML/PDF",
        "frequency": "biennial",
        "access": "public",
        "reliability": "high",
        "notes": "Aviation Benefits reports with SAF uptake stats."
    }
}

# =============================================================================
# 6. COMMUNITY & SENTIMENT DATA SOURCES
# =============================================================================

COMMUNITY_SOURCES = {
    "allafrica": {
        "name": "AllAfrica Nigeria Agriculture News",
        "base_url": "https://allafrica.com/nigeria/agriculture/",
        "rss_url": "https://allafrica.com/tools/headlines/rdf/nigeria/agriculture/headlines.rdf",
        "format": "HTML/RSS",
        "frequency": "daily",
        "access": "public",
        "reliability": "medium",
        "keywords": ["cassava", "biofuel", "ethanol", "farmers", "feedstock"],
        "notes": "~600 stories/day. Filter for relevant keywords."
    },
    "guardian_nigeria": {
        "name": "The Guardian Nigeria - Agriculture",
        "base_url": "https://guardian.ng/business-services/agro-care/",
        "format": "HTML",
        "frequency": "daily",
        "access": "public",
        "reliability": "medium",
        "notes": "Local coverage of farmer issues, prices."
    },
    "nairaland": {
        "name": "Nairaland Forums - Agriculture",
        "base_url": "https://www.nairaland.com/agriculture",
        "format": "HTML forum",
        "frequency": "daily",
        "access": "public",
        "reliability": "medium-low",
        "notes": "Grassroots opinions. Threads on commodity prices."
    },
    "twitter_x": {
        "name": "Twitter/X Monitoring",
        "api_url": "https://api.twitter.com/2/",  # Paid API
        "format": "JSON",
        "frequency": "real-time",
        "access": "paid",
        "reliability": "varies",
        "keywords": ["#cassava", "garri price", "biofuel", "SAF Nigeria"],
        "notes": "Official API is paid. Alternatives: snscrape, Nitter."
    },
    "naerls": {
        "name": "NAERLS Weekly Price Bulletin",
        "base_url": "https://naerls.gov.ng/tag/weekly-commodity-prices/",
        "format": "PDF/Word",
        "frequency": "weekly (historical)",
        "access": "restricted",
        "reliability": "high",
        "notes": "Partnership needed. Field officer data."
    },
    "google_trends": {
        "name": "Google Trends Nigeria",
        "base_url": "https://trends.google.com/trends/explore",
        "format": "JSON/CSV",
        "frequency": "real-time",
        "access": "public",
        "reliability": "medium",
        "keywords": ["cassava price", "fuel price", "garri"],
        "notes": "Proxy for public interest/concern."
    }
}

# =============================================================================
# COMBINED SOURCES DICTIONARY
# =============================================================================

ALL_SOURCES = {
    "feedstock": FEEDSTOCK_SOURCES,
    "regulatory": REGULATORY_SOURCES,
    "capital": CAPITAL_SOURCES,
    "technology": TECHNOLOGY_SOURCES,
    "market": MARKET_SOURCES,
    "community": COMMUNITY_SOURCES
}

# =============================================================================
# HELPER FUNCTIONS
# =============================================================================

def get_sources_by_category(category: str) -> dict:
    """Get all sources for a specific category."""
    return ALL_SOURCES.get(category, {})

def get_free_api_sources() -> dict:
    """Get all sources with free public APIs."""
    free_sources = {}
    for category, sources in ALL_SOURCES.items():
        for key, source in sources.items():
            if source.get("api_url") and source.get("access") == "public":
                if category not in free_sources:
                    free_sources[category] = {}
                free_sources[category][key] = source
    return free_sources

def get_rss_sources() -> dict:
    """Get all sources with RSS feeds available."""
    rss_sources = {}
    for category, sources in ALL_SOURCES.items():
        for key, source in sources.items():
            if source.get("rss_url"):
                if category not in rss_sources:
                    rss_sources[category] = {}
                rss_sources[category][key] = source
    return rss_sources


if __name__ == "__main__":
    # Print summary of available sources
    print("=" * 60)
    print("SAF MARKET INTELLIGENCE - DATA SOURCES SUMMARY")
    print("=" * 60)

    for category, sources in ALL_SOURCES.items():
        print(f"\n{category.upper()} ({len(sources)} sources)")
        print("-" * 40)
        for key, source in sources.items():
            access = source.get("access", "unknown")
            api = "API" if source.get("api_url") else "RSS" if source.get("rss_url") else "Web"
            print(f"  - {source['name']}: {access} ({api})")

    print("\n" + "=" * 60)
    print("FREE API SOURCES:")
    print("=" * 60)
    free = get_free_api_sources()
    for category, sources in free.items():
        for key, source in sources.items():
            print(f"  [{category}] {source['name']}")
            print(f"    URL: {source['api_url']}")
