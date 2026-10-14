# GenZero Climate-Tech Weekly Newsletter — Project Rules

## What this project is
A one-command Python pipeline (`python run.py`) that pulls the last 7 days of climate-tech news from
≥3 sources (≥2 source types), uses an LLM (any API key in `.env` first, else the local Claude Code CLI) to grade every item on an importance
matrix against GenZero's portfolio, peers and competitors, and renders a ONE-PAGE HTML newsletter for the
CEO and CIO. Full design and current state: `PLAN.md`. Task log: `PROGRESS.md`. Deliverables: `deliverables/`.
Published at https://github.com/Benjamin-Fernandez/genzero-climate-newsletter (commit and push after verified changes).

## START OF EVERY SESSION (mandatory)
1. Read `PROGRESS.md` → "Current state" and "Next step". Resume from there; do not restart work.
2. Read `PLAN.md` only for the sections relevant to the next step.
3. Check "Open decisions" in `PROGRESS.md`. Never implement something that depends on an open decision. Ask the user.

## Golden rules
- **Simple working model first.** A runnable end-to-end pipeline beats a clever partial one. No new
  frameworks, databases, queues, web servers or async code unless the user approves it.
- **No design changes without the user.** If a choice has trade-offs that PLAN.md does not settle, present
  2–3 options with pros/cons (AskUserQuestion) and record the outcome in `PLAN.md` § Decision log.
- **Deliverable size limits are hard limits:** `deliverables/REQUIREMENTS.md` ≤ 10 lines, `deliverables/README.md` ≤ 5 entries,
  newsletter ≤ 1 printed A4 page, each news item 2–4 lines (what happened + why it matters to investors/GenZero).
- **Stability over coverage:** prefer RSS / no-key APIs over scraping. A failing source must be logged
  and skipped, never crash the run.
- **Secrets:** LLM API keys live only in the git-ignored `.env` (template `.env.example`). Never commit, print or log them.
- Windows 11 + Python 3.12. The `claude` CLI is NOT on PATH; it is bundled with the VS Code extension
  (`~/.vscode/extensions/anthropic.claude-code-*/resources/native-binary/claude.exe`). Code must
  resolve it via `CLAUDE_BIN` env var → `claude` on PATH → newest VS Code extension binary.

## Prompt enhancement rule
For any user prompt that is a software or requirements request, invoke the project skill
`enhance-prompt` (`.claude/skills/enhance-prompt/SKILL.md`) first, show the enhanced prompt, then act on it.
It stands in for the ECC (Everything Claude Code) enhancer, which is not installed (decision D4, 2026-10-14).
Skip enhancement for chit-chat, status questions and yes/no answers.

## Agent roster (`.claude/agents/`)
Spawn agents for their dedicated tasks; the main session orchestrates and keeps PROGRESS.md current.
| Agent | Use for | Never |
|---|---|---|
| `planner` | Breaking a phase into tasks, updating PLAN.md, preparing option/pros-cons briefs for the user | Writing code |
| `researcher` | Testing sources/feeds, looking up GenZero portfolio & competitors, checking library/CLI behaviour | Writing project code |
| `software-engineer` | Implementing one task from PROGRESS.md, running it end to end, fixing failures | Changing the design or adding scope |

How to spawn: `Agent(subagent_type="software-engineer", prompt="Task <id> from PROGRESS.md: ...")`.
If the type is "not found" (agents created mid-session load only in the next session), use
`subagent_type="general-purpose"` and start the prompt with "Read .claude/agents/<name>.md and follow its rules."
Always pass the task ID, the acceptance criteria, and the files it may touch. Run independent
agents in parallel. After an agent returns, the main session verifies and updates PROGRESS.md.

## Progress tracking (survives token limits / manual stops)
- `PROGRESS.md` is the single source of truth. Update it **immediately after each task finishes**,
  not at the end of the session: tick the box, update "Current state", "Next step", and add one line
  to the session log (date, what changed, what's broken).
- If you are about to stop mid-task, write what is half-done and how to continue under "Next step".

## Commands
- Run pipeline: `python run.py` (writes `output/newsletter_YYYY-MM-DD.html` and `output/items_YYYY-MM-DD.json`)
- Dry run without LLM (for testing fetch/render): `python run.py --no-llm` (WARNING: it overwrites today's `output/newsletter_DATE.html`, so re-run the full pipeline afterwards)
- Fixed rules (not configurable, by user requirement): strict 7-day window; social-media posts never included; ranking only by the importance matrix, with no quotas.
- Install deps: `pip install -r requirements.txt`
