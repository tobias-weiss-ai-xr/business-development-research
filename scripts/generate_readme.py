#!/usr/bin/env python3
"""Generate README.md from statistics.json.

Usage:
    python3 scripts/generate_readme.py          # write README.md
    python3 scripts/generate_readme.py --check  # verify README is up to date (CI)
"""

STATS_ONLY = False  # Set True to skip full paper list generation
import argparse
import json
import os
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent

CATEGORY_DISPLAY = {
    "market-analysis": "Market Analysis & Research",
    "go-to-market": "Go-to-Market Strategy",
    "sales-strategy": "Sales Strategy & Process",
    "b2b-marketing": "B2B Marketing & Lead Gen",
    "content-marketing": "Content Marketing & Thought Leadership",
    "digital-marketing": "Digital Marketing & SEO",
    "brand-building": "Brand & Positioning",
    "customer-acquisition": "Customer Acquisition & Growth",
    "customer-retention": "Customer Retention & Churn",
    "customer-success": "Customer Success & Expansion",
    "pricing-strategy": "Pricing & Monetization",
    "product-market-fit": "Product-Market Fit & Validation",
    "business-models": "Business Models & Innovation",
    "competitive-intelligence": "Competitive Intelligence",
    "partnerships": "Partnerships & Alliances",
    "sales-psychology": "Sales Psychology & Negotiation",
    "networking": "Networking & Relationships",
    "entrepreneurship": "Entrepreneurship & Small Business",
    "growth-metrics": "Growth Metrics & Analytics",
    "ai-adoption": "AI Adoption & Transformation",
}

SUBCATEGORY_DISPLAY = {
    "theory": "Theory",
    "mechanism": "Mechanism",
    "method": "Method",
    "application": "Application",
    "development": "Development",
    "systems": "Systems & Technology",
    "evaluation": "Evaluation & Benchmarks",
    "review": "Reviews & Surveys",
}


def render_readme(stats):
    meta = stats["metadata"]
    total = meta["total_papers"]
    saturation = meta["taxonomy"]["saturation"]
    filled = meta["taxonomy"]["filled_cells"]
    total_cells = meta["taxonomy"]["total_cells"]
    by_cat = stats["by_category"]
    by_sub = stats["by_subcategory"]
    by_year = stats["by_year"]
    by_cell = stats["by_cell"]
    themes = stats.get("emerging_themes_12m", [])

    years = [y for y in by_year if y != "unknown"]
    ymin = min(years, default="—")
    ymax = max(years, default="—")

    top_cats = sorted(by_cat.items(), key=lambda kv: -kv[1])[:6]
    top_cats_rows = "\n".join(
        f"{i+1}. **{CATEGORY_DISPLAY[c]}** — {n} papers" for i, (c, n) in enumerate(top_cats)
    )

    theme_rows = "\n".join(
        f"{i+1}. **{t['keyword']}** — {t['papers']} papers" for i, t in enumerate(themes[:6])
    )

    momentum = stats.get("momentum", [])[:6]
    mom_rows = "\n".join(
        f"| {m['name']} | {m['total']} | {m['recent']} | "
        + (f"{m['growth_pct']:+}%" if m['growth_pct'] is not None else "—")
        + f" | {m['recent_share']*100:.0f}% |"
        for m in momentum
    )

    thin = sorted(by_cell.items(), key=lambda kv: kv[1])[:8]
    gap_rows = "\n".join(f"- `{c}` — {n} papers" for c, n in thin)

    cat_table = "\n".join(
        f"| {CATEGORY_DISPLAY[c]} | {by_cat.get(c, 0)} |"
        for c in CATEGORY_DISPLAY
    )
    sub_table = "\n".join(
        f"| {SUBCATEGORY_DISPLAY[s]} | {by_sub.get(s, 0)} |"
        for s in SUBCATEGORY_DISPLAY
    )

    return f"""# Business Development Research Corpus

**An open research corpus for business development** — Analysis of {total:,} research papers across 20 business development disciplines.

**Author:** Tobias Weiss
**Repository:** [github.com/tobias-weiss-ai-xr/business-development-research](https://github.com/tobias-weiss-ai-xr/business-development-research)

---

## 🎯 Overview

This repository is an open research resource: a curated corpus and reusable
tooling for business development scholarship and practice — market analysis,
go-to-market, sales, B2B marketing, pricing, customer success,
entrepreneurship, AI adoption and every adjacent discipline. It mirrors the
structure of the
[graph-research](https://github.com/tobias-weiss-ai-xr/graph-research) and
[learning-research](https://github.com/tobias-weiss-ai-xr/learning-research)
corpora. The evidence it aggregates is reusable by any downstream work:
research syntheses, teaching material, the business-development framework, or
content pipelines (blog, newsletter, courses).

### Research Scope

| Metric | Value |
|--------|-------|
| **Papers Analyzed** | {total:,} |
| **Business Development Disciplines** | {len(CATEGORY_DISPLAY)} |
| **Time Span** | {ymin}-{ymax} |
| **Research Aspects** | {len(SUBCATEGORY_DISPLAY)} |
| **Taxonomy Cells** | {total_cells} |
| **Saturation** | {saturation}% ({filled}/{total_cells} cells) |

### Top Evidence Areas

{top_cats_rows}

---

## 📊 The 20-Category Taxonomy

| Category | Papers |
|----------|--------|
{cat_table}

### Research Aspects (Subcategories)

| Aspect | Papers |
|--------|--------|
{sub_table}

---

## 🚀 Emerging Themes (Last 12 Months)

{theme_rows}

## 📈 Category Momentum (Last 12 Months)

Ranked by output density × year-over-year growth — the strongest leading indicator for what to cover next:

| Category | Total | Last 12m | Growth | 12-m share |
|----------|------:|---------:|-------:|-----------:|
{mom_rows}

---

## 🕳️ Research Gaps (Thinnest Cells)

Cells with the fewest papers are prime opportunities for content and offer design:

{gap_rows if gap_rows else "- (corpus still saturating — see `statistics.json`) *"}

---

## 📁 Repository Structure

```
business-development-research/
├── README.md                          # This file
├── papers.json                        # Paper metadata (JSON export)
├── papers.yaml                        # Paper metadata (source of truth)
├── statistics.json                    # Analysis statistics
├── requirements.txt                   # Python dependencies
│
├── assets/visualizations/             # Generated charts and graphs
│
├── docs/
│   ├── research/                      # Literature review, taxonomy, trend reports
│   └── topics/                        # Generated content topics
│
├── tools/                             # Content & strategy planning tools
│   ├── topic_planner.py               # Content topic planner ✨
│   ├── trend_scanner.py               # Emerging trend scanner ✨
│   ├── brief_generator.py             # Content brief generator ✨
│   └── landscape_analyzer.py          # Corpus landscape report ✨
│
├── scripts/                           # Research pipeline
│   ├── fetch/fetch_new_papers.py      # arXiv discovery (auto-classified)
│   ├── fetch/fetch_openalex.py        # OpenAlex discovery (primary)
│   ├── fetch/fetch_other_sources.py   # DBLP/CrossRef/EuropePMC discovery
│   ├── analysis/generate_analysis.py  # Statistics + visualizations
│   ├── validate_papers.py             # Corpus validation
│   └── generate_readme.py             # README generator
│
└── examples/                          # Usage examples
```

---

## 🛠️ Tools

### 1. Content Topic Planner

Generate evidence-based content topics from the corpus.

```bash
cd tools
python3 topic_planner.py --top 10
```

### 2. Trend Scanner

Detect emerging research trends from recent papers (keyword burst analysis).

```bash
cd tools
python3 trend_scanner.py --months 6
```

### 3. Content Brief Generator

Turn a topic into a ready-to-write brief (angle, outline, key papers).

```bash
cd tools
python3 brief_generator.py "AI adoption in SMEs" --papers 5
```

### 4. Landscape Analyzer

Full picture of the corpus: growth, aspects, venues, authors, gaps.

```bash
cd tools
python3 landscape_analyzer.py --write-doc
```

---

## 🔄 Research Pipeline

1. **Discover** — `python3 scripts/fetch/fetch_openalex.py --months 3`
   (OpenAlex across 160+ queries, auto-classified into the taxonomy; arXiv
   fetcher `scripts/fetch/fetch_new_papers.py` as the secondary source)
2. **Validate** — `python3 scripts/validate_papers.py`
3. **Analyze** — `python3 scripts/analysis/generate_analysis.py`
4. **Visualize** — `python3 scripts/visualize_statistics.py`
5. **Report** — `python3 scripts/analysis/generate_reports.py`
6. **Generate** — `python3 scripts/generate_readme.py`

CI (`.github/workflows/validate.yml`) validates and regenerates on every push;
a weekly scheduled job opens a PR with newly discovered papers.

---

## 🔗 Related Repositories

- **[business-development](https://github.com/tobias-weiss-ai-xr/business-development)** — open-source framework that consumes this corpus (analyze → understand → evaluate → steer)
- **[ki-kompetenz-training](https://github.com/tobias-weiss-ai-xr/ki-kompetenz-training)** — one downstream application built on this evidence base
- **[graph-research](https://github.com/tobias-weiss-ai-xr/graph-research)** — analogous research corpus
- **[learning-research](https://github.com/tobias-weiss-ai-xr/learning-research)** — analogous research corpus

---

## 📄 License

**© 2026 Tobias Weiss** — released as an open research resource.

- **Research corpus & tools:** MIT License — free to reuse, adapt, and build upon with attribution.

---

## 🙏 Acknowledgments

This corpus synthesizes {total:,} papers across {ymin}-{ymax} into an open,
reusable evidence base for business development research and practice: what the
field studies, how the disciplines connect, and where the literature is heading.

---

**Want to explore what the corpus suggests?**
`cd tools && python3 topic_planner.py`
"""


def main():
    parser = argparse.ArgumentParser(description="Generate README.md")
    parser.add_argument("--check", action="store_true", help="Verify README is current")
    args = parser.parse_args()

    stats_path = BASE / "statistics.json"
    if not stats_path.exists():
        print("ERROR: statistics.json not found — run scripts/analysis/generate_analysis.py first")
        sys.exit(1)

    with open(stats_path, encoding="utf-8") as f:
        stats = json.load(f)

    readme = render_readme(stats)
    readme_path = BASE / "README.md"

    if args.check:
        if readme_path.exists() and readme_path.read_text(encoding="utf-8") == readme:
            print("README.md is up to date")
        else:
            print("README.md is OUT OF DATE — run scripts/generate_readme.py")
            sys.exit(1)
    else:
        readme_path.write_text(readme, encoding="utf-8")
        print(f"Wrote README.md ({len(readme)} chars)")


if __name__ == "__main__":
    main()