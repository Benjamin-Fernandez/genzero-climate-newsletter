"""Dedupe, keyword-score and cap items."""
import logging
import re
from difflib import SequenceMatcher

log = logging.getLogger("newsletter.clean")

TIER_WEIGHT = {"portfolio": 5, "competitor_investors": 4, "sector_peers": 3, "partners_watch": 3}
KEYWORD_WEIGHT = 1


def norm_title(title):
    return re.sub(r"[^a-z0-9]+", " ", title.lower()).strip()


def word_re(term, ignore_case):
    return re.compile(r"(?<!\w)" + re.escape(term) + r"(?!\w)", re.IGNORECASE if ignore_case else 0)


def build_matchers(genzero, sector_peers=()):
    """List of (regex, name, tier, weight, related_holding). Entity names are matched
    case-sensitively (avoids 'imperative', 'perennial'); keywords case-insensitively."""
    matchers = []
    for tier, weight in TIER_WEIGHT.items():
        for entry in genzero.get(tier) or []:
            matchers.append((word_re(entry["name"], False), entry["name"], tier, weight, None))
    for group in sector_peers or []:
        for peer in group["peers"]:
            matchers.append((word_re(peer, False), peer, "peer", TIER_WEIGHT["sector_peers"], group["portfolio_company"]))
    for kw in genzero.get("keywords") or []:
        matchers.append((word_re(kw, True), kw, "keyword", KEYWORD_WEIGHT, None))
    return matchers


def score_item(item, matchers):
    text = item["title"] + " " + item["summary"]
    score, entities, keywords, seen = 0, [], [], set()
    for rx, name, tier, weight, holding in matchers:
        if (name, tier, holding) in seen or not rx.search(text):
            continue
        seen.add((name, tier, holding))
        score += weight
        if tier == "keyword":
            keywords.append(name)
        else:
            entities.append({"name": name, "tier": tier, "related_holding": holding})
    item["keyword_score"] = score
    item["matched_entities"] = entities
    item["matched_keywords"] = keywords


FUNDING_RE = re.compile(
    r"(?:S\$|[$€£])\s?\d|\d\s?(?:million|billion|bn|m)\b|\bSeries [A-F]\b|\bseed\b|\bfunding round\b", re.IGNORECASE)


def is_funding_noise(item):
    """Funding-query items must really be about money ('raises concern' is not a raise)."""
    return item["source_type"] == "funding" and not FUNDING_RE.search(item["title"])


def is_promo(item):
    title = item["title"].lower()
    return "techcrunch" in item["source"].lower() and ("disrupt" in title or "tickets" in title)


AMOUNT_RE = re.compile(r"[$€£]\s?\d[\d.,]*\s?(?:[mbk]|million|billion)?", re.IGNORECASE)


def story_key(title):
    """(first word, $ amount) of a title, or None if there is no amount."""
    amount = AMOUNT_RE.search(title)
    words = norm_title(title).split()
    if not amount or not words:
        return None
    return words[0], re.sub(r"\s", "", amount.group(0).lower())


def is_duplicate(item, kept):
    """Same story as an earlier kept item: similar title, or same leading word + same amount."""
    key = norm_title(item["title"])
    story = story_key(item["title"])
    for other in kept:
        if item["url"] == other["url"] or SequenceMatcher(None, key, norm_title(other["title"])).ratio() > 0.75:
            return True
        if story and story == story_key(other["title"]):
            return True
    return False


# Social-media posts are never news sources. Fixed by design, deliberately not configurable.
SOCIAL_SOURCES = {"facebook", "instagram", "linkedin", "x", "twitter", "youtube", "tiktok",
                  "reddit", "threads", "pinterest", "snapchat", "telegram", "whatsapp"}
SOCIAL_DOMAIN_RE = re.compile(
    r"://(?:[\w-]+\.)*(?:facebook|instagram|linkedin|twitter|x|youtube|youtu|tiktok|reddit|threads|pinterest|t)\.(?:com|net|be|me)/",
    re.IGNORECASE)


def is_social(item):
    return item["source"].strip().lower() in SOCIAL_SOURCES or bool(SOCIAL_DOMAIN_RE.search(item["url"]))


def is_non_english(title):
    """Simple heuristic: more than 30% of the letters in the title are non-ASCII."""
    letters = [c for c in title if c.isalpha()]
    return bool(letters) and sum(not c.isascii() for c in letters) / len(letters) > 0.3


def clean(items, config):
    matchers = build_matchers(config["genzero"], config.get("sector_peers"))
    kept, foreign, social = [], 0, 0
    for item in items:
        if is_social(item):
            social += 1
            continue
        if is_non_english(item["title"]):
            foreign += 1
            continue
        if is_promo(item) or is_funding_noise(item) or is_duplicate(item, kept):
            continue
        score_item(item, matchers)
        kept.append(item)
    log.info("Dropped %d social-media posts, %d non-English items", social, foreign)
    kept.sort(key=lambda i: i["published"], reverse=True)  # keyword_score stays as context; it never cuts
    cap = config["limits"]["max_items_for_llm"]
    if len(kept) > cap:
        log.warning("Safety cap: %d items over the limit of %d were cut (oldest first)", len(kept) - cap, cap)
    return kept[:cap]
