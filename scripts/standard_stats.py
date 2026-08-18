#!/usr/bin/env python3
"""Standard statistics generator."""
import json, yaml
from pathlib import Path
from collections import Counter
REPO = Path(__file__).resolve().parent.parent
with open(REPO / "papers.yaml") as f:
    data = yaml.safe_load(f) or {}
papers = data.get("papers", [])
total = len(papers)
by_source = Counter(p.get("source", "unknown") for p in papers)
by_year = Counter(str(p.get("date", "unknown")[:4]) if p.get("date") else "unknown" for p in papers)
stats = {"total": total, "by_source": dict(by_source), "by_year": dict(by_year), "saturation": f"{min(100, total//100)}%"}
with open(REPO / "statistics.json", "w") as f:
    json.dump(stats, f, indent=2)
print(f"Wrote statistics.json ({total} papers)")
