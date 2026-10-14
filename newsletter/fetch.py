"""Fetch RSS sources into normalised item dicts. Each source fails soft."""
import calendar
import hashlib
import html
import logging
import re
from datetime import datetime, timedelta, timezone

import feedparser
import requests

from newsletter.watchlist import watchlist_urls

log = logging.getLogger("newsletter.fetch")
USER_AGENT = "GenZeroNewsletterBot/0.1 (internal weekly digest; contact: genzero-newsletter)"


def strip_html(text, limit=600):
    text = re.sub(r"<[^>]+>", " ", text or "")
    text = re.sub(r"\s+", " ", html.unescape(text)).strip()
    return text[:limit]


def parse_entry(entry, source):
    parsed = entry.get("published_parsed") or entry.get("updated_parsed")
    if not parsed or not entry.get("link"):
        return None
    published = datetime.fromtimestamp(calendar.timegm(parsed), tz=timezone.utc)
    raw_title = html.unescape(entry.get("title", "")).strip()
    title, name = raw_title, source["name"]
    summary = strip_html(entry.get("summary", ""))
    if source.get("kind") == "google_news":
        publisher = (entry.get("source") or {}).get("title", "")
        if publisher:
            name = publisher
            suffix = " - " + publisher
            if title.endswith(suffix):
                title = title[: -len(suffix)]
        # Google's summary just repeats the title and publisher: drop it
        if summary.startswith(title) or summary == publisher:
            summary = ""
    return {
        "id": hashlib.sha1(entry["link"].encode()).hexdigest()[:10],
        "title": title,
        "url": entry["link"],
        "source": name,
        "source_type": source["type"],
        "published": published.isoformat(),
        "summary": summary,
    }


DROPPED = {"no_date": 0, "too_old": 0}  # reset by fetch_all, reported by run.py


def fetch_source(source, days, timeout, url=None):
    resp = requests.get(url or source["url"], headers={"User-Agent": USER_AGENT}, timeout=timeout)
    resp.raise_for_status()
    feed = feedparser.parse(resp.content)
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    items = []
    for entry in feed.entries:
        item = parse_entry(entry, source)
        if not item:
            DROPPED["no_date"] += 1
        elif datetime.fromisoformat(item["published"]) < cutoff:
            DROPPED["too_old"] += 1
        else:
            items.append(item)
    return items


def fetch_all(config):
    """Return (items, status) where status maps feed name -> item count or 'FAILED'."""
    days = config["limits"]["days"]
    DROPPED.update(no_date=0, too_old=0)
    timeout = config["limits"]["timeout"]
    items, status = [], {}
    for source in config["sources"]:
        urls = watchlist_urls(config, source) if source.get("watchlist") else [source["url"]]
        got, errors = [], 0
        for url in urls:  # watchlist queries may be split into several URLs; each fails soft
            try:
                got += fetch_source(source, days, timeout, url)
            except Exception as exc:
                errors += 1
                log.warning("Source %s failed (%s): %s", source["name"], url[:80], exc)
        if got:
            items += got
            status[source["name"]] = len(got)
        else:
            if not errors:
                log.warning("Source %s failed: no items in window", source["name"])
            status[source["name"]] = "FAILED"
    return items, status
