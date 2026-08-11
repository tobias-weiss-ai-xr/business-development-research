#!/usr/bin/env python3
"""Generate a ready-to-write article brief for a business development topic.

Pulls the most relevant papers from the corpus (keyword match + recency),
then assembles: title options, angle, outline, key papers and open questions.

Usage:
    python3 tools/brief_generator.py "AI adoption in SMEs" --papers 5
    python3 tools/brief_generator.py "subscription pricing" --json
"""

import argparse
import json
import os
import sys
import re
from collections import Counter

import yaml

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

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

OUTLINE_HOOKS = [
    "Why this matters now",
    "The core concepts, in plain English",
    "What the research says (with paper evidence)",
    "Common pitfalls and misconceptions",
    "Hands-on: a minimal working example",
    "Production considerations (cost, scale, ops)",
    "Where the field is heading",
]


def load_papers():
    with open(os.path.join(BASE, "papers.yaml"), encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return data.get("papers", [])


def tokenize(text):
    return set(re.findall(r"[a-z0-9]{3,}", text.lower()))


def build_brief(topic, papers, n=5):
    q = tokenize(topic)
    if not q:
        q = {"business", "development", "research"}
    scored = []
    for p in papers:
        text = f"{p.get('title', '')} {p.get('abstract', '')}"
        tokens = tokenize(text)
        overlap = len(q & tokens)
        if overlap == 0:
            continue
        # prefer exact phrase matches
        tl = text.lower()
        phrase_bonus = sum(2 for w in topic.lower().split() if len(w) > 3 and w in tl)
        date = p.get("date", "")
        recency = 1 if date >= "2025-01" else 0.5
        scored.append((overlap + phrase_bonus + recency, p))

    scored.sort(key=lambda x: -x[0])
    papers_out = []
    for score, p in scored[:n]:
        papers_out.append(
            {
                "title": p.get("title", ""),
                "date": p.get("date", ""),
                "url": p.get("url", ""),
                "category": p.get("category", ""),
                "subcategory": p.get("subcategory", ""),
                "score": score,
            }
        )

    cats = Counter(p["category"] for p in papers_out)
    dominant_cat = cats.most_common(1)[0][0] if cats else "growth-metrics"
    cat_name = CATEGORY_DISPLAY.get(dominant_cat, dominant_cat)

    title_candidates = [
        f"{topic.title()}: What the Research Says",
        f"{topic.title()} in Production: Lessons from the Literature",
        f"{topic.title()}, Explained for Engineers",
        f"The State of {topic.title()} ({papers_out[0]['date'][:4] if papers_out else '2026'})",
    ]

    return {
        "topic": topic,
        "category": dominant_cat,
        "category_name": cat_name,
        "title_candidates": title_candidates,
        "angle": (
            f"Evidence-based guide to {topic.lower()} — synthesize the {len(papers_out)} "
            f"most relevant papers into practical guidance for ki-kompetenz-training.org readers."
        ),
        "outline": [
            {"section": hook, "notes": f"Cover for topic: {topic}"}
            for hook in OUTLINE_HOOKS
        ],
        "key_papers": papers_out,
        "open_questions": [
            f"What does the newest paper on {topic} get wrong?",
            "Which claims are backed by benchmarks vs. anecdote?",
            "What would a production engineer still struggle with?",
        ],
    }


def main():
    parser = argparse.ArgumentParser(description="Article brief generator")
    parser.add_argument("topic", help="Article topic")
    parser.add_argument("--papers", type=int, default=5, help="Number of key papers")
    parser.add_argument("--json", action="store_true", help="Emit JSON")
    args = parser.parse_args()

    papers = load_papers()
    brief = build_brief(args.topic, papers, n=args.papers)

    if args.json:
        print(json.dumps(brief, indent=2))
        return

    print(f"\n📝 ARTICLE BRIEF: {brief['topic']}")
    print(f"   Category: {brief['category_name']} ({brief['category']})")
    print(f"   Angle: {brief['angle']}\n")

    print("Title candidates:")
    for t in brief["title_candidates"]:
        print(f"  - {t}")

    print("\nOutline:")
    for i, s in enumerate(brief["outline"], 1):
        print(f"  {i}. {s['section']}")

    print(f"\nKey papers ({len(brief['key_papers'])}):")
    for p in brief["key_papers"]:
        print(f"  [{p['date']}] {p['title'][:80]}")
        print(f"           {p['url']}  ({p['category']}/{p['subcategory']})")

    print("\nOpen questions:")
    for q in brief["open_questions"]:
        print(f"  ? {q}")


if __name__ == "__main__":
    main()
