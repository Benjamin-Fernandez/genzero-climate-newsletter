"""python run.py [--no-llm] -> output/newsletter_DATE.html + items_DATE.json"""
import argparse
import json
import logging
import time
from datetime import date
from pathlib import Path

import yaml

from newsletter import llm, providers
from newsletter.clean import clean
from newsletter.fetch import DROPPED, fetch_all
from newsletter.render import heuristic_items, render

ROOT = Path(__file__).parent


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-llm", action="store_true", help="skip Claude, use heuristics")
    args = parser.parse_args()
    providers.load_env()
    started = time.time()
    logging.basicConfig(level=logging.INFO, format="%(levelname)s %(message)s")

    config = yaml.safe_load((ROOT / "config.yaml").read_text(encoding="utf-8"))
    llm.validate_matrix(config)
    providers.configure(config)
    if not args.no_llm:
        backend = providers.detect_backend()
        if backend:
            print(providers.describe(backend))
        else:
            print(providers.NO_LLM_MESSAGE)
            args.no_llm = True
    raw, status = fetch_all(config)
    print(f"Dropped for age: {DROPPED['too_old']}, for missing date: {DROPPED['no_date']}")
    print("Watchlist items fetched:", sum(1 for r in raw if r["source_type"] == "watchlist"))
    items = clean(raw, config)

    page_items, glance = None, None
    if not args.no_llm:
        result = llm.analyse(items, config)  # Phase 2 returns page items, or None on failure
        if result:
            page_items = result
    if page_items is None:
        page_items = heuristic_items(items, config)
        if not args.no_llm:
            for p in page_items:
                p["impact"] = "Analysis unavailable this week"

    today = date.today().isoformat()
    meta = {
        "date": today,
        "sources_ok": [n for n, s in status.items() if s != "FAILED"],
        "sources_failed": [n for n, s in status.items() if s == "FAILED"],
        "scanned": len(raw),
    }
    out = ROOT / "output"
    out.mkdir(exist_ok=True)
    html_path = out / f"newsletter_{today}.html"
    html_path.write_text(render(page_items, meta, glance), encoding="utf-8")
    (out / f"items_{today}.json").write_text(
        json.dumps({"source_counts": status, "triage": llm.LAST_TRIAGE, "items": items, "page_items": page_items}, indent=2, ensure_ascii=False),
        encoding="utf-8",
    )
    print(f"Total time: {time.time() - started:.0f}s")
    print(f"Done: {html_path} | {len(page_items)} items | sources OK {len(meta['sources_ok'])} / failed {len(meta['sources_failed'])}")
    print("Per source:", status)


if __name__ == "__main__":
    main()
