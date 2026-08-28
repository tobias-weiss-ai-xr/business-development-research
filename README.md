# Business Development Research Corpus

**An open research corpus for business development** — Analysis of 6,449 research papers across 20 business development disciplines.

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
| **Papers Analyzed** | 6,449 |
| **Business Development Disciplines** | 20 |
| **Time Span** | 2021-2026 |
| **Research Aspects** | 8 |
| **Taxonomy Cells** | 160 |
| **Saturation** | 100.0% (160/160 cells) |

### Top Evidence Areas

1. **AI Adoption & Transformation** — 778 papers
2. **Digital Marketing & SEO** — 469 papers
3. **Pricing & Monetization** — 402 papers
4. **Market Analysis & Research** — 384 papers
5. **Content Marketing & Thought Leadership** — 380 papers
6. **Go-to-Market Strategy** — 359 papers

---

## 📊 The 20-Category Taxonomy

| Category | Papers |
|----------|--------|
| Market Analysis & Research | 384 |
| Go-to-Market Strategy | 359 |
| Sales Strategy & Process | 265 |
| B2B Marketing & Lead Gen | 244 |
| Content Marketing & Thought Leadership | 380 |
| Digital Marketing & SEO | 469 |
| Brand & Positioning | 266 |
| Customer Acquisition & Growth | 273 |
| Customer Retention & Churn | 277 |
| Customer Success & Expansion | 208 |
| Pricing & Monetization | 402 |
| Product-Market Fit & Validation | 252 |
| Business Models & Innovation | 253 |
| Competitive Intelligence | 287 |
| Partnerships & Alliances | 205 |
| Sales Psychology & Negotiation | 323 |
| Networking & Relationships | 304 |
| Entrepreneurship & Small Business | 313 |
| Growth Metrics & Analytics | 207 |
| AI Adoption & Transformation | 778 |

### Research Aspects (Subcategories)

| Aspect | Papers |
|--------|--------|
| Theory | 652 |
| Mechanism | 791 |
| Method | 2044 |
| Application | 1133 |
| Development | 110 |
| Systems & Technology | 1184 |
| Evaluation & Benchmarks | 216 |
| Reviews & Surveys | 319 |

---

## 🚀 Emerging Themes (Last 12 Months)

1. **literacy** — 114 papers
2. **workforce** — 48 papers
3. **solo** — 4 papers
4. **language** — 359 papers
5. **compliance** — 48 papers
6. **generative** — 209 papers

## 📈 Category Momentum (Last 12 Months)

Ranked by output density × year-over-year growth — the strongest leading indicator for what to cover next:

| Category | Total | Last 12m | Growth | 12-m share |
|----------|------:|---------:|-------:|-----------:|
| B2B Marketing | 244 | 197 | +885.0% | 81% |
| Digital Marketing | 469 | 202 | +477.1% | 43% |
| Ai Adoption | 778 | 507 | +387.5% | 65% |
| Competitive Intelligence | 287 | 94 | +394.7% | 33% |
| Market Analysis | 384 | 143 | +376.7% | 37% |
| Sales Psychology | 323 | 207 | +314.0% | 64% |

---

## 🕳️ Research Gaps (Thinnest Cells)

Cells with the fewest papers are prime opportunities for content and offer design:

- `partnerships/development` — 1 papers
- `pricing-strategy/development` — 1 papers
- `b2b-marketing/development` — 2 papers
- `customer-success/evaluation` — 2 papers
- `business-models/evaluation` — 2 papers
- `partnerships/evaluation` — 2 papers
- `customer-retention/review` — 3 papers
- `product-market-fit/evaluation` — 3 papers

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

This corpus synthesizes 6,449 papers across 2021-2026 into an open,
reusable evidence base for business development research and practice: what the
field studies, how the disciplines connect, and where the literature is heading.

---

**Want to explore what the corpus suggests?**
`cd tools && python3 topic_planner.py`
