"""LLM analysis (backend chosen in providers.py: API key if present, else the local Claude Code CLI).
Stage A: one batched triage call. Rank in code. Stage B: one impact call per selected item."""
import json
import logging
import re
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

from newsletter import providers
from newsletter.clean import is_duplicate

log = logging.getLogger("llm")
PROMPTS = Path(__file__).parent / "prompts"
TIERS = ["portfolio", "partners_watch", "peer", "competitor_investor"]
EVENT_TYPES_OTHER = "other"


# ---------- helpers ----------

def load_prompt(name, **values):
    text = (PROMPTS / name).read_text(encoding="utf-8")
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    return text


def names(entries):
    return ", ".join(e["name"] for e in entries or [])


def event_types(config):
    return [p["event_type"] for p in config["impact_framework"]["playbook"]] + [EVENT_TYPES_OTHER]


# ---------- T2.2 Stage A: triage ----------

def validate_matrix(config):
    """Fail early with a clear message if the scoring matrix is broken."""
    matrix = config.get("scoring_matrix") or {}
    criteria = matrix.get("criteria") or []
    if not criteria:
        raise SystemExit("config.yaml: scoring_matrix.criteria is missing")
    total = sum(c["weight"] for c in criteria)
    if total != 100:
        raise SystemExit(f"config.yaml: scoring_matrix weights sum to {total}, they must sum to 100")


def scores_schema(config):
    ids = [c["id"] for c in config["scoring_matrix"]["criteria"]]
    return {"type": "object", "required": ids,
            "properties": {i: {"type": "integer", "minimum": 0, "maximum": 5} for i in ids}}


def matrix_text(config):
    lines = []
    for c in config["scoring_matrix"]["criteria"]:
        levels = "; ".join(f"{k} = {v}" for k, v in sorted(c["levels"].items(), reverse=True))
        lines.append(f"- {c['id']} (weight {c['weight']}): {c['question']} Levels: {levels}")
    return "\n".join(lines)


def importance_from(scores, config):
    """Authoritative importance (0-100) = sum(weight * score / 5)."""
    return round(sum(c["weight"] * scores.get(c["id"], 0) / 5 for c in config["scoring_matrix"]["criteria"]))


def triage_schema(config):
    entity = {"type": "object", "required": ["name", "tier", "related_holding"], "properties": {
        "name": {"type": "string"}, "tier": {"type": "string", "enum": TIERS}, "related_holding": {"type": "string"}}}
    item = {"type": "object",
            "required": ["id", "event_type", "entities", "scores", "importance", "score_reason", "sentiment", "duplicate_of", "one_line"],
            "properties": {
                "id": {"type": "integer"},
                "event_type": {"type": "string", "enum": event_types(config)},
                "entities": {"type": "array", "items": entity},
                "scores": scores_schema(config),
                "importance": {"type": "integer", "minimum": 0, "maximum": 100},
                "score_reason": {"type": "string", "maxLength": 120},
                "sentiment": {"type": "string", "enum": ["positive", "negative", "neutral"]},
                "duplicate_of": {"type": ["integer", "null"]},
                "one_line": {"type": "string", "maxLength": 150}}}
    return {"type": "object", "required": ["items"], "properties": {"items": {"type": "array", "items": item}}}


def triage_batch(ids, items, config, watchlist):
    """Grade one batch of items (global ids). Returns {id: triage dict} or None if the call failed."""
    compact = [{"id": i, "title": items[i]["title"], "source": items[i]["source"], "summary": items[i]["summary"][:400],
                "watchlist_hits": [e["name"] for e in items[i]["matched_entities"]]} for i in ids]
    prompt = load_prompt("triage.md", EVENT_TYPES=", ".join(event_types(config)[:-1]),
                         MATRIX=matrix_text(config), WATCHLIST=json.dumps(watchlist, ensure_ascii=False),
                         ITEMS=json.dumps(compact, ensure_ascii=False))
    cfg = config["llm"]
    out = providers.complete_json(prompt, triage_schema(config), cfg["triage_timeout"], cfg["effort"]["triage"])  # includes one retry
    if not out or not out.get("items"):
        return None
    triaged = {t["id"]: t for t in out["items"] if t.get("id") in ids}
    for i, t in triaged.items():
        t["llm_importance"] = t.get("importance")
        t["importance"] = importance_from(t["scores"], config)  # the code's value is authoritative
        if abs(t["importance"] - (t["llm_importance"] or 0)) > 5:
            log.info("item %s: LLM total %s differs from computed %s", i, t["llm_importance"], t["importance"])
    return triaged


def triage(items, config):
    """Grade ALL items in parallel batches. Returns (triaged, n_batches, failed_batches) or None if every batch failed.
    Items of a failed batch are simply absent from `triaged` (not graded, never shown)."""
    g = config["genzero"]
    watchlist = {
        "portfolio": [e["name"] for e in g["portfolio"]],
        "partners_watch": [e["name"] for e in g["partners_watch"]],
        "sector_peers": {p["portfolio_company"]: p["peers"] for p in config["sector_peers"]},
        "competitor_investors": [e["name"] for e in g["competitor_investors"]],
        "keywords": g["keywords"],
    }
    size = config["llm"]["triage_batch_size"]
    batches = [list(range(a, min(a + size, len(items)))) for a in range(0, len(items), size)]
    with ThreadPoolExecutor(max_workers=providers.worker_count(config["llm"]["max_workers"])) as pool:
        results = list(pool.map(lambda b: triage_batch(b, items, config, watchlist), batches))
    triaged, failed = {}, 0
    for r in results:
        if r is None:
            failed += 1
        else:
            triaged.update(r)
    if failed == len(batches):
        return None
    return triaged, len(batches), failed


# ---------- T2.3 rank in code ----------

def score(t):
    return t["importance"]


COMPANY_VERBS = r"^(.+?)\s+(?:raises|raised|valued|closes|closed|secures|secured|nabs?|lands|bags|gets)\b"
GENERIC_WORDS = {"german", "cleantech", "company", "climate", "startup", "firm", "tech", "carbon", "energy", "green", "grad",
                 "american", "british", "singapore", "global", "ventures", "capital", "group", "inc"}


def company_tokens(title, t):
    """Distinctive words of the company in focus: first matched entity, else the title words before 'raises', 'valued'..."""
    if t["entities"]:
        phrase = t["entities"][0]["name"]
    else:
        m = re.match(COMPANY_VERBS, title, re.IGNORECASE)
        if not m:
            return set()
        phrase = m.group(1)
    words = re.findall(r"[a-z0-9]+", phrase.lower())
    return {w for w in words if len(w) >= 4 and w not in GENERIC_WORDS}


def mark_same_company(items, triaged):
    """Across all batches, keep the highest-importance item of each story. Items are the same story if the LLM linked
    them (duplicate_of, which only works inside a batch), they share a company and event_type, or titles are near-identical."""
    group = {i: (t["duplicate_of"] if t.get("duplicate_of") is not None else i) for i, t in triaged.items()}
    for t in triaged.values():
        t["duplicate_of"] = None
    kept = []
    for i in sorted(triaged, key=lambda i: (-score(triaged[i]), i)):
        t = triaged[i]
        tokens = company_tokens(items[i]["title"], t)
        for j in kept:
            same_company = triaged[j]["event_type"] == t["event_type"] and tokens & company_tokens(items[j]["title"], triaged[j])
            linked = group[i] == group[j] or group[i] == j or group[j] == i
            if linked or same_company or is_duplicate(items[i], [items[j]]):
                t["duplicate_of"] = j
                break
        else:
            kept.append(i)


def rank(triaged, items, limit, min_score):
    """Importance (desc), recency breaks ties; drop duplicates and anything below min_score; take the top `limit`."""
    live = [i for i, t in triaged.items() if t.get("duplicate_of") is None and t["importance"] >= min_score]
    live.sort(key=lambda i: items[i]["published"], reverse=True)
    live.sort(key=lambda i: -triaged[i]["importance"])
    return live[:limit]


# ---------- T2.4 Stage B: impact ----------

def impact_schema():
    metric = {"type": "object", "required": ["concern_id", "direction", "why"], "properties": {
        "concern_id": {"type": "string"}, "direction": {"type": "string", "enum": ["up", "down", "mixed"]},
        "why": {"type": "string"}}}
    props = {  # order matters: reasoning before writing
        "q1_facts": {"type": "string"}, "q2_exposure": {"type": "string"}, "q3_precedent": {"type": "string"},
        "q4_metrics": {"type": "array", "items": metric}, "q5_watch": {"type": "string"},
        "what": {"type": "string", "maxLength": 150}, "genzero_link": {"type": "string", "maxLength": 150},
        "impact": {"type": "string", "maxLength": 300}}
    return {"type": "object", "required": list(props), "properties": props}


def impact_prompt(item, t, config):
    g, fw = config["genzero"], config["impact_framework"]
    holdings = {e["related_holding"] for e in t["entities"] if e.get("related_holding")}
    holdings |= {e["name"] for e in t["entities"] if e["tier"] == "portfolio"}
    peers = [f"{p['portfolio_company']}: {', '.join(p['peers'])}" for p in config["sector_peers"]
             if not holdings or p["portfolio_company"] in holdings]
    concerns = "\n".join(f"- {c['id']}: {c['name']}. {c['question']}" for c in fw["concerns"])
    play = next((p for p in fw["playbook"] if p["event_type"] == t["event_type"]), None)
    playbook = (f"{play['event_type']}: {play['typical_effects']} Metrics: {play['metrics']}. "
                f"Precedents: {'; '.join(play['precedents'])}") if play else "No playbook entry; reason from general knowledge and say so."
    entities = ", ".join(f"{e['name']} ({e['tier']}{', peer of ' + e['related_holding'] if e.get('related_holding') else ''})"
                         for e in t["entities"]) or "none found"
    text = (f"Title: {item['title']}\nSource: {item['source']}\nPublished: {item['published']}\n"
            f"Summary: {item['summary'][:1500] or '(none, headline only)'}")
    return load_prompt(
        "impact.md",
        PORTFOLIO="; ".join(f"{e['name']} ({e['sector']})" for e in g["portfolio"]),
        PARTNERS="; ".join(f"{e['name']} ({e['sector']})" for e in g["partners_watch"]),
        PEERS="\n".join(peers) or "none", COMPETITORS=names(g["competitor_investors"]),
        ENTITIES=entities, EVENT_TYPE=t["event_type"], CONCERNS=concerns, PLAYBOOK=playbook, ITEM=text)


def link_text(t):
    """Plain fallback for 'Link to GenZero' built from triage entities."""
    parts = []
    for e in t["entities"]:
        if e["tier"] == "portfolio":
            parts.append(f"{e['name']}, a GenZero investment")
        elif e["tier"] == "partners_watch":
            parts.append(f"{e['name']}, a GenZero partner")
        elif e["tier"] == "peer":
            parts.append(f"{e['name']}, a competitor of {e.get('related_holding') or 'a GenZero investment'}")
        else:
            parts.append(f"{e['name']}, a rival climate investor")
    return "; ".join(parts[:3]) or "Sector-level news, no named GenZero link"


def analyse_item(item, t, config):
    """Build one page item; falls back to the quick take if the impact call fails."""
    base = {"title": item["title"], "url": item["url"], "source": item["source"],
            "event_type": t["event_type"], "sentiment": t["sentiment"], "entities": t["entities"],
            "importance": t["importance"], "scores": t["scores"], "score_reason": t["score_reason"]}
    cfg = config["llm"]
    out = providers.complete_json(impact_prompt(item, t, config), impact_schema(), cfg["impact_timeout"], cfg["effort"]["impact"])
    if out:
        return {**base, **out, "analysis": "full"}
    return {**base, "what": t["one_line"], "genzero_link": link_text(t),
            "impact": "(quick take, detailed analysis failed)", "analysis": "quick_take"}


LAST_TRIAGE = []  # audit rows for items_DATE.json


def analyse(items, config):
    """Full pipeline. Returns the page items, or None if triage failed (caller uses the keyword list)."""
    result = triage(items, config)
    if result is None:
        print("Triage FAILED (all batches), falling back to keyword list")
        return None
    triaged, n_batches, failed = result
    mark_same_company(items, triaged)
    graded_rows = [
        {"id": i, "title": items[i]["title"], "published": items[i]["published"], "graded": True, "scores": t["scores"],
         "llm_importance": t["llm_importance"], "importance": t["importance"], "score_reason": t["score_reason"],
         "event_type": t["event_type"], "sentiment": t["sentiment"], "entities": t["entities"],
         "duplicate_of": t.get("duplicate_of"), "one_line": t["one_line"]}
        for i, t in sorted(triaged.items(), key=lambda kv: -score(kv[1]))]
    ungraded_rows = [{"id": i, "title": it["title"], "published": it["published"], "graded": False, "importance": None,
                      "keyword_score": it["keyword_score"], "note": "not graded (triage batch failed)"}
                     for i, it in enumerate(items) if i not in triaged]
    LAST_TRIAGE[:] = graded_rows + ungraded_rows
    print(f"Triage: {len(items)} items, {n_batches} batches ({failed} failed), {len(triaged)} graded")
    chosen = rank(triaged, items, config["limits"]["max_items_on_page"], config["scoring_matrix"]["min_score_to_show"])
    print(f"Selected {len(chosen)} items for the page")
    results, done = {}, 0
    with ThreadPoolExecutor(max_workers=providers.worker_count(config["llm"]["max_workers"])) as pool:
        futures = {i: pool.submit(analyse_item, items[i], triaged[i], config) for i in chosen}
        for i, fut in futures.items():
            results[i] = fut.result()
            done += 1
            print(f"Impact {done}/{len(chosen)} done ({results[i]['analysis']})")
    return [results[i] for i in chosen]
