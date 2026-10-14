"""Build Google News RSS search URLs for the watchlist sources from config (never hardcoded)."""
from urllib.parse import quote

BASE = "https://news.google.com/rss/search?q={q}&hl=en-SG&gl=SG&ceid=SG:en"
MAX_QUERY_CHARS = 1500
MAX_TERMS = 4  # Google News ignores 'when:7d' on big OR queries (tested: 14 terms -> mostly old items)


def names_for(config, groups):
    """Distinctive names for the given config groups. Funds are skipped.
    Generic names get a qualifier from config['watchlist_qualifiers'], e.g. ("Rize" rice)."""
    qualifiers = config.get("watchlist_qualifiers") or {}
    seen, terms = set(), []
    for group in groups:
        if group == "sector_peers":
            entries = [{"name": p} for g in config["sector_peers"] for p in g["peers"]]
        else:
            entries = config["genzero"].get(group) or []
        for entry in entries:
            name = entry["name"]
            sector = entry.get("sector", "") + entry.get("type", "")
            if name in seen or "fund" in sector.lower():
                continue
            seen.add(name)
            term = f'"{name}"'
            if name in qualifiers:
                term = f"({term} {qualifiers[name]})"
            terms.append(term)
    return terms


def chunk_terms(terms, limit=MAX_QUERY_CHARS):
    """Split terms into OR-groups whose query text stays under `limit` characters."""
    chunks, current, size = [], [], 0
    for term in terms:
        if current and (size + len(term) + 4 > limit or len(current) >= MAX_TERMS):
            chunks.append(current)
            current, size = [], 0
        current.append(term)
        size += len(term) + 4
    if current:
        chunks.append(current)
    return chunks


def watchlist_urls(config, source):
    """One URL per chunk of names, restricted to the last 7 days."""
    terms = names_for(config, source["watchlist"])
    return [BASE.format(q=quote("(" + " OR ".join(chunk) + ") when:7d")) for chunk in chunk_terms(terms)]
