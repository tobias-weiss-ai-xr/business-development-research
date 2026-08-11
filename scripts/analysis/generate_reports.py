#!/usr/bin/env python3
"""Generate research reports from the corpus:
  - docs/research/literature_review.md    (synthesis + top papers per category)
  - docs/research/bizdev_trends_2026.md   (trend report from trend scanner)

Usage:
    python3 scripts/analysis/generate_reports.py
"""

import json
import os
import sys
from collections import Counter, defaultdict
from datetime import datetime

import yaml

sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), "tools"))
from trend_scanner import scan as scan_trends  # noqa: E402

BASE = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, BASE)

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

KEY_INSIGHTS = {
    "market-analysis": (
        "Market analysis research centers on segmentation, sizing and preference "
        "measurement (conjoint, willingness-to-pay); survey-based studies remain "
        "the dominant method, with ML-driven segmentation emerging."
    ),
    "go-to-market": (
        "Go-to-market research is driven by adoption/diffusion theory: early "
        "adopters, technology acceptance and launch timing. For digital services "
        "the evidence favors narrow beachhead segments and measurable pilots."
    ),
    "sales-strategy": (
        "Sales research covers forecasting, performance and account management. "
        "Recent work increasingly models sales processes with ML — a gap between "
        "academic forecasting and practitioner playbooks."
    ),
    "b2b-marketing": (
        "B2B marketing research clusters around lead generation, funnels and "
        "customer acquisition. Evidence-based content is repeatedly shown to be "
        "the highest-leverage tactic for small firms with limited budgets."
    ),
    "content-marketing": (
        "Content marketing research overlaps with influence and trust literature: "
        "thought leadership works via perceived expertise, and LLM-generated "
        "content is the fastest-growing application trend."
    ),
    "digital-marketing": (
        "Digital marketing research spans SEO, paid acquisition and social media. "
        "Effectiveness measurement (incrementality, A/B testing) is the recurring "
        "methodological theme."
    ),
    "brand-building": (
        "Brand research is anchored in brand equity and loyalty theory; online "
        "reputation and word-of-mouth are the fastest-growing application areas "
        "for small businesses and solo operators."
    ),
    "customer-acquisition": (
        "Acquisition research quantifies CAC, referral mechanics and viral growth. "
        "Free-trial and freemium evidence shows conversion depends on activation "
        "speed more than feature depth."
    ),
    "customer-retention": (
        "Retention and churn research is highly quantitative: survival models, "
        "churn prediction and subscription analytics dominate. The evidence base "
        "for recurring-revenue businesses is strong and actionable."
    ),
    "customer-success": (
        "Customer success research connects satisfaction, NPS and expansion "
        "revenue; AI support automation (chatbots, copilots) is the emerging "
        "application frontier."
    ),
    "pricing-strategy": (
        "Pricing research spans price discrimination, dynamic pricing and "
        "subscription models. Value-based and tiered pricing have the strongest "
        "evidence for B2B services; willingness-to-pay measurement is the key tool."
    ),
    "product-market-fit": (
        "PMF research overlaps with customer development and lean startup "
        "methods: MVP testing, user interviews and pilot evidence. The academic "
        "base is thinner than practitioner practice — a genuine research gap."
    ),
    "business-models": (
        "Business model research covers platform economics, network effects and "
        "subscription innovations. Two-sided market theory is the strongest "
        "theoretical anchor; AI-as-a-service models are the emerging cell."
    ),
    "competitive-intelligence": (
        "Competitive intelligence research is grounded in competitive advantage "
        "theory (Porter) plus modern monitoring methods. Differentiation and "
        "positioning evidence for small firms favors focus strategies."
    ),
    "partnerships": (
        "Partnership research covers alliances, joint ventures and ecosystems. "
        "Coopetition and channel strategy are active themes; affiliate and "
        "co-marketing evidence is directly actionable for solo operators."
    ),
    "sales-psychology": (
        "Sales psychology draws on behavioral economics: persuasion, trust, "
        "nudging and prospect theory. The evidence strongly supports the EU AI "
        "Act's push for transparency — trust is a measurable conversion factor."
    ),
    "networking": (
        "Networking research applies social capital and weak-tie theory to "
        "business outcomes. Professional networks and online communities are "
        "the dominant application; relationship marketing links it to revenue."
    ),
    "entrepreneurship": (
        "Entrepreneurship research covers startups, venture capital and small "
        "business economics. Solo/indie operation is an emerging cell with thin "
        "academic coverage — white space for evidence-driven content."
    ),
    "growth-metrics": (
        "Growth metrics research is measurement-heavy: unit economics, LTV, "
        "cohort analysis and A/B testing. The evidence base for subscription "
        "SaaS metrics is mature and directly transferable to training businesses."
    ),
    "ai-adoption": (
        "AI adoption is the fastest-moving category: firm-level productivity "
        "studies, AI literacy, EU AI Act compliance and digital transformation "
        "of SMEs. This is the core evidence base for KI-Kompetenz-Training's "
        "ALaaS positioning."
    ),
}


def render_literature_review(papers, now, stats=None):
    total = len(papers)
    lines = [
        "# Business Development Research — Literature Review",
        "",
        f"**Generated:** {now}  ",
        f"**Corpus:** {total:,} papers across {len(CATEGORY_DISPLAY)} categories",
        "",
        "> Synthesis of the business development research corpus. Category "
        "insights are drawn from title/abstract analysis of the papers themselves.",
        "",
        "---",
        "",
        "## Corpus Overview",
        "",
    ]
    cat_counter = Counter(p.get("category", "unknown") for p in papers)
    sub_counter = Counter(p.get("subcategory", "unknown") for p in papers)
    year_counter = Counter(p.get("date", "")[:4] for p in papers if p.get("date"))
    top_cats = sorted(cat_counter.items(), key=lambda kv: -kv[1])[:5]

    lines.append("| Rank | Category | Papers |")
    lines.append("|------|----------|--------|")
    for i, (c, n) in enumerate(top_cats, 1):
        lines.append(f"| {i} | {CATEGORY_DISPLAY.get(c, c)} | {n} |")

    years = sorted(y for y in year_counter if y)
    lines += [
        "",
        f"**Time span:** {years[0]}–{years[-1]} (median year {years[len(years)//2] if years else '—'})",
        f"**Dominant aspects:** {', '.join(f'{SUBCATEGORY_DISPLAY.get(s, s)} ({n})' for s, n in sub_counter.most_common(3))}",
        "",
        "---",
        "",
    ]

    # ---- enhanced sections drawn from statistics.json ----
    if isinstance(stats, dict):
        mom = stats.get("momentum", [])
        if mom:
            lines += [
                "## 📈 Research Momentum (Last 12 Months)",
                "",
                "Categories ranked by a momentum score combining recent output "
                "density with year-over-year growth.",
                "",
                "| Category | Total | Last 12m | Prior 12m | Growth | 12-m share | Papers/mo |",
                "|----------|------:|---------:|----------:|-------:|----------:|----------:|",
            ]
            for m in mom:
                g = f"{m['growth_pct']:+}%" if m['growth_pct'] is not None else "—"
                lines.append(
                    f"| {m['name']} | {m['total']} | {m['recent']} | {m['prior']} | {g} | "
                    f"{m['recent_share']*100:.0f}% | {m['papers_per_month']} |"
                )
            lines += ["", "---", ""]

        gaps = stats.get("gaps", {})
        if gaps:
            lines += ["## 🕳️ Research Gaps & White Space", ""]
            thinnest = gaps.get("thinnest_cells", [])[:8]
            if thinnest:
                lines += ["**Thinnest taxonomy cells:**", "", "| Cell | Papers |", "|------|--------|"]
                for g in thinnest:
                    lines.append(f"| `{g['cell']}` | {g['papers']} |")
                lines.append("")
            ws = gaps.get("white_space", [])[:8]
            if ws:
                lines += [
                    "**White-space cells** (low total but fast-growing):", "",
                    "| Cell | Total | Last-12m | 12-m share |",
                    "|------|-------:|---------:|-----------:|",
                ]
                for w in ws:
                    lines.append(f"| `{w['cell']}` | {w['total']} | {w['recent']} | {w['recent_share']*100:.0f}% |")
                lines.append("")
            lines += ["---", ""]

        if stats.get("venues"):
            lines += [
                "## Publishing Venues", "",
                "Top venues by paper count (where present in the metadata):", "",
                "| Venue | Papers |", "|-------|--------|",
            ]
            for v in stats["venues"][:10]:
                lines.append(f"| {v['name']} | {v['papers']} |")
            lines += ["", "---", ""]

    lines += ["", "## Category Insights", ""]
    for c in sorted(cat_counter, key=lambda c: -cat_counter[c]):
        if cat_counter[c] == 0:
            continue
        insight = KEY_INSIGHTS.get(c, "Category is still saturating — see `statistics.json` for cell counts.")
        # top recent papers
        cat_papers = [p for p in papers if p.get("category") == c and p.get("date", "") >= "2025-01"]
        cat_papers.sort(key=lambda p: p.get("date", ""), reverse=True)
        top3 = cat_papers[:3]
        lines += [
            f"### {CATEGORY_DISPLAY.get(c, c)} (`{c}`)",
            "",
            f"{insight}",
            "",
            f"**Corpus size:** {cat_counter[c]} papers",
        ]
        if top3:
            lines += ["", "**Recent papers:**", ""]
            for p in top3:
                lines.append(f"- [{p['date']}] {p['title'][:100]} — {p.get('url', '')}")
        lines.append("")
        lines.append("---")
        lines.append("")

    lines += [
        "## Methodology",
        "",
        "1. Papers are discovered via taxonomy-aware arXiv queries and "
        "auto-classified into the 20×8 taxonomy.",
        "2. Category insights above are editorially curated but grounded in "
        "corpus statistics.",
        "3. Regenerate this document with `scripts/analysis/generate_reports.py`.",
        "",
    ]
    return "\n".join(lines)


def render_trend_report(papers, now, stats=None):
    result = scan_trends(papers, months=12, top=15)
    lines = [
        "# Business Development Research Trends (12-Month View)",
        "",
        f"**Generated:** {now}  ",
        f"**Window:** since {result['cutoff']} — {result['recent_papers']} of {len(papers)} papers",
        "",
        "## 🔥 Keyword Bursts",
        "",
        "| Keyword | Recent | Total | Burst |",
        "|---------|--------|-------|-------|",
    ]
    for t in result["trends"]:
        lines.append(f"| {t['keyword']} | {t['recent_papers']} | {t['total_papers']} | {t['burst_score']}× |")

    lines += [
        "",
        "## 📈 Fastest-Growing Cells",
        "",
        "| Cell | Recent | Total | Recent Share |",
        "|------|--------|-------|--------------|",
    ]
    for g in result["growing_cells"]:
        lines.append(f"| `{g['cell']}` | {g['recent']} | {g['total']} | {g['recent_share']*100:.0f}% |")

    lines += [
        "",
        "## What This Means for KI-Kompetenz-Training",
        "",
        "- Categories with high burst scores are the safest content bets "
        "(reader interest follows research momentum) for the blog and newsletter.",
        "- Fast-growing cells with few total papers are white-space opportunities: "
        "early coverage builds topical authority for ALaaS positioning.",
        "- Thin cells in `statistics.json` mark research gaps where evidence is "
        "thin — write with appropriate caution.",
        "",
        "Regenerate with `python3 tools/trend_scanner.py --months 12`.",
        "",
    ]
    return "\n".join(lines)


def main():
    with open(os.path.join(BASE, "papers.yaml"), encoding="utf-8") as f:
        data = yaml.safe_load(f)
    papers = data.get("papers", [])
    now = datetime.now().isoformat()[:10]

    lit_path = os.path.join(BASE, "docs", "research", "literature_review.md")
    stats_path = os.path.join(BASE, "statistics.json")
    stats = None
    if os.path.exists(stats_path):
        with open(stats_path, encoding="utf-8") as f:
            stats = json.load(f)

    with open(lit_path, "w", encoding="utf-8") as f:
        f.write(render_literature_review(papers, now, stats))
    print(f"Wrote {lit_path}")

    trend_path = os.path.join(BASE, "docs", "research", "bizdev_trends_2026.md")
    with open(trend_path, "w", encoding="utf-8") as f:
        f.write(render_trend_report(papers, now, stats))
    print(f"Wrote {trend_path}")


if __name__ == "__main__":
    main()
