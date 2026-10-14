"""Heuristic (no-LLM) item building and Jinja2 rendering."""
import re
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, select_autoescape

SECTIONS = [
    ("risks", "Risks & Negative Signals"),
    ("deals", "Deals & Competitor Moves"),
    ("policy", "Policy & Markets"),
    ("tech", "Technology Signals"),
]
NEGATIVE = r"bankrupt|insolven|cancel|layoff|layoffs|shuts? down|scrapp|collapse|fraud|scandal|rollback|halt|delay|loses|lawsuit"
FUNDING = r"raises|raised|funding|series [a-d]|seed round|secures|closes|fund close|acquire|acquisition|merger|invest"
POLICY = r"policy|regulation|subsid|tariff|carbon market|article 6|corsia|tax credit|government|law|ban|target|cop\d"
TIER_LABEL = {
    "portfolio": "Portfolio",
    "competitor_investors": "Competitor investor",
    "partners_watch": "Partner",
    "sector_peers": "Peer",
    "peer": "Peer",
}


def classify(text):
    text = text.lower()
    for section, pattern in (("risks", NEGATIVE), ("deals", FUNDING), ("policy", POLICY)):
        if re.search(pattern, text):
            return section
    return "tech"


def to_page_item(item):
    text = item["title"] + " " + item["summary"]
    section = classify(text)
    sentiment = {"risks": "▼", "deals": "▲"}.get(section, "●")
    tags = [f"{TIER_LABEL[e['tier']]}: {e['name']}" for e in item["matched_entities"]]
    names = [e["name"] for e in item["matched_entities"]] + item["matched_keywords"]
    return {
        "section": section,
        "title": item["title"],
        "url": item["url"],
        "source": item["source"],
        "tags": tags[:3],
        "sentiment": sentiment,
        "what": (item["summary"] or item["title"])[:150],
        "genzero_link": ", ".join(names[:5]) if names else "Sector news",
        "impact": "LLM analysis disabled (--no-llm)",
    }


def heuristic_items(items, config):
    page = [to_page_item(i) for i in items]
    # risks get priority on a short page
    ranked = sorted(zip(items, page), key=lambda p: p[0]["keyword_score"] + (3 if p[1]["section"] == "risks" and p[0]["keyword_score"] > 0 else 0), reverse=True)
    return [p for _, p in ranked[: config["limits"]["max_items_on_page"]]]


def render(items, meta, glance=None, template_dir=None):
    """items: dicts with section,title,url,source,tags,sentiment,what,genzero_link,impact.
    Shown as one numbered list in the given (importance) order; section/tags/sentiment are not displayed."""
    template_dir = template_dir or Path(__file__).parent
    env = Environment(loader=FileSystemLoader(str(template_dir)), autoescape=select_autoescape(["html"]))
    return env.get_template("template.html").render(items=items, **meta)
