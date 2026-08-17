#!/usr/bin/env python3
"""Regenerate the '## 📊 Corpus Statistics' section of README.md from
statistics.json. Intended for the CI `refresh` job so the curated stats
README stays in sync with refreshed data WITHOUT reverting to the full
paper list (which scripts/generate_readme.py would do)."""
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ORG = "tobias-weiss-ai-xr"


def cat_total(v):
    if isinstance(v, dict):
        return v.get("total", v.get("papers", 0))
    return v if isinstance(v, int) else 0


def bar(n, max_n, width=12):
    if not max_n:
        return ""
    filled = int(n / max_n * width)
    return "█" * filled + "░" * (width - filled)


def render():
    stat = json.load(open(ROOT / "statistics.json"))
    meta = stat.get("metadata", {})
    total = meta.get("total_papers", 0)
    gen = meta.get("generated_date", "")
    src = stat.get("source_breakdown", {})
    by_cat = stat.get("by_category", {})
    by_year = stat.get("by_year", {})
    momentum = stat.get("momentum", [])
    bursts = stat.get("keyword_bursts", [])
    venues = stat.get("venues", [])
    gaps = stat.get("gaps", {}).get("thinnest_cells", [])
    repo = ROG = ROOT.name

    src_parts = []
    for k in ("arxiv", "doi", "other"):
        n = src.get(k, 0)
        if n:
            pct = n * 100 // total if total else 0
            label = "arXiv" if k == "arxiv" else ("DOI" if k == "doi" else "Other")
            src_parts.append(f"**{label}** {n:,} ({pct}%)")
    src_line = " · ".join(src_parts) if src_parts else "No source breakdown"
    gh_pages = f"https://{ORG}.github.io/{repo}"

    items = sorted(by_cat.items(), key=lambda x: cat_total(x[1]), reverse=True)
    top_n = 10
    cat_rows = ""
    rem = 0
    for i, (cid, v) in enumerate(items):
        n = cat_total(v)
        recent = v.get("recent", 0) if isinstance(v, dict) else 0
        if i < top_n:
            mx = cat_total(items[0][1]) if items else 0
            cat_rows += f"| {cid} | **{n:,}** | {recent:,} | {bar(n, mx)} |\n"
        else:
            rem += n
    if rem:
        cat_rows += f"| *other* | **{rem:,}** | | |\n"

    year_rows = ""
    if by_year:
        mx = max(by_year.values())
        for y in sorted(by_year.keys())[-3:]:
            year_rows += f"| {y} | {by_year[y]:,} | {bar(by_year[y], mx)} |\n"

    mom_rows = "".join(
        f"| {m.get('name', m.get('id', '?'))} | {m.get('total', 0):,} | "
        f"{m.get('papers_per_month', 0):.1f}/mo | {m.get('recent_share', 0):.0%} | {m.get('score', 0):.0f} |\n"
        for m in momentum[:5]
    )
    burst_rows = "".join(
        f"| {b.get('keyword', '?')} | {b.get('total', 0):,} | {b.get('burst_score', 0):.2f} |\n"
        for b in bursts[:8]
    )
    venue_rows = ""
    for v in venues[:8]:
        if isinstance(v, dict):
            venue_rows += f"| {v.get('name', '?')} | {v.get('papers', 0)} |\n"
        elif isinstance(v, list) and len(v) >= 2:
            venue_rows += f"| {v[0]} | {v[1]} |\n"

    gap_rows = "".join(f"| `{g.get('cell', '?')}` | {g.get('papers', 0)} |\n" for g in gaps[:5])

    lines = [
        "## 📊 Corpus Statistics", "",
        f"**{total:,} papers** across **{len(by_cat)} categories**.  ",
        f"Sources: {src_line}.  ",
        f"Full paper list: [GitHub Pages site]({gh_pages}).", "",
    ]
    if cat_rows:
        lines += ["### Top categories", "", "| Category | Papers | Recent | |", "|----------|--------|--------|-|", cat_rows, ""]
    if year_rows:
        lines += ["### By year", "", "| Year | Papers | |", "|------|--------|-|", year_rows, ""]
    if mom_rows:
        lines += ["### Momentum (hottest categories)", "", "| Category | Total | Rate | Recent | Score |", "|----------|-------|------|--------|-------|", mom_rows, ""]
    if burst_rows:
        lines += ["### Trending keywords", "", "| Keyword | Papers | Burst |", "|---------|--------|-------|", burst_rows, ""]
    if venue_rows:
        lines += ["### Top venues", "", "| Venue | Papers |", "|-------|--------|", venue_rows, ""]
    if gap_rows:
        lines += ["### Research gaps (thinnest cells)", "", "| Cell | Papers |", "|------|--------|", gap_rows, ""]
    if gen and gen != "None":
        lines += ["", f"*Generated {gen} by `scripts/standard_stats.py`.*"]
    return "\n".join(lines)


def main():
    readme = ROOT / "README.md"
    text = readme.read_text(encoding="utf-8")
    start = text.find("## 📊 Corpus Statistics")
    if start < 0:
        print("no stats section found; skipping")
        return
    nxt = text.find("\n## ", start + 1)
    if nxt < 0:
        nxt = len(text)
    new_text = text[:start] + render() + "\n\n" + text[nxt:]
    readme.write_text(new_text, encoding="utf-8")
    print("README stats section refreshed from statistics.json")


if __name__ == "__main__":
    main()
