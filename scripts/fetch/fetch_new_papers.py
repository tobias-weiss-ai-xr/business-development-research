#!/usr/bin/env python3
"""Discover business development research papers from the arXiv API across all 20 taxonomy categories.

Runs 100+ queries spanning market analysis, sales, marketing, pricing,
customer success, entrepreneurship, AI adoption and all other categories in
the taxonomy. Each query carries a category (and keyword-derived subcategory)
so new papers are auto-classified into the 20x8 taxonomy on discovery.

Usage:
    python3 scripts/fetch/fetch_new_papers.py --months 3 --dry-run
    python3 scripts/fetch/fetch_new_papers.py --months 1 --create-pr
"""

import argparse
import os
import re
import subprocess
import sys
import time
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests
import yaml

ARXIV_ID_PATTERN = re.compile(r"(\d{4}\.\d{4,5})")
ARXIV_SEARCH_API = (
    "https://export.arxiv.org/api/query?search_query={}&start={}&max_results={}"
)

# (query, category, subcategory-hint). Subcategory is refined by keyword scoring
# on title/abstract; the hint is used as a fallback when nothing matches.
QUERIES = [
    ('cat:econ.GN AND abs:"market analysis"', 'market-analysis', 'application'),
    ('cat:econ.GN AND abs:"market research"', 'market-analysis', 'method'),
    ('cat:stat.AP AND abs:"market segmentation"', 'market-analysis', 'method'),
    ('cat:econ.GN AND abs:"market size"', 'market-analysis', 'application'),
    ('cat:econ.GN AND abs:"market structure" AND abs:"industry"', 'market-analysis', 'theory'),
    ('cat:econ.GN AND abs:"customer preferences"', 'market-analysis', 'application'),
    ('cat:stat.AP AND abs:"conjoint analysis"', 'market-analysis', 'method'),
    ('cat:econ.GN AND abs:"market potential"', 'market-analysis', 'application'),
    ('cat:cs.SI AND abs:"market analysis" AND abs:"social"', 'market-analysis', 'application'),
    ('cat:econ.GN AND abs:"survey" AND abs:"market" AND abs:"research"', 'market-analysis', 'review'),
    ('cat:econ.GN AND abs:"go-to-market"', 'go-to-market', 'method'),
    ('cat:econ.GN AND abs:"market entry strategy"', 'go-to-market', 'method'),
    ('cat:econ.GN AND abs:"market entry"', 'go-to-market', 'application'),
    ('cat:econ.GN AND abs:"product launch"', 'go-to-market', 'application'),
    ('cat:econ.GN AND abs:"early adopters"', 'go-to-market', 'mechanism'),
    ('cat:cs.CY AND abs:"technology adoption" AND abs:"firm"', 'go-to-market', 'mechanism'),
    ('cat:econ.GN AND abs:"diffusion" AND abs:"innovation"', 'go-to-market', 'theory'),
    ('cat:physics.soc-ph AND abs:"diffusion" AND abs:"innovation"', 'go-to-market', 'theory'),
    ('cat:econ.GN AND abs:"crossing the chasm"', 'go-to-market', 'theory'),
    ('cat:econ.GN AND abs:"launch strategy"', 'go-to-market', 'method'),
    ('cat:econ.GN AND abs:"sales strategy"', 'sales-strategy', 'method'),
    ('cat:econ.GN AND abs:"sales performance"', 'sales-strategy', 'evaluation'),
    ('cat:cs.CY AND abs:"sales" AND abs:"digital"', 'sales-strategy', 'application'),
    ('cat:econ.GN AND abs:"account management"', 'sales-strategy', 'method'),
    ('cat:econ.GN AND abs:"key account"', 'sales-strategy', 'method'),
    ('cat:cs.CY AND abs:"sales process"', 'sales-strategy', 'method'),
    ('cat:econ.GN AND abs:"sales forecasting"', 'sales-strategy', 'evaluation'),
    ('cat:stat.AP AND abs:"sales forecasting"', 'sales-strategy', 'method'),
    ('cat:q-fin.EC AND abs:"sales" AND abs:"demand"', 'sales-strategy', 'evaluation'),
    ('cat:econ.GN AND abs:"sales management"', 'sales-strategy', 'method'),
    ('cat:econ.GN AND abs:"business-to-business"', 'b2b-marketing', 'application'),
    ('cat:econ.GN AND abs:"B2B marketing"', 'b2b-marketing', 'method'),
    ('cat:cs.CY AND abs:"lead generation"', 'b2b-marketing', 'method'),
    ('cat:cs.SI AND abs:"lead scoring"', 'b2b-marketing', 'method'),
    ('cat:econ.GN AND abs:"industrial marketing"', 'b2b-marketing', 'application'),
    ('cat:cs.CY AND abs:"inbound marketing"', 'b2b-marketing', 'method'),
    ('cat:cs.SI AND abs:"customer acquisition" AND abs:"marketing"', 'b2b-marketing', 'application'),
    ('cat:econ.GN AND abs:"marketing funnel"', 'b2b-marketing', 'method'),
    ('cat:stat.AP AND abs:"customer lifetime value" AND abs:"marketing"', 'b2b-marketing', 'evaluation'),
    ('cat:cs.CY AND abs:"digital marketing" AND abs:"firm"', 'b2b-marketing', 'application'),
    ('cat:cs.CY AND abs:"content marketing"', 'content-marketing', 'method'),
    ('cat:cs.SI AND abs:"content marketing"', 'content-marketing', 'method'),
    ('cat:cs.CL AND abs:"content creation" AND abs:"marketing"', 'content-marketing', 'application'),
    ('cat:cs.SI AND abs:"thought leadership"', 'content-marketing', 'mechanism'),
    ('cat:cs.CY AND abs:"content strategy"', 'content-marketing', 'method'),
    ('cat:cs.IR AND abs:"content recommendation" AND abs:"marketing"', 'content-marketing', 'application'),
    ('cat:cs.CL AND abs:"LLM" AND abs:"content generation"', 'content-marketing', 'application'),
    ('cat:cs.SI AND abs:"influencer marketing"', 'content-marketing', 'application'),
    ('cat:econ.GN AND abs:"advertising" AND abs:"content"', 'content-marketing', 'evaluation'),
    ('cat:cs.CY AND abs:"storytelling" AND abs:"brand"', 'content-marketing', 'mechanism'),
    ('cat:cs.CY AND abs:"digital marketing"', 'digital-marketing', 'method'),
    ('cat:cs.IR AND abs:"search engine optimization"', 'digital-marketing', 'method'),
    ('cat:cs.IR AND abs:"SEO"', 'digital-marketing', 'method'),
    ('cat:econ.GN AND abs:"online advertising"', 'digital-marketing', 'evaluation'),
    ('cat:cs.CY AND abs:"social media marketing"', 'digital-marketing', 'application'),
    ('cat:cs.SI AND abs:"social media" AND abs:"marketing"', 'digital-marketing', 'application'),
    ('cat:econ.GN AND abs:"pay-per-click"', 'digital-marketing', 'evaluation'),
    ('cat:stat.AP AND abs:"advertising effectiveness"', 'digital-marketing', 'evaluation'),
    ('cat:econ.GN AND abs:"display advertising"', 'digital-marketing', 'evaluation'),
    ('cat:cs.IR AND abs:"sponsored search"', 'digital-marketing', 'method'),
    ('cat:econ.GN AND abs:"brand equity"', 'brand-building', 'theory'),
    ('cat:econ.GN AND abs:"branding"', 'brand-building', 'mechanism'),
    ('cat:econ.GN AND abs:"brand loyalty"', 'brand-building', 'mechanism'),
    ('cat:cs.CY AND abs:"brand" AND abs:"online"', 'brand-building', 'application'),
    ('cat:econ.GN AND abs:"brand positioning"', 'brand-building', 'method'),
    ('cat:cs.SI AND abs:"brand" AND abs:"social media"', 'brand-building', 'application'),
    ('cat:econ.GN AND abs:"personal branding"', 'brand-building', 'application'),
    ('cat:cs.CY AND abs:"reputation" AND abs:"online"', 'brand-building', 'mechanism'),
    ('cat:econ.GN AND abs:"brand awareness"', 'brand-building', 'evaluation'),
    ('cat:cs.SI AND abs:"word of mouth"', 'brand-building', 'mechanism'),
    ('cat:econ.GN AND abs:"customer acquisition cost"', 'customer-acquisition', 'evaluation'),
    ('cat:econ.GN AND abs:"customer acquisition"', 'customer-acquisition', 'method'),
    ('cat:cs.CY AND abs:"customer acquisition"', 'customer-acquisition', 'method'),
    ('cat:stat.AP AND abs:"acquisition" AND abs:"customer" AND abs:"model"', 'customer-acquisition', 'method'),
    ('cat:econ.GN AND abs:"referral" AND abs:"customer"', 'customer-acquisition', 'mechanism'),
    ('cat:cs.SI AND abs:"viral" AND abs:"growth"', 'customer-acquisition', 'mechanism'),
    ('cat:econ.GN AND abs:"free trial"', 'customer-acquisition', 'evaluation'),
    ('cat:cs.CY AND abs:"freemium"', 'customer-acquisition', 'method'),
    ('cat:econ.GN AND abs:"cost per acquisition"', 'customer-acquisition', 'evaluation'),
    ('cat:cs.SI AND abs:"growth hacking"', 'customer-acquisition', 'method'),
    ('cat:econ.GN AND abs:"customer retention"', 'customer-retention', 'method'),
    ('cat:econ.GN AND abs:"churn"', 'customer-retention', 'evaluation'),
    ('cat:stat.AP AND abs:"churn prediction"', 'customer-retention', 'method'),
    ('cat:cs.LG AND abs:"churn prediction"', 'customer-retention', 'method'),
    ('cat:econ.GN AND abs:"customer loyalty"', 'customer-retention', 'mechanism'),
    ('cat:econ.GN AND abs:"retention rate"', 'customer-retention', 'evaluation'),
    ('cat:stat.AP AND abs:"survival analysis" AND abs:"customer"', 'customer-retention', 'method'),
    ('cat:cs.CY AND abs:"subscription" AND abs:"retention"', 'customer-retention', 'application'),
    ('cat:econ.GN AND abs:"repeat purchase"', 'customer-retention', 'mechanism'),
    ('cat:cs.LG AND abs:"customer churn"', 'customer-retention', 'application'),
    ('cat:cs.CY AND abs:"customer success"', 'customer-success', 'method'),
    ('cat:econ.GN AND abs:"customer satisfaction"', 'customer-success', 'evaluation'),
    ('cat:econ.GN AND abs:"net promoter score"', 'customer-success', 'evaluation'),
    ('cat:econ.GN AND abs:"customer experience"', 'customer-success', 'mechanism'),
    ('cat:cs.CY AND abs:"customer support" AND abs:"AI"', 'customer-success', 'application'),
    ('cat:econ.GN AND abs:"upselling"', 'customer-success', 'method'),
    ('cat:econ.GN AND abs:"cross-selling"', 'customer-success', 'method'),
    ('cat:stat.AP AND abs:"customer satisfaction" AND abs:"survey"', 'customer-success', 'evaluation'),
    ('cat:cs.CY AND abs:"customer service" AND abs:"chatbot"', 'customer-success', 'application'),
    ('cat:econ.GN AND abs:"service quality"', 'customer-success', 'evaluation'),
    ('cat:econ.GN AND abs:"pricing strategy"', 'pricing-strategy', 'method'),
    ('cat:econ.GN AND abs:"price discrimination"', 'pricing-strategy', 'theory'),
    ('cat:econ.GN AND abs:"subscription pricing"', 'pricing-strategy', 'method'),
    ('cat:q-fin.EC AND abs:"pricing" AND abs:"willingness to pay"', 'pricing-strategy', 'evaluation'),
    ('cat:econ.GN AND abs:"dynamic pricing"', 'pricing-strategy', 'method'),
    ('cat:cs.LG AND abs:"dynamic pricing"', 'pricing-strategy', 'application'),
    ('cat:econ.GN AND abs:"freemium"', 'pricing-strategy', 'method'),
    ('cat:econ.GN AND abs:"value-based pricing"', 'pricing-strategy', 'method'),
    ('cat:q-fin.EC AND abs:"price elasticity"', 'pricing-strategy', 'theory'),
    ('cat:econ.GN AND abs:"monetization"', 'pricing-strategy', 'method'),
    ('cat:econ.GN AND abs:"product-market fit"', 'product-market-fit', 'method'),
    ('cat:cs.CY AND abs:"product-market fit"', 'product-market-fit', 'method'),
    ('cat:econ.GN AND abs:"customer development"', 'product-market-fit', 'method'),
    ('cat:econ.GN AND abs:"minimum viable product"', 'product-market-fit', 'development'),
    ('cat:cs.CY AND abs:"user feedback" AND abs:"product"', 'product-market-fit', 'application'),
    ('cat:econ.GN AND abs:"market validation"', 'product-market-fit', 'method'),
    ('cat:cs.SE AND abs:"user research" AND abs:"product"', 'product-market-fit', 'method'),
    ('cat:econ.GN AND abs:"willingness to pay"', 'product-market-fit', 'evaluation'),
    ('cat:cs.HC AND abs:"user interviews"', 'product-market-fit', 'method'),
    ('cat:econ.GN AND abs:"pilot" AND abs:"customer"', 'product-market-fit', 'application'),
    ('cat:econ.GN AND abs:"business model"', 'business-models', 'theory'),
    ('cat:econ.GN AND abs:"business model innovation"', 'business-models', 'method'),
    ('cat:cs.CY AND abs:"platform business model"', 'business-models', 'theory'),
    ('cat:econ.GN AND abs:"subscription model"', 'business-models', 'method'),
    ('cat:econ.GN AND abs:"two-sided market"', 'business-models', 'theory'),
    ('cat:econ.GN AND abs:"network effects"', 'business-models', 'mechanism'),
    ('cat:cs.SI AND abs:"network effects"', 'business-models', 'mechanism'),
    ('cat:econ.GN AND abs:"software as a service"', 'business-models', 'application'),
    ('cat:econ.GN AND abs:"service-based business"', 'business-models', 'application'),
    ('cat:econ.GN AND abs:"recurring revenue"', 'business-models', 'evaluation'),
    ('cat:econ.GN AND abs:"competitive advantage"', 'competitive-intelligence', 'theory'),
    ('cat:econ.GN AND abs:"competitive strategy"', 'competitive-intelligence', 'theory'),
    ('cat:cs.CY AND abs:"competitive intelligence"', 'competitive-intelligence', 'method'),
    ('cat:cs.CY AND abs:"competitor analysis"', 'competitive-intelligence', 'method'),
    ('cat:econ.GN AND abs:"market positioning"', 'competitive-intelligence', 'method'),
    ('cat:cs.IR AND abs:"competitor" AND abs:"monitoring"', 'competitive-intelligence', 'application'),
    ('cat:econ.GN AND abs:"differentiation strategy"', 'competitive-intelligence', 'method'),
    ('cat:econ.GN AND abs:"industry analysis"', 'competitive-intelligence', 'theory'),
    ('cat:cs.CY AND abs:"benchmarking" AND abs:"firm"', 'competitive-intelligence', 'evaluation'),
    ('cat:econ.GN AND abs:"moat"', 'competitive-intelligence', 'theory'),
    ('cat:econ.GN AND abs:"strategic alliance"', 'partnerships', 'method'),
    ('cat:econ.GN AND abs:"strategic partnership"', 'partnerships', 'method'),
    ('cat:econ.GN AND abs:"joint venture"', 'partnerships', 'method'),
    ('cat:cs.CY AND abs:"ecosystem" AND abs:"partnership"', 'partnerships', 'application'),
    ('cat:econ.GN AND abs:"coopetition"', 'partnerships', 'theory'),
    ('cat:cs.CY AND abs:"affiliate marketing"', 'partnerships', 'method'),
    ('cat:econ.GN AND abs:"channel partner"', 'partnerships', 'method'),
    ('cat:econ.GN AND abs:"co-marketing"', 'partnerships', 'method'),
    ('cat:cs.SI AND abs:"collaboration network" AND abs:"firm"', 'partnerships', 'mechanism'),
    ('cat:econ.GN AND abs:"inter-firm collaboration"', 'partnerships', 'mechanism'),
    ('cat:econ.GN AND abs:"negotiation" AND abs:"bargaining"', 'sales-psychology', 'theory'),
    ('cat:cs.AI AND abs:"negotiation" AND abs:"agent"', 'sales-psychology', 'method'),
    ('cat:econ.GN AND abs:"persuasion" AND abs:"consumer"', 'sales-psychology', 'mechanism'),
    ('cat:cs.CY AND abs:"persuasive technology"', 'sales-psychology', 'mechanism'),
    ('cat:econ.GN AND abs:"behavioral economics" AND abs:"consumer"', 'sales-psychology', 'mechanism'),
    ('cat:econ.GN AND abs:"decision making" AND abs:"purchase"', 'sales-psychology', 'mechanism'),
    ('cat:q-fin.EC AND abs:"prospect theory" AND abs:"consumer"', 'sales-psychology', 'theory'),
    ('cat:cs.CY AND abs:"nudging" AND abs:"consumer"', 'sales-psychology', 'mechanism'),
    ('cat:econ.GN AND abs:"trust" AND abs:"seller"', 'sales-psychology', 'mechanism'),
    ('cat:cs.HC AND abs:"user trust" AND abs:"recommendation"', 'sales-psychology', 'mechanism'),
    ('cat:econ.GN AND abs:"social capital" AND abs:"business"', 'networking', 'theory'),
    ('cat:cs.SI AND abs:"professional network"', 'networking', 'application'),
    ('cat:cs.SI AND abs:"LinkedIn"', 'networking', 'application'),
    ('cat:econ.GN AND abs:"business networking"', 'networking', 'method'),
    ('cat:cs.SI AND abs:"weak ties"', 'networking', 'theory'),
    ('cat:econ.GN AND abs:"social networks" AND abs:"entrepreneur"', 'networking', 'mechanism'),
    ('cat:cs.SI AND abs:"influence" AND abs:"network"', 'networking', 'mechanism'),
    ('cat:econ.GN AND abs:"relationship marketing"', 'networking', 'method'),
    ('cat:physics.soc-ph AND abs:"social network" AND abs:"economic"', 'networking', 'mechanism'),
    ('cat:cs.SI AND abs:"community" AND abs:"professional"', 'networking', 'application'),
    ('cat:econ.GN AND abs:"entrepreneurship"', 'entrepreneurship', 'theory'),
    ('cat:econ.GN AND abs:"startup"', 'entrepreneurship', 'application'),
    ('cat:econ.GN AND abs:"venture capital"', 'entrepreneurship', 'evaluation'),
    ('cat:econ.GN AND abs:"entrepreneurial ecosystem"', 'entrepreneurship', 'mechanism'),
    ('cat:econ.GN AND abs:"small business"', 'entrepreneurship', 'application'),
    ('cat:econ.GN AND abs:"solo entrepreneur"', 'entrepreneurship', 'application'),
    ('cat:econ.GN AND abs:"freelance"', 'entrepreneurship', 'application'),
    ('cat:econ.GN AND abs:"business planning"', 'entrepreneurship', 'method'),
    ('cat:cs.CY AND abs:"indie" AND abs:"business"', 'entrepreneurship', 'application'),
    ('cat:econ.GN AND abs:"startup failure"', 'entrepreneurship', 'evaluation'),
    ('cat:cs.CY AND abs:"key performance indicator"', 'growth-metrics', 'method'),
    ('cat:econ.GN AND abs:"KPI"', 'growth-metrics', 'method'),
    ('cat:econ.GN AND abs:"customer lifetime value"', 'growth-metrics', 'method'),
    ('cat:econ.GN AND abs:"unit economics"', 'growth-metrics', 'method'),
    ('cat:stat.AP AND abs:"cohort analysis"', 'growth-metrics', 'method'),
    ('cat:econ.GN AND abs:"churn rate"', 'growth-metrics', 'evaluation'),
    ('cat:cs.LG AND abs:"conversion prediction"', 'growth-metrics', 'method'),
    ('cat:stat.AP AND abs:"A/B testing" AND abs:"marketing"', 'growth-metrics', 'evaluation'),
    ('cat:cs.CY AND abs:"growth metrics"', 'growth-metrics', 'method'),
    ('cat:econ.GN AND abs:"return on investment" AND abs:"marketing"', 'growth-metrics', 'evaluation'),
    ('cat:econ.GN AND abs:"artificial intelligence" AND abs:"adoption"', 'ai-adoption', 'mechanism'),
    ('cat:cs.CY AND abs:"AI adoption" AND abs:"firm"', 'ai-adoption', 'application'),
    ('cat:econ.GN AND abs:"AI" AND abs:"productivity" AND abs:"firm"', 'ai-adoption', 'evaluation'),
    ('cat:econ.GN AND abs:"artificial intelligence" AND abs:"labor market"', 'ai-adoption', 'evaluation'),
    ('cat:cs.CY AND abs:"AI literacy"', 'ai-adoption', 'method'),
    ('cat:econ.GN AND abs:"generative AI" AND abs:"business"', 'ai-adoption', 'application'),
    ('cat:cs.CY AND abs:"large language model" AND abs:"enterprise"', 'ai-adoption', 'application'),
    ('cat:econ.GN AND abs:"digital transformation"', 'ai-adoption', 'mechanism'),
    ('cat:cs.CY AND abs:"digital transformation" AND abs:"SME"', 'ai-adoption', 'application'),
    ('cat:econ.GN AND abs:"automation" AND abs:"firms"', 'ai-adoption', 'evaluation'),
    ('cat:econ.GN AND abs:"brand" AND abs:"survey"', 'brand-building', 'review'),
    ('cat:econ.GN AND abs:"pricing" AND abs:"survey"', 'pricing-strategy', 'review'),
    ('cat:econ.GN AND abs:"business model" AND abs:"survey"', 'business-models', 'review'),
    ('cat:econ.GN AND abs:"sales" AND abs:"survey"', 'sales-strategy', 'review'),
    ('cat:cs.CY AND abs:"AI adoption" AND abs:"survey"', 'ai-adoption', 'review'),
    ('cat:econ.GN AND abs:"marketing" AND abs:"survey"', 'b2b-marketing', 'review'),
    ('cat:econ.GN AND abs:"digital transformation" AND abs:"survey"', 'ai-adoption', 'review'),
    ('cat:econ.GN AND abs:"customer" AND abs:"retention" AND abs:"survey"', 'customer-retention', 'review'),
    ('cat:econ.GN AND abs:"entrepreneurship" AND abs:"survey"', 'entrepreneurship', 'review'),
    ('cat:econ.GN AND abs:"adoption" AND abs:"technology" AND abs:"survey"', 'go-to-market', 'review'),
    ('cat:econ.GN AND abs:"artificial intelligence" AND abs:"review"', 'ai-adoption', 'review'),
    ('cat:q-fin.GN AND abs:"market" AND abs:"analysis" AND abs:"survey"', 'market-analysis', 'review'),
    ('cat:econ.GN AND abs:"social media" AND abs:"firm" AND abs:"survey"', 'digital-marketing', 'review'),
    ('cat:econ.GN AND abs:"customer experience" AND abs:"survey"', 'customer-success', 'review'),
    ('cat:econ.GN AND abs:"startup" AND abs:"review"', 'entrepreneurship', 'review'),
]

# Subcategory keyword rules, applied in order. First match wins.
# Each rule: (subcategory, keywords, title_only?) — title_only restricts
# matching to the paper title (for strong signals like "survey").
SUBCATEGORY_RULES = [
    ("review", ["survey", "systematic review", "state-of-the-art", "sota", "overview of"], True),
    ("review", ["a survey of", "review of", "bibliographic review"], False),
    ("theory", ["expressivity", "expressiveness", "theoretical", "complexity of", "bounds", "fundamental limits", "axiomat", "computational complexity", "approximation guarantees"], False),
    ("application", ["application to", "application of", "case study", "real-world", "in practice", "production", "clinical", "medical", "fraud detection", "drug discovery", "recommender", "supply chain", "bioinformatics", "proteomics", "genomics", "diagnosis", "osint", "cybersecurity", "deployment"], False),
    ("development", ["open-source", "library", "toolkit", "implementation of", "software package", "benchmarking tool", "api for", "python library"], False),
    ("mechanism", ["interpretab", "explainab", "understanding why", "analysis of", "inner workings", "attention analysis", "probing", "mechanism", "why graph"], False),
    ("systems", ["system", "engine", "platform", "infrastructure", "architecture", "pipeline", "distributed", "scalable", "indexing", "storage", "gpu", "parallel"], False),
    ("evaluation", ["benchmark", "empirical study", "empirical comparison", "experimental evaluation", "evaluating", "comparative analysis", "dataset"], False),
]

SUBCATEGORY_FALLBACK = "method"


def classify_subcategory(title, abstract):
    """Assign a subcategory using keyword rules against title + abstract."""
    t_lower = title.lower()
    text = f"{title} {abstract}".lower()
    for subcat, keywords, title_only in SUBCATEGORY_RULES:
        haystack = t_lower if title_only else text
        for kw in keywords:
            if kw in haystack:
                return subcat
    return SUBCATEGORY_FALLBACK


def load_existing_papers(yaml_path):
    if not yaml_path.exists():
        return {}, []
    with open(yaml_path, "r") as f:
        data = yaml.safe_load(f) or {}
    papers = data.get("papers", [])
    by_id = {}
    titles_lower = []
    for p in papers:
        url = p.get("url", "")
        match = ARXIV_ID_PATTERN.search(url)
        if match:
            by_id[match.group(1)] = p
        titles_lower.append(p.get("title", "").lower().strip())
    return by_id, titles_lower


def search_arxiv(query, months, start=0, max_results=100, max_retries=4):
    now = datetime.now(timezone.utc).replace(tzinfo=None)
    cutoff = now - timedelta(days=months * 30)
    date_start = cutoff.strftime("%Y%m%d0000")
    date_end = now.strftime("%Y%m%d") + "2359"

    full_query = f"({query}) AND submittedDate:[{date_start} TO {date_end}]"
    try:
        resp = None
        for attempt in range(max_retries):
            resp = requests.get(
                ARXIV_SEARCH_API.format(
                    requests.utils.quote(full_query), start, max_results
                ),
                timeout=30,
            )
            if resp.status_code == 429:
                wait = 8 * (attempt + 1)
                print(f"    rate-limited (429), waiting {wait}s...", flush=True)
                time.sleep(wait)
                continue
            resp.raise_for_status()
            break
        if resp is None:
            return []
        if resp.status_code != 200:
            print(f"  WARNING: arXiv returned HTTP {resp.status_code}", flush=True)
            return []
        entries = []
        root = resp.text
        for match in re.finditer(r"<entry>(.*?)</entry>", root, re.DOTALL):
            entry_xml = match.group(1)
            entry = {}
            title_m = re.search(r"<title>(.*?)</title>", entry_xml, re.DOTALL)
            if title_m:
                entry["title"] = re.sub(r"\s+", " ", title_m.group(1).strip())
            id_m = re.search(r"<id>(.*?)</id>", entry_xml)
            if id_m:
                entry["url"] = id_m.group(1).strip().replace("http://", "https://")
            published_m = re.search(r"<published>(.*?)</published>", entry_xml)
            if published_m:
                entry["date"] = published_m.group(1).strip()[:7]
            summary_m = re.search(r"<summary>(.*?)</summary>", entry_xml, re.DOTALL)
            if summary_m:
                entry["abstract"] = re.sub(r"\s+", " ", summary_m.group(1).strip())
            authors_m = re.findall(r"<name>(.*?)</name>", entry_xml)
            if authors_m:
                entry["authors"] = [a.strip() for a in authors_m][:3]
            if entry.get("title") and entry.get("url"):
                entries.append(entry)
        return entries
    except Exception as e:
        print(f"  WARNING: arXiv search error: {e}", flush=True)
        return []


def format_yaml_entry(entry, category, subcategory):
    title = entry["title"].replace('"', '\\"')
    authors = ", ".join(entry.get("authors", [])[:3])
    lines = [
        f'  - title: "{title}"',
        f'    date: "{entry.get("date", "")}"',
        f'    url: "{entry.get("url", "")}"',
        f"    category: {category}",
        f"    subcategory: {subcategory}",
        f"    authors: [{authors}]",
    ]
    if entry.get("abstract"):
        abstract = entry["abstract"][:200].replace('"', '\\"')
        lines.append(f'    abstract: "{abstract}..."')
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(
        description="Discover business development research papers from arXiv"
    )
    parser.add_argument(
        "--months",
        type=int,
        default=3,
        help="Search papers from the last N months (default: 3)",
    )
    parser.add_argument(
        "--dry-run", action="store_true", help="Preview without creating anything"
    )
    parser.add_argument(
        "--create-pr", action="store_true", help="Create a GitHub PR with new papers"
    )
    parser.add_argument(
        "--sleep", type=float, default=2.0, help="Seconds between queries"
    )
    parser.add_argument(
        "--max-results",
        type=int,
        default=100,
        help="Max results per arXiv query (default: 100)",
    )
    parser.add_argument(
        "--from",
        dest="from_idx",
        type=int,
        default=0,
        help="Start at query index (0-based, inclusive)",
    )
    parser.add_argument(
        "--to",
        dest="to_idx",
        type=int,
        default=None,
        help="Stop at query index (0-based, inclusive)",
    )
    args = parser.parse_args()

    yaml_path = Path(__file__).resolve().parent.parent.parent / "papers.yaml"
    by_id, titles_lower = load_existing_papers(yaml_path)

    print(f"Loaded {len(by_id)} existing papers from papers.yaml", flush=True)
    print(
        f"Searching arXiv ({len(QUERIES)} queries) for papers from the last {args.months} month(s)...",
        flush=True,
    )

    all_new = []
    CHECKPOINT_EVERY = 10
    to_idx = args.to_idx if args.to_idx is not None else len(QUERIES) - 1
    for qi, qdef in enumerate(QUERIES[args.from_idx:to_idx + 1], start=args.from_idx):
        if len(qdef) == 4:
            query, category, hint, force_sub = qdef
        else:
            query, category, hint = qdef
            force_sub = None
        print(f"Query {qi + 1}/{len(QUERIES)} [{category}] {query[:70]}", flush=True)
        entries = search_arxiv(query, args.months, max_results=args.max_results)
        for entry in entries:
            arxiv_id_match = ARXIV_ID_PATTERN.search(entry.get("url", ""))
            arxiv_id = arxiv_id_match.group(1) if arxiv_id_match else None

            if arxiv_id and arxiv_id in by_id:
                continue

            title_lower = entry.get("title", "").lower().strip()
            if any(title_lower == t for t in titles_lower):
                continue

            if arxiv_id and any(e.get("url", "") == entry["url"] for e in all_new):
                continue

            entry["category"] = category
            entry["subcategory"] = force_sub or classify_subcategory(
                entry.get("title", ""), entry.get("abstract", "")
            )
            all_new.append(entry)
            by_id[arxiv_id] = entry
            titles_lower.append(title_lower)

        # Incremental checkpoint so partial runs are never lost
        if not args.dry_run and all_new and (qi + 1) % CHECKPOINT_EVERY == 0:
            append_papers(yaml_path, all_new)
            print(f"  [checkpoint] saved {len(all_new)} papers so far", flush=True)
            all_new = []
            by_id, titles_lower = load_existing_papers(yaml_path)

        time.sleep(args.sleep)

    print(
        f"\nFound {len(all_new)} new papers ({len(by_id)} already in list)", flush=True
    )

    if not all_new:
        print("No new papers to add.", flush=True)
        return

    print("\n--- New Papers (first 10) ---", flush=True)
    for entry in all_new[:10]:
        print(format_yaml_entry(entry, entry["category"], entry["subcategory"]), flush=True)
        print(flush=True)
    print(f"... and {max(0, len(all_new) - 10)} more", flush=True)

    if args.dry_run:
        print("\nDry run complete — no files modified", flush=True)
        return

    if args.create_pr:
        branch_name = f"add-new-papers-{datetime.now().strftime('%Y%m%d')}"
        print(f"\nCreating branch '{branch_name}' and PR...", flush=True)
        try:
            subprocess.run(
                ["git", "checkout", "-b", branch_name], check=True, cwd=yaml_path.parent
            )
            append_papers(yaml_path, all_new)
            subprocess.run(["git", "add", "papers.yaml"], check=True, cwd=yaml_path.parent)
            subprocess.run(
                ["git", "commit", "-m", f"Add {len(all_new)} new papers from arXiv discovery"],
                check=True,
                cwd=yaml_path.parent,
            )
            subprocess.run(
                ["git", "push", "origin", branch_name], check=True, cwd=yaml_path.parent
            )
            subprocess.run(
                [
                    "gh", "pr", "create",
                    "--title", f"Add {len(all_new)} new papers from arXiv discovery",
                    "--body", "Automatically discovered papers.\n\n**Please review taxonomy assignments.**",
                ],
                check=True,
                cwd=yaml_path.parent,
            )
            print("PR created successfully!", flush=True)
        except subprocess.CalledProcessError as e:
            print(f"ERROR: Failed to create PR: {e}", flush=True)
            sys.exit(1)
    else:
        append_papers(yaml_path, all_new)
        print(f"\nAppended {len(all_new)} papers to papers.yaml", flush=True)
        print(
            "\nNext: run scripts/analysis/generate_analysis.py and scripts/generate_readme.py",
            flush=True,
        )


def append_papers(yaml_path, new_papers):
    """Append new papers to papers.yaml in stable format."""
    if yaml_path.exists():
        with open(yaml_path, "r") as f:
            data = yaml.safe_load(f) or {}
    else:
        data = {}
    papers = data.get("papers", [])
    for entry in new_papers:
        papers.append(
            {
                "title": entry.get("title", ""),
                "date": entry.get("date", ""),
                "url": entry.get("url", ""),
                "category": entry.get("category", ""),
                "subcategory": entry.get("subcategory", ""),
                "authors": entry.get("authors", []),
                "abstract": entry.get("abstract", ""),
            }
        )
    data["papers"] = papers
    with open(yaml_path, "w") as f:
        yaml.dump(
            data, f, default_flow_style=False, allow_unicode=True, sort_keys=False
        )


if __name__ == "__main__":
    main()
