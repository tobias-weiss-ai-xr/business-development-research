# Business Development Research — Documentation Index

## Research

| Document | Purpose |
|----------|---------|
| [`research/taxonomy.md`](research/taxonomy.md) | The 20×8 taxonomy definition |
| [`research/literature_review.md`](research/literature_review.md) | Synthesis of the corpus |
| [`research/bizdev_trends_2026.md`](research/bizdev_trends_2026.md) | Trend analysis for content planning |
| [`research/landscape_report.md`](research/landscape_report.md) | Full corpus landscape analysis |
| [`research/ai_adoption_deep_dive.md`](research/ai_adoption_deep_dive.md) | Deep-dive on the AI-adoption evidence base (core of the ALaaS offer) |

## Topics (Generated)

| Document | Purpose |
|----------|---------|
| [`topics/ARTICLE_TOPICS.md`](topics/ARTICLE_TOPICS.md) | Evidence-ranked content topics for ki-kompetenz-training.org |

## Data Files

| File | Description |
|------|-------------|
| `../papers.yaml` | Source of truth (paper metadata) |
| `../papers.json` | JSON export of all papers |
| `../statistics.json` | Machine-readable statistics |

## Regenerating

```bash
python3 scripts/analysis/generate_analysis.py   # statistics.json + papers.json
python3 scripts/visualize_statistics.py          # PNG charts
python3 tools/trend_scanner.py --months 6        # trend report
python3 tools/topic_planner.py --top 10          # ARTICLE_TOPICS.md
python3 scripts/analysis/generate_reports.py     # literature review + trends
python3 scripts/generate_readme.py               # README.md
```