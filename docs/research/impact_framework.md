# Impact framework: "why it matters" reasoning reference (T0.7)

Researched 2026-10-14 by the `researcher` agent. Web-search summaries were used (pages were not all fetched in full).
Labels: **[S]** = URL appeared in a search result that supported the claim; **[H]** = company homepage URL given from
general knowledge, not fetched this session (use only as an identifier); **unverified** = single or secondary source.
Direction convention in the playbook: the arrow is the direction of the *underlying variable* (e.g. `competition: up` =
competition intensifies; `valuation: down` = marks fall). Claude decides whether that is good or bad for GenZero.

Reasoning chain per news item: (1) what happened, (2) GenZero exposure (direct holding / fund LP / enabler / none),
(3) what usually follows this event type, (4) which concerns move and which way, (5) final lines (so what, watch-for, timeframe).

---

## 1. Investor concern checklist (11)

Grounding: valuation concerns follow IPEV fair-value practice (price of recent investment, multiples, calibration; recent
round prices should not be assumed to stay fair value indefinitely) [S] https://www.houlihancapital.com/2025-ipev-valuation-guidelines/ ,
https://central.cvca.ca/financial-compliance-and-reporting/navigating-ipev-valuation-guidelines-key-concepts-and-practical-insights/ .
ILPA guidance was not fetched; it is cited as a general LP reporting reference only (https://ilpa.org, unverified for specifics).
Market-level context: PitchBook Q1 2026 climate VC deal value US$14.3bn, highest since Q3 2023 [S]
https://pitchbook.brightspotcdn.com/e4/da/43dcc46e45b981a943163aaff6b0/q1-2026-climate-tech-vc-trends-preview.pdf ;
Currence (formerly Sightline Climate) H1 2026 climate VC US$26.1bn, +55% y/y, 34% to low-carbon data-centre tech [S]
https://www.esgtoday.com/climate-tech-funding-surges-in-h1-2026-on-growing-data-center-demand-for-low-carbon-power-report/ ;
climate dry powder US$90bn at Q1 2026 vs US$112bn peak [S] https://www.ctvc.co/new-the-2026-climate-dry-powder-new-funds-report/ .

| id | Concern | Definition | Question for Claude |
|---|---|---|---|
| valuation | Valuation and comparable marks | Fair value of holdings and fund NAVs, driven by recent round prices and peer multiples | How does this change the mark or the comparable set for a GenZero holding or LP fund? |
| capital | Follow-on capital and dilution | Availability, price and terms of next rounds, dry powder, risk of down rounds | How does this change the odds or terms of the next round for the affected holding? |
| exit | Exit routes | M&A, IPO, secondary and strategic-buyer appetite and multiples | How does this change who could buy or list the holding, and at what multiple? |
| demand | Revenue, demand and offtake | Contracted and expected buyers, offtake size, buyer concentration | How does this change contracted or likely demand for the holding's product or credits? |
| economics | Unit economics, cost curve, tech risk | Cost per unit vs price, learning curve, technology readiness | How does this change cost per tonne/litre/kWh or technical risk? |
| carbon_price | Carbon credit price and supply | Spot/forward prices by credit type, supply-demand balance (CORSIA, compliance links) | How does this change price or supply for the credit types GenZero holds or trades? |
| integrity | Integrity, counterparty, reputational and ESG risk | Credit quality, ratings, fraud, greenwashing exposure of GenZero or its partners | Could this damage credit quality, a partner, or GenZero's reputation (cf. C-Quest exit)? |
| policy | Policy and regulatory exposure | Subsidies, tax credits, Article 6, CORSIA, mandates (ReFuelEU), carbon taxes | How does this change the subsidy, mandate or market-access rules affecting the holding? |
| competition | Competitive position | Peer strength, funding, share of buyers, consolidation | Does this strengthen or weaken the holding's position against named peers? |
| pipeline | Deal pipeline and co-investment | New deal flow, co-investors, valuation entry points, fund-manager access | Does this open or close an investable deal, entry price or co-investor? |
| execution | Project execution | Delays, capex overruns, permitting, grid or feedstock access, financing close | Does this change timing, capex or delivery risk on a project or plant? |

---

## 2. Event-type playbook (11 event types)

Typical timeframes are practitioner judgement unless a precedent supports them.

### 2.1 peer_fundraise: peer or competitor large raise
- Next: (1st) peer extends runway, hires, wins offtakes; read-across validates the sector and lifts comps. (2nd) competition for deals and talent rises; follow-on investors anchor on the new price. Weeks to 6 months.
- Moves: valuation up, capital up, competition up, exit mixed.
- Precedents: Twelve US$645m total incl. US$400m project equity led by TPG Rise [S] https://www.esgdive.com/news/american-airlines-completes-first-commercial-flight-with-esaf-infinium/827270/ (SAF page also in [S] https://www.cbinsights.com/esp/industrials/aerospace-tech/sustainable-aviation-fuels-(saf)-%26-e-fuels-producers); Climate VC H1 2026 rebound [S] https://www.esgtoday.com/climate-tech-funding-surges-in-h1-2026-on-growing-data-center-demand-for-low-carbon-power-report/ .

### 2.2 distress: down round, insolvency, layoffs
- Next: (1st) markdowns on the company and listed or private comps; lenders and offtakers reassess. (2nd) investors become selective on capital-heavy models; assets sold cheaply; talent spills out. 1 to 12 months.
- Moves: valuation down, capital down, exit down, pipeline up (cheaper entry), competition mixed (survivors gain).
- Precedents: Northvolt bankruptcy, c. EUR10bn raised; PitchBook showed European battery investment falling and some investors reluctant to fund new entrants, while others called it an anomaly [S] https://sifted.eu/articles/northvolt-bankrupt-vc-reaction-ev-battery , https://morningstar.co.uk/uk/news/257712/vw-and-goldman-sachs-exposed-to-northvolt-collapse.aspx . Climeworks cut 106 staff (22%) in May 2025 citing US policy retreat and market conditions [S] https://www.swissinfo.ch/eng/climeworks-is-cutting-22%25-of-staff-as-us-climate-backlash-hits-carbon-removal/89379470 . Fulcrum BioEnergy Chapter 11, Sept 2024 (over US$500m raised, more than US$456m obligations) [S] https://www.argusmedia.com/en/news-and-insights/latest-market-news/2608211-fulcrum-bioenergy-files-for-chapter-11-relief .

### 2.3 fund_close: competitor investor or fund-of-interest closes a fund
- Next: (1st) signals LP appetite, more dry powder for same deal types. (2nd) bidding for deals tightens entry prices; a GenZero fund manager closing is a positive read for NAV and follow-on reserves. Deployment over 12 to 36 months.
- Moves: capital up, competition up, pipeline mixed (more co-investors, higher prices), valuation up (slight).
- Precedents: Brookfield BGTF II US$20bn final close, Oct 2025 [S] https://bam.brookfield.com/press-releases/brookfield-raises-20-billion-record-transition-fund ; TPG Rise Climate Fund I US$7.3bn [S] https://impactalpha.com/tpg-seals-its-rise-climate-fund-at-7-3-billion/ ; climate dry powder falling from US$112bn to US$90bn [S] https://www.ctvc.co/new-the-2026-climate-dry-powder-new-funds-report/ .

### 2.4 exit: M&A, IPO or strategic acquisition in the sector
- Next: (1st) sets a multiple and proves a buyer universe; comps repriced. (2nd) consolidation pressures sub-scale peers; strategic acquirers (data/index providers, exchanges, majors) show appetite. 0 to 12 months.
- Moves: exit up, valuation up, competition up (consolidation), pipeline mixed.
- Precedents: MSCI acquiring Trove Research (Oct 2023), a data provider moving into carbon-credit analytics [S] https://esgnews.com/msci-to-advance-clarity-in-carbon-markets-with-acquisition-of-trove-research ; CIX and Carbonplace merger announced Aug 2026, GenZero holds CIX [S] https://esgtoday.com/environmental-carbon-markets-platforms-climate-impact-x-carbonplace-to-merge/ .

### 2.5 policy_support: subsidy, mandate or market rule introduced
- Next: (1st) demand visibility improves for the affected tech or credit type; announced projects reach FID. (2nd) capital flows in, peers raise, input costs rise. 3 to 24 months (rules need implementation).
- Moves: policy up, demand up, carbon_price up (if credits linked), capital up, economics up, competition up.
- Precedents: CORSIA Phase 1 eligible supply vs demand: Sylvera June 2026 counts about 38M eligible issued credits against about 163M potential demand, scenario prices US$15 to 53 [S] https://info.sylvera.com/hubfs/CORSIA-Countdown-Report_Sylvera-June2026.pdf?hsLang=en ; CORSIA-eligible credits sold at US$21.70 in an auction [S] https://carbon-pulse.com/360825/?site=cpp .

### 2.6 policy_rollback: subsidy cut, rule delay or political reversal
- Next: (1st) project economics and tax-equity assumptions break; marks fall for exposed assets; layoffs and delays. (2nd) capital rotates to other geographies or tech; non-US/EU jurisdictions gain relative appeal. 0 to 12 months; sharp for tax-credit-dependent sectors.
- Moves: policy down, demand down, valuation down, capital down, execution down (delays), pipeline mixed (distress buys).
- Precedents: US One Big Beautiful Bill Act, July 2025: 45V construction start deadline pulled to end-2027, wind/solar placed-in-service cut-off, FEOC limits, 45Q parity changes [S] https://www.cliffordchance.com/briefings/2025/07/one-big-beautiful-bill-act--updates-to-section-45q-tax-credits-f.html , https://3degreesinc.com/insights/what-you-need-to-know-about-the-one-big-beautiful-bill-and-your-climate-action-plans/ ; H1 2025 climate funding down 19% per CTVC [S] https://trellis.net/article/trumps-big-beautiful-bill-climate-tech-investment/ .

### 2.7 integrity_event: carbon-market integrity scandal, rating or standard decision
- Next: (1st) prices of affected credit types drop within days to weeks; buyers pause or shift to renewable or CCP-labelled credits. (2nd) rating and MRV providers see demand; developers face issuance suspensions and leadership changes; standards tighten. 1 to 18 months.
- Moves: integrity down, carbon_price down (affected types), demand mixed (shift to high-quality), competition mixed (ratings and MRV up).
- Precedents: Jan 2023 Guardian REDD+ investigation: REDD+ prices fell from US$3.05-6.80 to US$2.25-5.00 range in weeks; nature-based avoidance down 66% to US$2.70 by early 2024 [S] https://carbon-pulse.com/234197/ , https://www.spglobal.com/energy/en/news-research/latest-news/energy-transition/022224-credits-from-katingan-project-hold-the-fort-in-a-bearish-redd-market ; Kariba suspension, South Pole CEO exit Nov 2023 [S] https://carbon-pulse.com/235499/ , https://www.swissinfo.ch/eng/ceo-of-swiss-carbon-offset-firm-south-pole-resigns/48969692 ; ICVCM CCP label premium up to about 25% (ICVCM/analyst claim) [S] https://icvcm.org/core-carbon-principles-at-the-heart-of-market-transformation-report/ .

### 2.8 big_offtake: large corporate offtake or credit purchase
- Next: (1st) validates the credit or fuel type and sets a price benchmark; supplier raises or scales. (2nd) concentration risk if one buyer dominates; copycat buyers follow. 0 to 12 months.
- Moves: demand up, carbon_price up, valuation up, capital up, competition up; buyer-concentration risk up.
- Precedents: Microsoft took about 90% of 2025 durable CDR volume; Fastmarkets: about 91% of H1 2025 long-term removal agreements (56.3 Mt) [S] https://www.fastmarkets.com/insights/cdr-offtakes-reach-61-5-mln-tco2e-tech-giants-drive-demand/ ; Microsoft's pause exposes thin demand [S] https://www.fastmarkets.com/insights/microsoft-pause-in-carbon-removal-buying-exposes-lack-of-depth-in-demand-analysis/ ; Q1 2026 CDR.fyi: 2.3 Mt contracted, biochar 93% of volume [S] https://decarbonfuse.com/posts/carbon-removal-posts-record-q1-in-2026-driven-by-biochar-and-big-buyers . GenZero's own Amazon 680k+ t rice-methane agreement (see portfolio.md).

### 2.9 project_delay: project cancellation, delay or impairment
- Next: (1st) impairment and guidance cut; offtakers and lenders reassess; share or credit price reaction. (2nd) rights issue or asset sales, rating downgrades, supply-chain contagion; cheaper assets for patient buyers. 0 to 12 months.
- Moves: execution down, valuation down, capital down, demand mixed, pipeline up (distressed entry).
- Precedents: Orsted halted Hornsea 4 (2.4 GW), Sunrise Wind divestment halted, DKK60bn rights issue, shares -24%, S&P cut to BBB- [S] https://www.windtech-international.com/company-news/orsted-outlines-rights-issue-and-reports-h1-2025-results , https://www.offshore-mag.com/special-reports/news/55310667/orsteds-shares-downgraded-to-near-junk-status ; UK NorthPoint SAF facility uncertain after Fulcrum bankruptcy [S] https://fastmarkets.com/insights/uks-northpoint-saf-facility-uncertain-as-project-developer-files-for-bankruptcy .

### 2.10 tech_cost: technology breakthrough or cost decline
- Next: (1st) incumbent technologies face margin pressure; new entrants raise. (2nd) offtake prices reset lower; policy support may shift; learning-curve narratives spread. 6 to 36 months.
- Moves: economics up (adopter) or down (displaced), competition up, valuation mixed, carbon_price down (cheaper abatement substitutes), demand up.
- Precedents: Biochar cost and volume dominance in durable CDR (Q1 2026) [S] https://biochartoday.com/news/cdr-fyi-and-microsoft-demonstrate-biochar-dominance-in-record-breaking-q1-2026-market-report/ ; Puro biochar CORC prices stable US$125-145 in 2025 [S] https://puro.earth/our-blog/346-biochars-market-leadership-in-carbon-removal . Further precedent not searched: unverified.

### 2.11 fraud_scandal: partner or portfolio-adjacent fraud, enforcement or litigation
- Next: (1st) immediate write-down or exit; counterparties pause. (2nd) due diligence tightens market-wide; ratings and MRV demand rises. 0 to 6 months.
- Moves: integrity down, valuation down, demand down (affected type), competition mixed.
- Precedents: C-Quest Capital: GenZero exited after the former head was indicted for fraud [S] https://www.eco-business.com/news/genzero-nears-halfway-mark-to-climate-goal-exits-scandal-hit-cookstove-projects/ ; South Pole Kariba (above).

Gaps: no precedent URL verified for a climate-IPO repricing or for Article 6.4 first issuances; add later if needed.

---

## 3. Sector peers watchlist

Peer selection is researcher judgement. URLs are company homepages [H] unless a source is marked [S].
Only direct investments and enablers are listed (funds excluded, per brief).

| Portfolio company | Peers (URL) | Basis |
|---|---|---|
| Aurora Sustainable Lands | Chestnut Carbon (chestnutcarbon.com), Finite Carbon (finitecarbon.com), Mombak (mombak.com), Pachama (pachama.com) | [H] IFM and reforestation removal developers |
| Rize | Agreena (agreena.com), Indigo Ag (indigoag.com), Regrow (regrow.ag) | [H] ag-carbon and rice methane |
| Carbo Culture | Charm Industrial (charmindustrial.com), Exomad Green (exomadgreen.com), Airex Energy (airex-energy.com), Oregon Biochar Solutions | [H]; Airex and Oregon Biochar named in a market-report summary [S] https://businesswire.com/news/home/20250814477045/en/Biochar-Market-Report-2026-2036-with-Profiles-of-148-Companies-Driving-Market-Development-Including-Established-Producers-Emerging-Technology-Innovators-and-Integrated-Carbon-Removal-Specialists---ResearchAndMarkets.com ; biochar sector [S] https://puro.earth/our-blog/346-biochars-market-leadership-in-carbon-removal |
| CycloKinetics | LanzaJet (lanzajet.com), Gevo (gevo.com), Twelve (twelve.co), Infinium (infiniumtechnologies.ai) | [S] https://www.safinvestor.com/sponsor/lanzajet ; https://www.esgdive.com/news/american-airlines-completes-first-commercial-flight-with-esaf-infinium/827270/ |
| Velocys | Infinium, Twelve, LanzaJet, Fulcrum BioEnergy (bankrupt, a cautionary peer) | [S] https://www.argusmedia.com/en/news-and-insights/latest-market-news/2608211-fulcrum-bioenergy-files-for-chapter-11-relief |
| Newlight Technologies | Mango Materials (mangomaterials.com), Danimer Scientific (danimerscientific.com), Origin Materials (originmaterials.com), CJ Biomaterials | [H] biopolymer and PHA peers |
| PCG Global | Sembcorp (sembcorp.com), Vena Energy (venaenergy.com), Sunseap/Sun Cable-type developers, Equis (equis.com) | [H] SEA/Oceania solar and storage platforms |
| Terra CO2 | Brimstone (brimstone.com), Sublime Systems (sublime-systems.com), Fortera (fortera.com), Solidia | [S] funding aggregator data https://www.caplight.com/company/fortera , https://impactalpha.com/sublime-systems-secures-40-million-to-commercialize-electrified-zero-carbon-cement |
| BeZero Carbon | Sylvera (sylvera.com), Calyx Global (calyxglobal.com; check current ownership), Renoster (renoster.io), MSCI Carbon Markets | [S] https://carbonmarketwatch.org/publications/assessing-and-comparing-carbon-credit-rating-agencies/ ; https://esgnews.com/msci-to-advance-clarity-in-carbon-markets-with-acquisition-of-trove-research |
| Chooose | Normative (normative.io), Watershed (watershed.com), Sweep (sweep.net), Persefoni (persefoni.com) | [H] climate and carbon accounting software |
| Climate Impact X | Xpansiv (xpansiv.com), AirCarbon Exchange (aircarbon.co), Carbonplace (carbonplace.com; merging with CIX), Senken (senken.io) | [S] https://esgtoday.com/environmental-carbon-markets-platforms-climate-impact-x-carbonplace-to-merge/ ; https://www.cbinsights.com/company/thallo/alternatives-competitors |
| South Pole | Climate Impact Partners (climateimpact.com), ClimeCo (climeco.com), Everland (everland.earth), Wildlife Works (wildlifeworks.com) | [H]; South Pole context [S] https://carbon-pulse.com/235499/ |
| Perennial | Regrow (regrow.ag), Indigo Ag, Agreena, Nori-style soil MRV: unverified | [H] soil-carbon MRV |
| AJA Climate Solutions | Wildlife Works, Everland, Carbon Streaming-type developers: unverified | [H] nature carbon project developers |

Programme partners (Brujula Verde, Imperative, Good Rice Alliance) are not given peers (project-level, not companies).
Not verified: AirCarbon Exchange status (search returned nothing), Calyx Global current ownership, Pegasus (no result).

---

## 4. Ready-to-paste YAML

```yaml
impact_framework:
  direction_note: "arrow = direction of the underlying variable (competition up = intensifies); judge good/bad for GenZero yourself"
  chain: "what happened > GenZero exposure (direct/fund LP/enabler/none) > what usually follows > metrics moved with direction > final lines (so what, watch-for, timeframe)"
  concerns:
    - {id: valuation, name: Valuation and comparable marks, question: "How does this change the mark or comparable set for a GenZero holding or LP fund?"}
    - {id: capital, name: Follow-on capital and dilution, question: "How does this change the odds or terms of the next round for the affected holding?"}
    - {id: exit, name: Exit routes, question: "How does this change who could buy or list the holding, and at what multiple?"}
    - {id: demand, name: Revenue, demand and offtake, question: "How does this change contracted or likely demand for the holding's product or credits?"}
    - {id: economics, name: Unit economics and technology risk, question: "How does this change cost per unit or technical risk?"}
    - {id: carbon_price, name: Carbon credit price and supply, question: "How does this change price or supply for credit types GenZero holds or trades?"}
    - {id: integrity, name: Integrity, counterparty, reputational and ESG risk, question: "Could this damage credit quality, a partner or GenZero's reputation?"}
    - {id: policy, name: Policy and regulatory exposure, question: "How does this change subsidy, mandate or market-access rules for the holding?"}
    - {id: competition, name: Competitive position, question: "Does this strengthen or weaken the holding against named peers?"}
    - {id: pipeline, name: Deal pipeline and co-investment, question: "Does this open or close an investable deal, entry price or co-investor?"}
    - {id: execution, name: Project execution, question: "Does this change timing, capex or delivery risk on a project or plant?"}
  playbook:
    - {event_type: peer_fundraise, typical_effects: "Peer gets runway and validates sector, comps lift; then deal and talent competition and anchored round prices. Weeks to 6 months.", metrics: {valuation: up, capital: up, competition: up, exit: mixed}, precedents: ["Twelve US$645m incl. TPG Rise-led project equity", "H1 2026 climate VC +55% (Currence)"]}
    - {event_type: distress, typical_effects: "Markdowns on company and comps, lenders and offtakers reassess; then selectivity against capex-heavy models, cheap asset sales, talent spill. 1 to 12 months.", metrics: {valuation: down, capital: down, exit: down, pipeline: up, competition: mixed}, precedents: ["Northvolt bankruptcy 2024-25", "Climeworks cut 22% staff May 2025", "Fulcrum Chapter 11 Sept 2024"]}
    - {event_type: fund_close, typical_effects: "Signals LP appetite and dry powder; then tighter entry prices; a GenZero fund manager closing helps NAV and reserves. Deployment 12 to 36 months.", metrics: {capital: up, competition: up, pipeline: mixed, valuation: up}, precedents: ["Brookfield BGTF II US$20bn Oct 2025", "TPG Rise Climate US$7.3bn"]}
    - {event_type: exit_ma_ipo, typical_effects: "Sets multiple and shows buyer universe, comps repriced; then consolidation pressure on sub-scale peers. 0 to 12 months.", metrics: {exit: up, valuation: up, competition: up, pipeline: mixed}, precedents: ["MSCI buys Trove Research 2023", "CIX-Carbonplace merger Aug 2026"]}
    - {event_type: policy_support, typical_effects: "Demand visibility improves, projects reach FID; then capital inflow, peers raise, input costs rise. 3 to 24 months.", metrics: {policy: up, demand: up, carbon_price: up, capital: up, economics: up, competition: up}, precedents: ["CORSIA Phase 1 eligible supply 38M vs demand ~163M (Sylvera Jun 2026)", "CORSIA credits US$21.70 auction"]}
    - {event_type: policy_rollback, typical_effects: "Project economics and tax-equity break, marks fall, layoffs and delays; then capital rotates to other geographies and tech. 0 to 12 months.", metrics: {policy: down, demand: down, valuation: down, capital: down, execution: down, pipeline: mixed}, precedents: ["US OBBBA July 2025 (45V, 48E/45Y, FEOC)", "H1 2025 climate funding -19% (CTVC)"]}
    - {event_type: integrity_event, typical_effects: "Prices of affected credit types fall in days to weeks, buyers shift to CCP-labelled or renewables credits; then issuance suspensions, leadership changes, tighter standards, ratings and MRV demand. 1 to 18 months.", metrics: {integrity: down, carbon_price: down, demand: mixed, competition: mixed}, precedents: ["Guardian REDD+ Jan 2023: REDD+ prices down, nature avoidance -66% by 2024", "Kariba suspension, South Pole CEO exit Nov 2023", "ICVCM CCP premium up to ~25%"]}
    - {event_type: big_offtake, typical_effects: "Validates credit or fuel type and sets price benchmark, supplier scales; then buyer concentration risk and copycat buyers. 0 to 12 months.", metrics: {demand: up, carbon_price: up, valuation: up, capital: up, competition: up}, precedents: ["Microsoft ~90% of 2025 durable CDR volume", "Microsoft buying pause exposes thin demand (Fastmarkets)", "GenZero-linked Amazon 680k t rice methane"]}
    - {event_type: project_delay, typical_effects: "Impairment, guidance cut, lenders and offtakers reassess; then rights issues, asset sales, downgrades, distressed entry for patient buyers. 0 to 12 months.", metrics: {execution: down, valuation: down, capital: down, demand: mixed, pipeline: up}, precedents: ["Orsted Hornsea 4 halt, DKK60bn rights issue, shares -24%, S&P BBB- (2025)", "UK NorthPoint SAF uncertain after Fulcrum"]}
    - {event_type: tech_cost, typical_effects: "Incumbent margins squeezed, new entrants raise; then offtake prices reset, learning-curve narratives spread. 6 to 36 months.", metrics: {economics: mixed, competition: up, valuation: mixed, carbon_price: down, demand: up}, precedents: ["Biochar 93% of Q1 2026 durable CDR volume", "Puro biochar CORC US$125-145 in 2025"]}
    - {event_type: fraud_scandal, typical_effects: "Immediate write-down or exit, counterparties pause; then market-wide due diligence tightening and ratings and MRV demand. 0 to 6 months.", metrics: {integrity: down, valuation: down, demand: down, competition: mixed}, precedents: ["C-Quest Capital exit by GenZero", "South Pole Kariba 2023"]}
sector_peers:
  - {portfolio_company: Aurora Sustainable Lands, peers: [Chestnut Carbon, Finite Carbon, Mombak, Pachama]}
  - {portfolio_company: Rize, peers: [Agreena, Indigo Ag, Regrow]}
  - {portfolio_company: Carbo Culture, peers: [Charm Industrial, Exomad Green, Airex Energy, Oregon Biochar Solutions]}
  - {portfolio_company: CycloKinetics, peers: [LanzaJet, Gevo, Twelve, Infinium]}
  - {portfolio_company: Velocys, peers: [Infinium, Twelve, LanzaJet, Fulcrum BioEnergy]}
  - {portfolio_company: Newlight Technologies, peers: [Mango Materials, Danimer Scientific, Origin Materials]}
  - {portfolio_company: PCG Global, peers: [Sembcorp, Vena Energy, Equis]}
  - {portfolio_company: Terra CO2, peers: [Brimstone, Sublime Systems, Fortera, Solidia]}
  - {portfolio_company: BeZero Carbon, peers: [Sylvera, Calyx Global, Renoster, MSCI Carbon Markets]}
  - {portfolio_company: Chooose, peers: [Normative, Watershed, Sweep, Persefoni]}
  - {portfolio_company: Climate Impact X, peers: [Xpansiv, AirCarbon Exchange, Carbonplace, Senken]}
  - {portfolio_company: South Pole, peers: [Climate Impact Partners, ClimeCo, Everland, Wildlife Works]}
  - {portfolio_company: Perennial, peers: [Regrow, Indigo Ag, Agreena]}
  - {portfolio_company: AJA Climate Solutions, peers: [Wildlife Works, Everland]}
```
