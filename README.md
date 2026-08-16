# Business Development Research Corpus

**Evidence base for KI-Kompetenz-Training** — Analysis of 5,287 research papers across 20 business development disciplines.

**Author:** Tobias Weiss
**Contact:** ki-kompetenz-training@tobias-weiss.org
**Website:** [ki-kompetenz-training.org](https://www.ki-kompetenz-training.org)

---

## 🎯 Overview

This repository contains the research corpus and tooling for growing
KI-Kompetenz-Training: market analysis, go-to-market, sales, B2B marketing,
pricing, customer success, entrepreneurship, AI adoption and every adjacent
business development discipline. It mirrors the structure of the
[graph-research](https://github.com/tobias-weiss-ai-xr/graph-research) and
[learning-research](https://github.com/tobias-weiss-ai-xr/learning-research)
corpora and feeds evidence-based topics into the content pipeline
(blog, newsletter, landing pages, ALaaS offer design).

### Research Scope

| Metric | Value |
|--------|-------|
| **Papers Analyzed** | 5,287 |
| **Business Development Disciplines** | 20 |
| **Time Span** | 2021-2026 |
| **Research Aspects** | 8 |
| **Taxonomy Cells** | 160 |
| **Saturation** | 100.0% (160/160 cells) |

### Top Evidence Areas

1. **Digital Marketing & SEO** — 394 papers
2. **Market Analysis & Research** — 384 papers
3. **AI Adoption & Transformation** — 380 papers
4. **Go-to-Market Strategy** — 359 papers
5. **Content Marketing & Thought Leadership** — 339 papers
6. **Pricing & Monetization** — 292 papers

---

## 📊 The 20-Category Taxonomy

| Category | Papers |
|----------|--------|
| Market Analysis & Research | 384 |
| Go-to-Market Strategy | 359 |
| Sales Strategy & Process | 265 |
| B2B Marketing & Lead Gen | 232 |
| Content Marketing & Thought Leadership | 339 |
| Digital Marketing & SEO | 394 |
| Brand & Positioning | 262 |
| Customer Acquisition & Growth | 203 |
| Customer Retention & Churn | 197 |
| Customer Success & Expansion | 208 |
| Pricing & Monetization | 292 |
| Product-Market Fit & Validation | 247 |
| Business Models & Innovation | 253 |
| Competitive Intelligence | 202 |
| Partnerships & Alliances | 205 |
| Sales Psychology & Negotiation | 235 |
| Networking & Relationships | 195 |
| Entrepreneurship & Small Business | 228 |
| Growth Metrics & Analytics | 207 |
| AI Adoption & Transformation | 380 |

### Research Aspects (Subcategories)

| Aspect | Papers |
|--------|--------|
| Theory | 546 |
| Mechanism | 618 |
| Method | 1844 |
| Application | 871 |
| Development | 95 |
| Systems & Technology | 877 |
| Evaluation & Benchmarks | 152 |
| Reviews & Surveys | 284 |

---

## 🚀 Emerging Themes (Last 12 Months)

1. **agentic** — 23 papers
2. **solo** — 3 papers
3. **eu ai act** — 3 papers
4. **saas** — 7 papers
5. **lead generation** — 18 papers
6. **literacy** — 30 papers

## 📈 Category Momentum (Last 12 Months)

Ranked by output density × year-over-year growth — the strongest leading indicator for what to cover next:

| Category | Total | Last 12m | Growth | 12-m share |
|----------|------:|---------:|-------:|-----------:|
| B2B Marketing & Lead Gen | 232 | 185 | +825.0% | 80% |
| Market Analysis & Research | 384 | 143 | +376.7% | 37% |
| Digital Marketing & SEO | 394 | 127 | +262.9% | 32% |
| Go-to-Market Strategy | 359 | 147 | +162.5% | 41% |
| Sales Psychology & Negotiation | 235 | 119 | +138.0% | 51% |
| Content Marketing & Thought Leadership | 339 | 98 | +145.0% | 29% |

---

## 🕳️ Research Gaps (Thinnest Cells)

Cells with the fewest papers are prime opportunities for content and offer design:

- `partnerships/development` — 1 papers
- `pricing-strategy/development` — 1 papers
- `b2b-marketing/development` — 2 papers
- `customer-success/evaluation` — 2 papers
- `business-models/evaluation` — 2 papers
- `partnerships/evaluation` — 2 papers
- `sales-psychology/development` — 2 papers
- `customer-acquisition/evaluation` — 3 papers

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

Generate evidence-based content topics for ki-kompetenz-training.org from the corpus.

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

- **Framework (uses this corpus):** [business-development](https://github.com/tobias-weiss-ai-xr/business-development) — open-source playbook to hone business ideas (analyze → understand → evaluate → steer); every method links to this evidence base
- **Content site:** [ki-kompetenz-training](https://github.com/tobias-weiss-ai-xr/ki-kompetenz-training) — KI-Kompetenz-Training
- **Analogous corpus:** [graph-research](https://github.com/tobias-weiss-ai-xr/graph-research)
- **Analogous corpus:** [learning-research](https://github.com/tobias-weiss-ai-xr/learning-research)

---

## 📄 License

**© 2026 KI-Kompetenz-Training | Tobias Weiss**

- **Research corpus:** Proprietary
- **Tools:** MIT License

---

## 🙏 Acknowledgments

This corpus synthesizes 5,287 papers across 2021-2026 to create a
comprehensive evidence base for business development decisions: what to write,
what to offer, how to price, and where the market is heading.

---

**Want to turn this corpus into content?**
`cd tools && python3 topic_planner.py`
