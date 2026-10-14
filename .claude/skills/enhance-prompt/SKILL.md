---
name: enhance-prompt
description: Rewrites a raw software or requirements request for the GenZero newsletter project into a precise, scoped task before any work starts. Use on every user prompt that asks to build, change, fix or specify software or requirements. Skip for chit-chat, status questions and yes/no answers.
---

# Enhance prompt (project-local stand-in for the ECC prompt enhancer)

Given the user's raw prompt, produce an **enhanced prompt** and show it to the user in a short block
headed `Enhanced prompt:` before acting on it. Then act on the enhanced version.

Build it from these parts (one or two lines each, omit any that don't apply):
1. **Goal**: the outcome in one sentence, in the user's terms.
2. **Context**: the relevant PROGRESS.md task ID(s) and PLAN.md section(s).
3. **Scope**: files and modules that may change. **Out of scope**: what must not change.
4. **Constraints**: the rules from CLAUDE.md that apply (simple first, fail-soft, 1-page/2–4-line limits,
   local Claude CLI, no new deps without approval).
5. **Acceptance criteria**: concrete and checkable (a command plus its expected result).
6. **Agent routing**: which agent(s) do which part (`planner` / `researcher` / `software-engineer`).
7. **Open questions**: anything ambiguous that needs a user decision. If any is blocking, ask before acting.

Rules:
- Do not add features the user did not ask for. Enhancement clarifies; it does not expand scope.
- Keep the enhanced prompt under ~15 lines.
