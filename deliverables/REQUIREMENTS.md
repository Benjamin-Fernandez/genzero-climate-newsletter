1. Audience: GenZero CEO and CIO. A weekly climate-tech briefing read through an investor's lens, covering strictly the last 7 days (never further back, even in a quiet week).
2. Run: one command (`python run.py`), repeatable every week on the local machine with no manual steps.
3. Sources: at least 3 sources spanning at least 2 types. RSS only: Google News (funding, negative-news and portfolio/peer watchlist queries), TechCrunch Climate, CTVC, Carbon Brief, Eco-Business.
4. Not a news summary: each item says what happened and why it matters to investors and GenZero's portfolio.
5. Priority content: fundraises by competitors, by companies in GenZero's sectors and by rivals of its portfolio companies, plus positive and especially negative news.
6. An LLM (any API key in .env, else the local Claude Code CLI) grades each item on a weighted importance matrix (0–100). The top scorers are shown, then it reasons through investor metrics to explain the impact on GenZero.
7. Format: one-page HTML in plain English, a simple list ordered by importance. Each item has 1 line on what happened, 1 on the link to GenZero, and 1–2 on why it matters.
8. Robustness: a failed source or a failed LLM call is logged and skipped, and a newsletter is still produced.
9. Scope: a simple working model first; full-text fetching.
10. Deliverables: this note, the one-page HTML newsletter, runnable code, and README.
