#!/usr/bin/env python3
"""Detect emerging research trends in the business development corpus.

Uses keyword-burst analysis: keywords that appear unusually often in recent
papers (last N months) relative to the whole corpus signal emerging trends.
Also ranks the fastest-growing taxonomy cells.

Usage:
    python3 tools/trend_scanner.py --months 6
    python3 tools/trend_scanner.py --months 12 --json
"""

import argparse
import json
import os
import sys
from collections import Counter
from datetime import datetime

import yaml

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TREND_KEYWORDS = [
    "generative ai", "genai", "llm", "large language model", "chatgpt", "agent",
    "agentic", "ai adoption", "automation", "digital transformation", "sme",
    "small business", "solo", "freelance", "subscription", "saas", "as-a-service",
    "platform", "marketplace", "network effect", "churn", "retention", "acquisition",
    "unit economics", "lifetime value", "cohort", "kpi", "b2b", "lead generation",
    "funnel", "inbound", "content marketing", "seo", "brand", "positioning",
    "pricing", "freemium", "dynamic pricing", "personalization", "recommend",
    "social media", "influencer", "word of mouth", "referral", "partnership",
    "alliance", "negotiation", "persuasion", "behavioral", "nudge", "trust",
    "product-market fit", "mvp", "startup", "venture capital", "benchmark",
    "ab test", "conversion", "customer success", "upsell", "eu ai act",
    "regulation", "ai literacy", "skills", "training", "productivity",
]

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


def load_papers():
    with open(os.path.join(BASE, "papers.yaml"), encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("papers", [])


def scan(papers, months, top=15):
    now = datetime.now()
    cutoff_year = now.year
    cutoff_month = now.month - months
    while cutoff_month <= 0:
        cutoff_year -= 1
        cutoff_month += 12

    def is_recent(date_str):
        try:
            y, m = (int(x) for x in date_str.split("-"))
            return (y, m) >= (cutoff_year, cutoff_month)
        except (ValueError, AttributeError):
            return False

    recent = [p for p in papers if is_recent(p.get("date", ""))]
    recent_n = len(recent)
    total_n = len(papers)

    recent_counter = Counter()
    total_counter = Counter()
    for p in papers:
        text = (p.get("title", "") + " " + p.get("abstract", "")).lower()
        for kw in TREND_KEYWORDS:
            if kw in text:
                total_counter[kw] += 1
                if is_recent(p.get("date", "")):
                    recent_counter[kw] += 1

    # burst score: recent share vs corpus share
    trends = []
    for kw in TREND_KEYWORDS:
        r = recent_counter.get(kw, 0)
        t = total_counter.get(kw, 0)
        if r == 0:
            continue
        corpus_share = t / total_n if total_n else 0
        recent_share = r / recent_n if recent_n else 0
        burst = recent_share / corpus_share if corpus_share > 0 else 99
        trends.append(
            {"keyword": kw, "recent_papers": r, "total_papers": t, "burst_score": round(burst, 1)}
        )
    trends.sort(key=lambda x: (-x["burst_score"], -x["recent_papers"]))

    # fastest growing cells
    cell_total = Counter()
    cell_recent = Counter()
    for p in papers:
        cell = (p.get("category", ""), p.get("subcategory", ""))
        cell_total[cell] += 1
        if is_recent(p.get("date", "")):
            cell_recent[cell] += 1
    growth = []
    for cell, t in cell_total.items():
        r = cell_recent.get(cell, 0)
        if r == 0 or t == 0:
            continue
        growth.append({"cell": f"{cell[0]}/{cell[1]}", "recent": r, "total": t, "recent_share": round(r / t, 2)})
    growth.sort(key=lambda x: -x["recent_share"])

    return {"cutoff": f"{cutoff_year}-{cutoff_month:02d}", "recent_papers": recent_n, "trends": trends[:top], "growing_cells": growth[:top]}


def main():
    parser = argparse.ArgumentParser(description="Business development research trend scanner")
    parser.add_argument("--months", type=int, default=6, help="Look-back window (default: 6)")
    parser.add_argument("--top", type=int, default=15)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    papers = load_papers()
    result = scan(papers, args.months, top=args.top)

    if args.json:
        print(json.dumps(result, indent=2))
        return

    print(f"\n=== Business Development Research Trends (last {args.months} months, since {result['cutoff']}) ===")
    print(f"Recent papers: {result['recent_papers']} of {len(papers)}\n")

    print("🔥 TOP KEYWORD BURSTS (recent share vs corpus share)")
    print("-" * 70)
    for t in result["trends"]:
        bar = "#" * min(40, int(t["burst_score"] * 2))
        print(f"{t['keyword']:<28} {t['recent_papers']:>4} recent / {t['total_papers']:>4} total  burst={t['burst_score']:<5} {bar}")

    print("\n📈 FASTEST-GROWING TAXONOMY CELLS")
    print("-" * 70)
    for g in result["growing_cells"]:
        print(f"{g['cell']:<40} {g['recent']:>3}/{g['total']:<4} ({g['recent_share']*100:.0f}% recent)")


if __name__ == "__main__":
    main()
