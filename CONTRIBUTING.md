# Contributing to business-development-research

Thanks for helping build the evidence base for KI-Kompetenz-Training!

## Ways to Contribute

### 1. Add Papers

1. Fork the repository.
2. Edit `papers.yaml` — append entries in this format:

```yaml
- title: "A great business development paper"
  date: "2026-07"
  url: https://doi.org/10.xxxx/xxxxx
  category: ai-adoption
  subcategory: application
  authors: []
  abstract: "Short abstract..."
```

3. Open a PR. Use the `paper_submission` issue template for guidance.

### Taxonomy Reference

**Categories (20):** `market-analysis`, `go-to-market`, `sales-strategy`,
`b2b-marketing`, `content-marketing`, `digital-marketing`, `brand-building`,
`customer-acquisition`, `customer-retention`, `customer-success`,
`pricing-strategy`, `product-market-fit`, `business-models`,
`competitive-intelligence`, `partnerships`, `sales-psychology`, `networking`,
`entrepreneurship`, `growth-metrics`, `ai-adoption`

**Aspects (8):** `theory`, `mechanism`, `method`, `application`,
`development`, `systems`, `evaluation`, `review`

### 2. Fix Classification

Run the reclassification helper after tuning subcategory rules:

```bash
python3 scripts/reclassify_papers.py --dry-run
python3 scripts/reclassify_papers.py
```

### 3. Improve Tooling

All scripts are standard Python 3.11+ with `pyyaml`, `requests`,
`matplotlib`. Keep them dependency-light and self-contained (path resolution
relative to the repo root).

## Validation

Before merging, run:

```bash
python3 scripts/validate_papers.py --strict
python3 scripts/generate_readme.py --check
```