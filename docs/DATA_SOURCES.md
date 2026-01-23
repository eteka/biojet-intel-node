# SAF Market Intelligence Data Sources for West Africa (Nigeria Focus)

Reference document for live data sources across the six intelligence categories.

---

## 1. Feedstock Pricing Data Sources

### WFP Nigeria Food Price Dataset (HDX)
- **URL:** https://data.humdata.org/dataset/wfp-food-prices-for-nigeria
- **Format:** CSV, JSON via HDX API
- **Frequency:** Monthly (2002-present)
- **Access:** Public, no auth required
- **Reliability:** HIGH
- **Coverage:** Maize, rice, garri (cassava), etc.
- **Note:** Cassava peel/pulp NOT separately tracked - data gap

### NBS Selected Food Price Watch
- **URL:** https://nigeria.opendataforafrica.org/gjskat/selected-food-prices-watch
- **Format:** CSV/XLS, JSON API, SDMX
- **Frequency:** Monthly (mid-month releases)
- **Access:** Public, open portal
- **Reliability:** HIGH (official NBS data)
- **Coverage:** Garri, yam, grains - NOT residues like cassava peels

### FEWS NET Nigeria Price Bulletins
- **URL:** https://fews.net/west-africa/nigeria/price-bulletin/
- **Format:** PDF bulletins with price graphs
- **Frequency:** Monthly
- **Access:** Public (no API, scraping/manual needed)
- **Reliability:** MEDIUM (aggregated graphs, not raw data)

### AFEX Commodities Exchange (XIP Portal)
- **URL:** https://xip.afex.africa
- **Format:** Proprietary platform, CSV/XLS downloads
- **Frequency:** Daily
- **Access:** PAID (₦1.5M/year subscription)
- **Reliability:** HIGH
- **Coverage:** Grains, possibly cassava chips

### Nigerian Commodity Exchange (NCX)
- **URL:** https://ncx.com.ng
- **Format:** HTML ticker, internal API
- **Frequency:** Daily
- **Access:** Registration required
- **Reliability:** MEDIUM (less active than AFEX)
- **Coverage:** 9 crops in 12 states

### Other Sources
- **FAO FPMA:** International price comparisons
- **Tridge / Index Mundi:** Commodity aggregators (signup required)

### Data Gap: Feedstock Residues
Cassava peels, sugarcane bagasse, palm kernel shells lack official feeds.
**Partnership opportunities:**
- IITA/CGIAR cassava peel utilization projects
- NAERLS/ADPs field price bulletins
- Local farmer cooperatives via WhatsApp

---

## 2. Regulatory & Policy Update Sources

### ICAO Environmental News & CORSIA
- **URL:** https://www.icao.int/newsroom | https://www.icao.int/CORSIA
- **Format:** HTML news, PDFs
- **Frequency:** Ad-hoc (around major events)
- **Access:** Public, RSS feed available
- **Reliability:** HIGH

### EASA Newsroom & ReFuelEU Updates
- **URL:** https://www.easa.europa.eu/en/newsroom
- **RSS:** https://www.easa.europa.eu/en/rss
- **Format:** HTML, PDF reports
- **Frequency:** Regular
- **Access:** Public
- **Reliability:** HIGH

### NCAA Nigeria Press Releases
- **URL:** https://ncaa.gov.ng/media/news/
- **Format:** HTML articles, occasional PDFs
- **Frequency:** Moderate
- **Access:** Public (NO RSS - scraping required)
- **Reliability:** HIGH

### AFCAC & Regional Bodies
- **URL:** https://afcac.org
- **Format:** HTML news, PDF communiqués
- **Frequency:** Low
- **Access:** Public
- **Reliability:** MEDIUM

### IATA Sustainability Updates
- **URL:** https://www.iata.org/pressroom
- **Newsletter:** https://www.iata.org/en/publications/newsletters/sustainability-economics-insights/
- **Format:** Press releases, newsletter
- **Frequency:** Moderate
- **Access:** Public, RSS available
- **Reliability:** HIGH

---

## 3. Capital & Funding Signal Sources

### Green Climate Fund - Project Database
- **URL:** https://data.greenclimate.fund
- **API:** Yes, JSON queries supported
- **Format:** Interactive DB with CSV/Excel export
- **Frequency:** Real-time (after board meetings)
- **Access:** Public
- **Reliability:** HIGH

### African Development Bank - Projects
- **URL:** https://projects.afdb.org
- **Data Portal:** https://dataportal.opendataforafrica.org/ujcqcqf/african-development-bank-projects
- **API:** Yes (JSON, XML)
- **Format:** Structured project database
- **Frequency:** Regular
- **Access:** Public
- **Reliability:** HIGH

### World Bank Climate Finance & Projects
- **URL:** https://api.worldbank.org/v2/projects
- **API:** Yes (JSON/XML, no key needed)
- **Format:** Project metadata with amounts
- **Frequency:** Real-time
- **Access:** Public
- **Reliability:** HIGH

### DFI Feeds (USAID, EU, etc.)
- **USAID Power Africa:** https://www.usaid.gov/power-africa
- **EU Global Gateway:** https://europa.eu/rapid (filter by Africa)
- **Format:** HTML news, PDFs
- **Access:** Public (scattered sources)

### Climate Finance Trackers
- **CPI Global Landscape:** Annual reports + Excel data
- **ODI Climate Funds Update:** Online database
- **Format:** Reports, data files
- **Frequency:** Annual

---

## 4. Technology & Pathway Economics Sources

### ASTM D7566 Fuel Annex Updates
- **Source:** ASTM International, CAAFI, FAA
- **Format:** PDF standards, press releases
- **Frequency:** Infrequent (new pathways every few years)
- **Access:** Paid for standards, announcements public
- **Reliability:** HIGH

### ICAO CORSIA Eligible Fuels & LCA Data
- **URL:** https://www.icao.int/CORSIA
- **Documents:** https://www.icao.int/CORSIA/corsia-certified-fuels
- **Format:** PDFs with emission values
- **Frequency:** Periodic (annual updates)
- **Access:** Public
- **Reliability:** HIGH

### RSB Certification Database
- **URL:** https://rsb.org/certification/rsb-certificates/
- **Format:** Web table (searchable)
- **Frequency:** Real-time (new certs added)
- **Access:** Public (scrapeable)
- **Reliability:** HIGH

### NREL GREET & ATB
- **GREET:** Argonne National Lab downloadable model
- **ATB:** https://atb.nrel.gov (Annual Technology Baseline)
- **Format:** Software, CSV, graphs
- **Frequency:** Annual
- **Access:** Public
- **Reliability:** HIGH

### SAF Production Trackers
- **IATA SAF Report:** https://www.iata.org/en/programs/sustainability/sustainable-aviation-fuels/
- **GreenAir News SAF Section:** https://www.greenairnews.com (RSS available)
- **ATAG Publications:** Biennial reports

---

## 5. Market Access & Offtake Sources

### Airline Press Releases
- **Coverage:** Air Peace, Ethiopian, Kenya Airways, KLM, Emirates, Delta
- **Format:** HTML news, PDF sustainability reports
- **Frequency:** Regular news, annual reports
- **Access:** Public, many have RSS

### GreenAir News
- **URL:** https://www.greenairnews.com
- **Format:** News articles (RSS available)
- **Frequency:** Weekly (multiple SAF stories)
- **Reliability:** MEDIUM-HIGH

### Advanced Biofuels USA
- **URL:** https://advancedbiofuelsusa.info
- **Format:** Curated daily news links
- **Frequency:** Daily
- **Access:** Public

### IATA & ATAG Dashboards
- **Format:** Aggregated figures in reports
- **Frequency:** Occasional (conferences)
- **Access:** Public (derived stats)

---

## 6. Community & Sentiment Sources

### AllAfrica Nigeria Agriculture News
- **URL:** https://allafrica.com/nigeria/agriculture/
- **RSS:** https://allafrica.com/tools/headlines/rdf/nigeria/agriculture/headlines.rdf
- **Format:** Aggregated news articles
- **Frequency:** Daily (~600 stories/day across all topics)
- **Access:** Public
- **Reliability:** MEDIUM

### Twitter/X Monitoring
- **API:** Mostly paid now (alternatives: snscrape)
- **Keywords:** #cassava, "garri price", "biofuel"
- **Note:** Include Yoruba/Hausa/Pidgin terms

### Nairaland Forums
- **URL:** https://www.nairaland.com (agriculture section)
- **Format:** Forum posts (scraping required)
- **Frequency:** Daily
- **Access:** Public
- **Reliability:** MEDIUM-LOW (anecdotal)

### NAERLS Extension Reports
- **URL:** https://naerls.gov.ng (historical bulletins)
- **Format:** PDF/Word reports
- **Frequency:** Weekly (if revived)
- **Access:** Restricted (partnership needed)
- **Reliability:** HIGH

---

## Data Gaps Summary

| Category | Gap | Mitigation |
|----------|-----|------------|
| Feedstock | Cassava peel, bagasse, PKS prices | Partner with IITA, NAERLS |
| Regulatory | African-specific SAF policy | Monitor AFCAC, national gazettes |
| Capital | No unified "SAF in Africa" fund DB | Aggregate multiple DFI sources |
| Technology | Real-time production volumes | Use certifications as proxy |
| Market | African airline offtake deals | Monitor international carriers to Africa |
| Sentiment | Rural farmer voice | Partner with NGOs, use Google Trends |

---

## Partnership Opportunities

1. **IITA/CGIAR** - Cassava value chain price data
2. **NAERLS/ADPs** - Grassroots market price bulletins
3. **AFRAA** - African airline SAF survey data
4. **Universities** - Covenant, Ilorin, Bayero Kano (KasuwaGo project)
5. **Private Sector** - Nestlé Nigeria, Nigerian Breweries biomass data
6. **Climate Finance Accelerator Nigeria** - Pipeline project info
