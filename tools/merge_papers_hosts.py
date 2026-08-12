#!/usr/bin/env python3
"""merge_papers_hosts.py — merge host-fetched papers.yaml files into a local corpus.

Dedupe key: normalized URL-identifier (arXiv/DOI) + normalized title.
Keeps the record with the most populated fields per key.

Usage:
  python3 tools/merge_papers_hosts.py <repo-dir> _distributed/*.yaml

Writes the union back into <repo-dir>/papers.yaml and prints stats.
"""
import re
import sys
import yaml


def nkey(p):
    url = (p.get("url") or "").strip().lower()
    m = re.search(r"(arxiv\.org/(abs|pdf)/\d{4}\.\d{4,5})v?\d*|doi\.org/(10\.\S+)", url)
    ident = (m.group(1) or m.group(3)) if m else url
    return ident, re.sub(r"[^a-z0-9]", "", (p.get("title") or "").lower())[:80]


def score(p):
    return sum(bool(p.get(k)) for k in (
        "url", "date", "category", "subcategory", "agent_type",
        "environment", "capability", "abstract", "venue"))


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    repo, *hostfiles = sys.argv[1:]
    local = yaml.safe_load(open(f"{repo}/papers.yaml"))["papers"]
    by_key = {}
    for p in local:
        by_key[nkey(p)] = p
    added = {}
    for hf in hostfiles:
        host = yaml.safe_load(open(hf))["papers"]
        for p in host:
            k = nkey(p)
            prev = by_key.get(k)
            if prev is None or score(p) > score(prev):
                by_key[k] = p
                added.setdefault(hf, 0)
                added[hf] += 1
    merged = list(by_key.values())
    with open(f"{repo}/papers.yaml", "w") as f:
        yaml.safe_dump({"papers": merged}, f, allow_unicode=True, sort_keys=False, width=1000)
    print(f"local={len(local)} union={len(merged)} (+{len(merged) - len(local)})")
    for hf, n in added.items():
        print(f"  {hf}: +{n}")


if __name__ == "__main__":
    main()
