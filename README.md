<h1 align="center">
  <strong>Business Development Research Corpus</strong>
</h1>
<h3 align="center">Evidence base for KI-Kompetenz-Training — 20 business development disciplines</h3>

### 🔗 Links

- **GitHub**: https://github.com/tobias-weiss-ai-xr/business-development-research
- **License**: https://github.com/tobias-weiss-ai-xr/business-development-research/blob/main/LICENSE
- **CI**: https://github.com/tobias-weiss-ai-xr/business-development-research/actions/workflows/validate.yml
- **Marketing**: https://github.com/tobias-weiss-ai-xr/marketing-research
- **AI Literacy**: https://github.com/tobias-weiss-ai-xr/ai-literacy-research
- **Learning**: https://github.com/tobias-weiss-ai-xr/learning-research


> 💼 **Business development research corpus:** market analysis, go-to-market,
> sales, marketing, brand building, customer acquisition/retention, pricing,
> strategy, leadership, and more — part of the family of `*-research` corpora.

<p align="center">
  <img src="https://raw.githubusercontent.com/tobias-weiss-ai-xr/business-development-research/main/assets/visualizations/category_distribution.png" alt="Teaser" width="600" />
</p>

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
| **Papers Analyzed** | 5,963 |
| **Business Development Disciplines** | 20 |
| **Time Span** | 2021-2026 |
| **Research Aspects** | 8 |
| **Taxonomy Cells** | 160 |
| **Saturation** | 100.0% (160/160 cells) |

### Top Evidence Areas

1. **AI Adoption & Transformation** — 742 papers
2. **Digital Marketing & SEO** — 400 papers
3. **Market Analysis & Research** — 384 papers
4. **Content Marketing & Thought Leadership** — 380 papers
5. **Go-to-Market Strategy** — 359 papers
6. **Sales Psychology & Negotiation** — 323 papers

---

## 📊 The 20-Category Taxonomy

| Category | Papers |
|----------|--------|
| Market Analysis & Research | 384 |
| Go-to-Market Strategy | 359 |
| Sales Strategy & Process | 265 |
| B2B Marketing & Lead Gen | 244 |
| Content Marketing & Thought Leadership | 380 |
| Digital Marketing & SEO | 400 |
| Brand & Positioning | 266 |
| Customer Acquisition & Growth | 203 |
| Customer Retention & Churn | 214 |
| Customer Success & Expansion | 208 |
| Pricing & Monetization | 317 |
| Product-Market Fit & Validation | 252 |
| Business Models & Innovation | 253 |
| Competitive Intelligence | 202 |
| Partnerships & Alliances | 205 |
| Sales Psychology & Negotiation | 323 |
| Networking & Relationships | 304 |
| Entrepreneurship & Small Business | 235 |
| Growth Metrics & Analytics | 207 |
| AI Adoption & Transformation | 742 |

### Research Aspects (Subcategories)

| Aspect | Papers |
|--------|--------|
| Theory | 597 |
| Mechanism | 723 |
| Method | 1920 |
| Application | 1055 |
| Development | 102 |
| Systems & Technology | 1069 |
| Evaluation & Benchmarks | 201 |
| Reviews & Surveys | 296 |

---

## 🚀 Emerging Themes (Last 12 Months)

1. **agentic** — 67 papers
2. **eu ai act** — 9 papers
3. **literacy** — 111 papers
4. **negotiation** — 88 papers
5. **benchmark** — 129 papers
6. **solo** — 4 papers

## 📈 Category Momentum (Last 12 Months)

Ranked by output density × year-over-year growth — the strongest leading indicator for what to cover next:

| Category | Total | Last 12m | Growth | 12-m share |
|----------|------:|---------:|-------:|-----------:|
| B2B Marketing & Lead Gen | 244 | 197 | +885.0% | 81% |
| AI Adoption & Transformation | 742 | 471 | +352.9% | 64% |
| Market Analysis & Research | 384 | 143 | +376.7% | 37% |
| Sales Psychology & Negotiation | 323 | 207 | +314.0% | 64% |
| Digital Marketing & SEO | 400 | 133 | +280.0% | 33% |
| Networking & Relationships | 304 | 110 | +254.8% | 36% |

---

## 🕳️ Research Gaps (Thinnest Cells)

Cells with the fewest papers are prime opportunities for content and offer design:

- `partnerships/development` — 1 papers
- `pricing-strategy/development` — 1 papers
- `b2b-marketing/development` — 2 papers
- `customer-success/evaluation` — 2 papers
- `business-models/evaluation` — 2 papers
- `partnerships/evaluation` — 2 papers
- `customer-acquisition/evaluation` — 3 papers
- `customer-retention/review` — 3 papers

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

- **Content site:** [ki-kompetenz-training](https://github.com/tobias-weiss-ai-xr/ki-kompetenz-training) — KI-Kompetenz-Training
- **Analogous corpus:** [graph-research](https://github.com/tobias-weiss-ai-xr/graph-research)
- **Analogous corpus:** [learning-research](https://github.com/tobias-weiss-ai-xr/learning-research)

---

## 📊 Corpus Statistics

**6,444 papers** across **20 categories**.  
Sources: **arXiv** 1,749 (27%) · **DOI** 4,439 (68%) · **Other** 256 (3%).  
Full paper list: [GitHub Pages site](https://tobias-weiss-ai-xr.github.io/business-development-research).

### Top categories

| Category | Papers | Recent | |
|----------|--------|--------|-|
| ai-adoption | **773** | 0 | ████████████ |
| digital-marketing | **469** | 0 | ███████░░░░░ |
| pricing-strategy | **402** | 0 | ██████░░░░░░ |
| market-analysis | **384** | 0 | █████░░░░░░░ |
| content-marketing | **380** | 0 | █████░░░░░░░ |
| go-to-market | **359** | 0 | █████░░░░░░░ |
| sales-psychology | **323** | 0 | █████░░░░░░░ |
| entrepreneurship | **313** | 0 | ████░░░░░░░░ |
| networking | **304** | 0 | ████░░░░░░░░ |
| competitive-intelligence | **287** | 0 | ████░░░░░░░░ |
| *other* | **2,450** | | |


### By year

| Year | Papers | |
|------|--------|-|
| 2024 | 972 | ██████░░░░░░ |
| 2025 | 1,004 | ██████░░░░░░ |
| 2026 | 1,886 | ████████████ |


### Momentum (hottest categories)

| Category | Total | Rate | Recent | Score |
|----------|-------|------|--------|-------|
| B2B Marketing & Lead Gen | 244 | 16.4/mo | 81% | 966 |
| Digital Marketing & SEO | 469 | 16.8/mo | 43% | 520 |
| AI Adoption & Transformation | 773 | 41.8/mo | 65% | 448 |
| Competitive Intelligence | 287 | 7.8/mo | 33% | 428 |
| Market Analysis & Research | 384 | 11.9/mo | 37% | 414 |


### Trending keywords

| Keyword | Papers | Burst |
|---------|--------|-------|
| mvp | 1 | 2.71 |
| agentic | 71 | 2.63 |
| eu ai act | 10 | 2.44 |
| saas | 20 | 2.30 |
| literacy | 135 | 2.29 |
| negotiation | 108 | 2.21 |
| benchmark | 161 | 2.20 |
| genai | 71 | 2.17 |


### Top venues

| Venue | Papers |
|-------|--------|
| Zenodo (CERN European Organization for Nuclear Research) | 169 |
| Sustainability | 122 |
| Journal of Business Research | 54 |
| SSRN Electronic Journal | 48 |
| The International Conference on Sustainable Economics Management and Accounting Proceeding | 39 |
| Open MIND | 38 |
| Journal of the Association for Information Systems | 37 |
| Journal of Retailing and Consumer Services | 35 |


### Research gaps (thinnest cells)

| Cell | Papers |
|------|--------|
| `partnerships/development` | 1 |
| `pricing-strategy/development` | 1 |
| `b2b-marketing/development` | 2 |
| `customer-success/evaluation` | 2 |
| `business-models/evaluation` | 2 |



*Generated 2026-08 by `scripts/standard_stats.py`.*


## 📄 License

**© 2026 KI-Kompetenz-Training | Tobias Weiss**

- **Research corpus:** Proprietary
- **Tools:** MIT License

---

## 🙏 Acknowledgments

This corpus synthesizes 5,963 papers across 2021-2026 to create a
comprehensive evidence base for business development decisions: what to write,
what to offer, how to price, and where the market is heading.

---

**Want to turn this corpus into content?**
`cd tools && python3 topic_planner.py`
