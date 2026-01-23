# CLAUDE.md - Project Intelligence for Claude Code

## Project Overview

**SAF HUB** - West Africa's Sustainable Aviation Fuel (SAF) Market Intelligence Platform by Biojet Nigeria Limited. Aggregates real-time market intelligence on SAF opportunities across Nigeria and West Africa through six specialized intelligence agents.

**Focus Areas:** Cassava-based SAF production, ICAO CORSIA/EASA compliance, funding pipelines, technology benchmarking (HEFA, ETJ, AtJ, FT pathways), airline offtake agreements, and community sentiment.

## Tech Stack

| Layer | Technology |
|-------|------------|
| Frontend | Vanilla HTML5/JS, Tailwind CSS 3 (CDN) |
| Backend/Agents | Python 3.x |
| Data Storage | JSON files in `data/` |
| CI/CD | GitHub Actions (daily at 08:00 UTC) |
| Deployment | Static HTML (no build step) |

## Project Structure

```
biojet-intel-node/
├── agents/                      # Python intelligence agents
│   ├── feedstock_watchdog.py   # Cassava peel price monitoring
│   ├── regulatory_sentry.py    # ICAO/EASA/NCAA alerts
│   ├── capital_signals.py      # Funding opportunities
│   ├── technology_diligence.py # SAF pathway economics
│   ├── market_access.py        # Airline offtake signals
│   └── community_pulse.py      # Sentiment + editorial content
├── data/                        # JSON data persistence
│   ├── prices.json
│   ├── regulatory_alerts.json
│   ├── capital_signals.json
│   ├── technology_updates.json
│   ├── market_signals.json
│   └── community_pulse.json
├── index.html                   # Single-page dashboard
├── requirements.txt             # Python dependencies
└── .github/workflows/
    └── daily_scrape.yml        # Automated daily runs
```

## Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run agents (mock mode - default)
python agents/feedstock_watchdog.py
python agents/regulatory_sentry.py
python agents/capital_signals.py
python agents/technology_diligence.py
python agents/market_access.py
python agents/community_pulse.py

# Run agents (live mode - not yet implemented)
python agents/feedstock_watchdog.py --live

# Frontend - just open in browser
# No build step required
```

## Agent Architecture Pattern

All agents follow this identical structure:

```python
def generate_mock_data() -> list[dict]:
    """Create sample data with realistic variation"""

def load_existing_data() -> list[dict]:
    """Read from JSON file, return empty list if missing"""

def persist_data(records: list[dict]) -> None:
    """Write to JSON, limit to 30-50 records, sort by timestamp desc"""

def run(mock: bool = True) -> dict:
    """Main execution - raises NotImplementedError if mock=False"""

def parse_args():
    """CLI argument handling with --live flag"""

def main():
    """Entry point, prints JSON to stdout"""
```

## Code Conventions

### Python (Agents)
- **Naming:** snake_case for functions/variables, noun_verb for agent files
- **Timestamps:** ISO 8601 format with timezone (`datetime.now(timezone.utc).isoformat()`)
- **Mode field:** Every record includes `"mode": "mock"` or `"mode": "live"`
- **Record limits:** Keep 30-50 records max per JSON file to prevent bloat
- **Output:** Agents print JSON to stdout for pipeline compatibility

### JavaScript (Frontend)
- **No framework** - vanilla JS with async/await fetch
- **Demo toggle:** Stored in `localStorage.getItem('isDemoMode')`
- **Error handling:** Try/catch with user-friendly fallback messages
- **Data filtering:** Filter by mode field based on demo toggle state

### HTML/CSS
- **Styling:** Tailwind utility classes exclusively
- **Custom effects:** `.glass` class for glassmorphism UI
- **IDs:** kebab-case describing content area
- **Responsive:** Mobile-first grid layouts

## Data Model Examples

```json
// prices.json
{
  "timestamp": "2025-01-22T08:00:00.000000+00:00",
  "commodity": "cassava_peel",
  "currency": "NGN",
  "price_per_tonne": 23280,
  "mode": "mock"
}

// capital_signals.json
{
  "timestamp": "2025-01-22T...",
  "source": "Green Climate Fund",
  "title": "GCF Readiness Support",
  "amount_usd": 2500000,
  "funding_type": "Grant",
  "deadline": "2025-06-30",
  "eligibility": ["Nigeria", "Ghana"],
  "relevance_score": 85,
  "mode": "mock"
}
```

## Key Constants

| Constant | Value | Context |
|----------|-------|---------|
| Cassava price range | ₦15,000-₦25,000/tonne | Feedstock |
| Funding range | $750K-$50M | Capital signals |
| HEFA cost | $3.50-$5.00/gal | Technology |
| ETJ cost | $4.00-$6.50/gal | Technology |
| AtJ cost | $4.50-$7.00/gal | Technology |
| FT cost | $5.00-$8.00/gal | Technology |
| Co-processing | $2.50-$4.00/gal | Technology |
| Sentiment range | 0-100 | Community pulse |
| Relevance scores | 60-99 | All agents |

## Common Tasks

### Adding a new agent
1. Create `agents/new_agent.py` following the architecture pattern above
2. Add corresponding `data/new_agent.json` (or let agent create it)
3. Add agent to `.github/workflows/daily_scrape.yml`
4. Add frontend section in `index.html` with data loading

### Modifying mock data
- Edit `MOCK_*` constants at top of each agent file
- Re-run agent to regenerate: `python agents/<agent>.py`

### Testing frontend changes
- Open `index.html` directly in browser
- Toggle demo/live mode via UI switch
- Check browser console for fetch errors

## Architecture Decisions

1. **File-based JSON over database** - Simplicity for MVP, git-trackable data
2. **Mock-first design** - All agents work offline, live mode is additive
3. **No build step** - Reduces complexity, CDN for Tailwind
4. **Single HTML file** - Easy deployment, no routing complexity
5. **GitHub Actions for automation** - Free, reliable, git-integrated

## Gotchas & Warnings

- **Live mode not implemented** - All `--live` flags raise `NotImplementedError`
- **No environment variables** - All config is hardcoded (intentional for MVP)
- **JSON file size** - Agents auto-trim to prevent unbounded growth
- **Tailwind via CDN** - Requires internet for styling (no offline CSS)
- **localStorage dependency** - Demo toggle won't persist in private browsing

## Future Implementation Notes

When implementing live mode:
- Add rate limiting for external APIs
- Implement retry logic with exponential backoff
- Add proxy support for protected feeds
- Consider caching layer to reduce redundant scraping
- Add data validation before persistence

## External Data Sources (Planned)

| Agent | Sources |
|-------|---------|
| Feedstock | FEWS NET, Nigerian commodity exchanges |
| Regulatory | ICAO RSS, EASA database, NCAA updates |
| Capital | GCF, AfDB, EU Global Gateway, IFC/World Bank |
| Technology | ASTM D7566, Neste, LanzaJet, GREET model |
| Market | Airline press releases, IATA pledges, SkyNRG |
| Community | Agricultural associations, social media, local news |
