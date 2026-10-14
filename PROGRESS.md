# PROGRESS — single source of truth (update after EVERY task)

## Current state
WORKING MODEL COMPLETE and verified by the main session (2026-10-14):
`python run.py` → 8/8 sources, ~120 in-window items, all graded by the importance matrix in 3 parallel batches,
top 7 analysed (Q1–Q5 chain), 126 s, 1 A4 page (Edge PDF). Checks passed: page order = importance order; max item age 6 days;
code importance matches weights for all rows; full triage audit in output/items_DATE.json. README and PLAN updated for 8 sources.

## Next step
1. T3.2: user reads output/newsletter_2026-10-14.html. Open user calls: (a) matrix weights: wind setbacks with exposure 2 still
   reach the page through materiality + downside, and competitor stories rank highly through exposure 4; (b) min_score_to_show (30).
2. T3.3: talking points "how it works / where it fails" (PLAN §8 + matrix + watchlist chunking).
3. Optional v2: full-text fetch for top items (D3-B), verify [H] peer URLs, reduce run-to-run score variance (e.g. grade twice and average).

## Open decisions (do not implement anything that depends on these)
- [x] D1 Sources: Google News funding + negative queries, TechCrunch Climate, CTVC, Carbon Brief, Eco-Business
- [x] D2 One batched Claude call (+1 retry, keyword fallback)
- [x] D3 RSS title + summary only
- [x] D4 Local `enhance-prompt` skill (ECC not installed)
- [x] D6 Exited/non-investment partners → partners_watch tier (shown as "partner of GenZero")
- [x] D5 Step-1 answers = the user additions embedded in the Step-2 brief (competitor/sector fundraises, +/- news with negative priority, LLM relevance vs portfolio & competitors, local Claude Code, 2–4 lines per item). Captured in REQUIREMENTS.md.

## Phases and tasks
### Phase 0: Planning
- [x] T0.1 Environment check (Python 3.12.10; Claude CLI 2.1.299 bundled in VS Code ext, not on PATH; ECC not installed)
- [x] T0.2 Project rules (CLAUDE.md), agents (.claude/agents/), PROGRESS.md
- [x] T0.3 Source research (researcher agent, live-tested feeds)
- [x] T0.4 PLAN.md with architecture, diagrams, trade-offs
- [x] T0.5 User resolves D1–D5; write REQUIREMENTS.md (≤10 lines)
- [x] T0.6 Researcher: GenZero portfolio, competitors, keywords → docs/research/portfolio.md (with source URLs)
- [x] T0.7 Researcher: investor concern checklist + event playbook + sector peers → docs/research/impact_framework.md (done; peer URLs partly unverified [H])
- [x] T0.8 PLAN rev 2 (impact engine §5, fixed item format, plain list layout) + REQUIREMENTS update

### Phase 1: Walking skeleton (no LLM)
- [x] T1.1 `config.yaml` (sources, portfolio, competitors, limits) + `requirements.txt`
- [x] T1.2 `fetch.py`: RSS/API → normalised items, last 7 days, per-source fail-soft
- [x] T1.3 Dedupe + keyword pre-filter + cap (~60 items)
- [x] T1.4 `render.py` + `template.html`: one-page A4 HTML from items
- [x] T1.5 `run.py --no-llm` produces an HTML file end to end

### Phase 2: LLM analysis (investor-impact engine, PLAN.md §5)
- [x] T2.0 Merge impact_framework.md YAML (impact_framework, sector_peers) into config.yaml; fuzzy dedupe; case-sensitive entity names
- [x] T2.1 `llm.py`: resolve claude binary, headless call helper (`-p --output-format json --json-schema`), timeout, 1 retry
- [x] T2.2 Stage A triage (1 batched call): event_type, entities+tier, relevance, sentiment, duplicate_of; `prompts/triage.md`
- [x] T2.3 Rank in code → top 7 (relevance + negative bonus + direct-link bonus)
- [x] T2.4 Stage B impact (1 call per item, ≤4 parallel): Q1–Q5 reasoning fields → What / GenZero link / Impact; `prompts/impact.md` with impact framework pre-prompt, plain-English and no-filler rules
- [x] T2.5 Fallbacks (triage fail → keyword list; item fail → quick take) + full `python run.py`; check one-page fit

- [x] T2.6 Relevance tuning: tighter funding query + money-amount filter, explicit triage rubric (focus sectors), min relevance 3, negative bonus only if relevant, variety cap, save full triage to JSON (done: funding 31→8 clean items, Singapore/Helix/1KOMMA5 now picked)
- [x] T2.7 Watchlist Google News queries (portfolio+partners; peers+competitor investors) built from config, rubric: focus-sector 4 needs company-level event, 'other' exempt from variety cap, same-company dedupe (done: 3/7 items now direct portfolio hits; found Google News ignores when:7d with ≥14 OR terms → 4 terms per query)
- [~] T2.8 Page-mix quotas: CANCELLED by user (no slot reservations or caps on competitor news)
- [x] T2.9 Weighted importance matrix (config scoring_matrix, 6 criteria, code recomputes 0-100, top scorers shown, min_score_to_show 30); strict 7-day window, no --days, drop undated (done; 152s, 1 page)
- [x] T2.10 Grade EVERY in-window item: remove keyword pre-cut to 60, parallel triage batches of 40, cross-batch dedupe, drop non-English (done; 120 graded in 3 batches, exclude_sources for social posts added by engineer)

### Phase 4: Hand-over
- [x] T4.1 API-key LLM backends (providers.py, .env/.env.example, anthropic + openai SDKs). 20 tests pass; non-CLI paths verified by mocks only (Ollama test cancelled by user). Full CLI run re-verified by main session.
- [x] T4.2 README updated for fuss-free setup (key in .env → python run.py)
- [ ] T4.3 Publish to GitHub: public repo Benjamin-Fernandez/genzero-climate-newsletter (sample newsletter committed; .env and audit JSON ignored)

### Phase 3: Deliverables
- [x] T3.1 README.md (≤5 lines: run, sources used, rejected + why, limitations)
- [ ] T3.2 Generate this week's newsletter; human review of the output
- [ ] T3.3 Prepare "how it works / where it fails" talking points (PLAN.md §8)

## Session log
- 2026-10-14: Planning session. Created CLAUDE.md, PROGRESS.md, PLAN.md, 3 agents. Researcher live-tested sources. User chose D1–D4 (all recommended options). Waiting on D5 (Step-1 answers).
- 2026-10-14: D5 resolved (Step-1 info is inside the brief). REQUIREMENTS.md written (10 lines). T0.6 portfolio research started.
- 2026-10-14: T0.6 done. portfolio.md written by researcher; 9 items marked unverified. Pending D6 (exited/partner entries) and user go-ahead for Phase 1.
- 2026-10-14: User added: impact analysis is the crux (multi-prompt, investor metrics, precedents), track sector peers, fixed 3-part format; then plain list layout without categories/jargon. PLAN rev 2 + REQUIREMENTS updated. Phase 1 build and T0.7 research started in parallel.
- 2026-10-14: Phase 1 done + verified. T0.7 done. Phase 2 started (software-engineer).
- 2026-10-14: Phase 2 done + verified (79s run). README written. Review found relevance/ranking issues → T2.6 in flight.
- 2026-10-14: T2.6 done (relevance rubric, min-3 ranking, funding filter, full triage audit). T2.7 watchlist queries started. User edited README formatting (keep).
- 2026-10-14: T2.7 done (watchlist queries, 114s run, 1 page). Page had 0 negative items → T2.8 page-mix rules started.
- 2026-10-14: User rejected T2.8 quotas; asked for an importance matrix + strict 7-day window. PLAN §5.2b added. T2.9 sent to software-engineer.
- 2026-10-14: T2.9 done (matrix ranking, strict 7d). Found keyword pre-cut contradicts 'top matrix scorers shown' → T2.10: triage all items in parallel batches.
- 2026-10-14: T2.10 done + verified by main session (order, 7-day, weights, 1 page). README/PLAN sources updated. Working model complete.
- 2026-10-14: Social posts now ALWAYS excluded (hardcoded SOCIAL_SOURCES + domain check in clean.py; config key removed, by user requirement). Full run re-verified: 3 social posts dropped, 129 s, 7 analysed items.
- 2026-10-14: User is submitting the project → T4.1 API-key backends started (any key beats the CLI). PLAN §5.0 added.
- 2026-10-14: T4.1/T4.2 done and verified (pytest 20 passed; full run via CLI 136s, 7 items). PLAN §6 updated for API keys. Publishing to GitHub (T4.3).
