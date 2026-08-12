#!/usr/bin/env python3
"""distributed_openalex_fetch.py — sharded, budget-aware, resumable multi-host OpenAlex ingestion.

Solves the pain points observed in the first distributed run (2026-08-12):
  * overlapping category fetches across hosts   -> sharding: each category fetched once
  * hardcoded sibling-module deps               -> AST-based discovery of fetcher imports
  * hosts running into 0 credits + 429 backoff  -> budget-proportional allocation, clean stop at 0
  * no resume                                   -> manifest + fetch.log derived done-set
  * manual merge/validate/commit                -> automated, gated on 0 validation errors

Usage:
  python3 tools/distributed_openalex_fetch.py <repo-dir> --hosts "alias1 alias2 ..." \
      [--per-category 100] [--months 60] [--sleep 1] \
      [--dry-run] [--commit] [--push] [--resume] [--merge-only DIR]

  # multi-repo batch (reproducible weekly refresh) — config mode:
  python3 tools/distributed_openalex_fetch.py --config refresh.yaml --push

Config file (refresh.yaml):
  hosts: [tobias-weiss.org, chemie-lernen.org, contextual-intelligence.org, weiss@192.168.42.11]
  repos:
    agent-learning-research: {repo: ../agent-learning-research, per-category: 200, months: 60}
    dm-research:              {repo: ../dm-research,              per-category: 200, months: 60}

Notes:
  * hosts are SSH aliases (see ~/.ssh/config.d/personal.conf); for inventory hosts
    not in ssh config use "user@host" strings.
  * each host's public IP gets its own OpenAlex budget (1,000 credits/day, 10/page,
    resets midnight UTC); probe with curl of X-RateLimit-Remaining.
  * state + collected corpora live in <repo>/_distributed/.
"""
from __future__ import annotations

import argparse
import ast
import json
import re
import subprocess
import sys
import time
from pathlib import Path

MAILTO = "business@tobias-weiss.org"


def ssh(host: str, cmd: str, timeout: int = 120) -> str:
    r = subprocess.run(
        ["ssh", "-o", "ConnectTimeout=8", "-o", "BatchMode=yes", host, cmd],
        capture_output=True, text=True, timeout=timeout)
    if r.returncode != 0:
        raise RuntimeError(f"ssh {host}: {r.stderr.strip()[:300]}")
    return r.stdout.strip()


def host_credits(host: str) -> int:
    out = ssh(host, f'curl -sI --max-time 10 "https://api.openalex.org/works?per-page=1&mailto={MAILTO}" | grep -i x-ratelimit-remaining | head -1')
    m = re.search(r"x-ratelimit-remaining:\s*(\d+)", out, re.I)
    return int(m.group(1)) if m else 0


def extract_categories(fetcher: Path) -> list[str]:
    tree = ast.parse(fetcher.read_text())
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and any(
                isinstance(t, ast.Name) and t.id == "CATEGORY_TERMS" for t in node.targets):
            if isinstance(node.value, ast.List):
                cats = []
                for el in node.value.elts:
                    if isinstance(el, ast.Tuple) and el.elts and isinstance(el.elts[0], ast.Constant):
                        cats.append(str(el.elts[0].value))
                return cats
    raise RuntimeError(f"CATEGORY_TERMS not found in {fetcher}")


def detect_deps(fetcher: Path) -> list[Path]:
    """Find sibling modules the fetcher imports, transitively (e.g. fetch_new_papers.py -> domain.py)."""
    search_dirs = [fetcher.parent, fetcher.parent.parent]  # scripts/fetch/, scripts/
    deps: list[Path] = []
    seen: set[Path] = set()
    queue = [fetcher]
    while queue:
        f = queue.pop()
        if f in seen:
            continue
        seen.add(f)
        try:
            tree = ast.parse(f.read_text())
        except Exception:
            continue
        for node in ast.walk(tree):
            if isinstance(node, ast.ImportFrom) and node.module:
                mods = [node.module.split(".")[0]]
            elif isinstance(node, ast.Import):
                mods = [a.name.split(".")[0] for a in node.names]
            else:
                continue
            for mod in mods:
                for d in search_dirs:
                    cand = d / f"{mod}.py"
                    if cand.exists() and cand not in seen and cand != fetcher:
                        deps.append(cand)
                        queue.append(cand)
                        break
    return deps


def estimate_pages(per_category: int) -> int:
    """OpenAlex pages of 100; fetcher stops at per_category entries, may need a page more."""
    return max(1, (per_category + 99) // 100 + 1)


def allocate(categories: list[str], budgets: dict[str, int], per_category: int) -> dict[str, list[str]]:
    """Balance categories across hosts (round-robin), capped by each host's credit budget.

    Each category costs ~estimate_pages*10 credits. A host gets slots = budget//cost.
    Categories are assigned round-robin over hosts that still have slots, so the
    richest host covers the remainder — wall time ≈ total_cats / n_hosts.
    """
    cost = estimate_pages(per_category) * 10
    slots = {h: max(0, b // cost) for h, b in budgets.items()}
    plan: dict[str, list[str]] = {h: [] for h in budgets}
    hosts_w = [h for h in budgets if slots[h] > 0]
    idx = 0
    for cat in categories:
        if not hosts_w:
            break
        h = hosts_w[idx % len(hosts_w)]
        plan[h].append(cat)
        slots[h] -= 1
        if slots[h] <= 0:
            hosts_w.pop(idx % len(hosts_w))
        else:
            idx += 1
    return plan


def done_categories(repo: Path, host: str) -> set[str]:
    """Categories already completed on a host, derived from its fetch log."""
    out = ssh(host, f"grep -oE '[0-9]+ new for [a-z0-9-]+' ~/openalex/{repo.name}/fetch.log 2>/dev/null || true")
    done: set[str] = set()
    for line in out.splitlines():
        m = re.search(r"new for ([a-z0-9-]+)", line)
        if m:
            done.add(m.group(1))
    return done


def deploy(host: str, repo: Path):
    remote = f"~/openalex/{repo.name}"
    ssh(host, f"mkdir -p {remote}/scripts/fetch")
    fetcher = repo / "scripts/fetch/fetch_openalex_bulk.py"
    for local in [fetcher, repo / "papers.yaml", *detect_deps(fetcher)]:
        dest = remote if local == repo / "papers.yaml" else f"{remote}/scripts"
        subprocess.run(["rsync", "-az", "--quiet", str(local), f"{host}:{dest}/"],
                       check=True, capture_output=True)
    ssh(host, 'python3 -c "import requests, yaml" 2>/dev/null || python3 -m pip install --user --quiet pyyaml requests || true')


def launch(host: str, repo: Path, cats: list[str], per_category: int, months: int, sleep: int) -> str:
    remote = f"~/openalex/{repo.name}"
    cat_arg = ",".join(cats)
    cmd = (f"cd {remote} && nohup python3 scripts/fetch/fetch_openalex_bulk.py "
           f"--per-category {per_category} --months {months} --sleep {sleep} "
           f"--categories '{cat_arg}' > fetch.log 2>&1 & echo $!")
    return ssh(host, cmd)


def poll(repo: Path, hosts: list[str], timeout_s: int, poll_every: int = 30) -> bool:
    """Wait until all host processes exit. Returns False on timeout."""
    t0 = time.time()
    while time.time() - t0 < timeout_s:
        running = []
        for host in hosts:
            try:
                n = ssh(host, f"ps aux | grep -v grep | grep -c 'python3 scripts/fetch/fetch_openalex' || true")
            except Exception:
                running.append(host)  # unreachable — assume still running
                continue
            if n and n != "0":
                running.append(host)
        if not running:
            print("  all hosts finished", flush=True)
            return True
        for h in running:
            try:
                credits = host_credits(h)
                if credits <= 0:
                    print(f"  {h}: 0 credits — killing to avoid 429 backoff waste", flush=True)
                    ssh(h, "pkill -f 'python3 scripts/fetch' || true")
            except Exception:
                pass
        print(f"  running: {running}", flush=True)
        time.sleep(poll_every)
    return False


def _yaml_load(path: Path | str):
    import yaml
    loader = getattr(yaml, "CSafeLoader", yaml.SafeLoader)  # C loader is ~10x faster
    return yaml.load(Path(path).read_text(), Loader=loader)


def _yaml_dump(data, path: Path):
    import yaml
    path.write_text(yaml.safe_dump(data, allow_unicode=True, sort_keys=False, width=1000))


def merge(repo: Path, hostfiles: list[Path]):
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

    local = _yaml_load(repo / "papers.yaml")["papers"]
    by_key = {nkey(p): p for p in local}
    for hf in hostfiles:
        for p in _yaml_load(hf)["papers"]:
            k = nkey(p)
            prev = by_key.get(k)
            if prev is None or score(p) > score(prev):
                by_key[k] = p
    merged = list(by_key.values())
    _yaml_dump({"papers": merged}, repo / "papers.yaml")
    print(f"  merge: local={len(local)} union={len(merged)} (+{len(merged) - len(local)})")
    return len(merged)


def validate(repo: Path) -> tuple[int, int]:
    v = repo / "scripts/validate_papers.py"
    if not v.exists():
        return -1, -1
    r = subprocess.run(["python3", str(v)], capture_output=True, text=True, cwd=repo)
    errors = sum(1 for ln in r.stdout.splitlines() if re.match(r"^\s+- \[", ln))
    return errors, 0


def run_repo(repo: Path, hosts: list[str], per_category: int, months: int, sleep: int,
             dry_run: bool, commit: bool, push: bool, resume: bool, timeout_s: int):
    fetcher = repo / "scripts/fetch/fetch_openalex_bulk.py"
    if not fetcher.exists():
        print(f"SKIP {repo.name}: no fetcher")
        return
    out = repo / "_distributed"
    out.mkdir(exist_ok=True)

    cats = extract_categories(fetcher)
    print(f"repo {repo.name}: {len(cats)} categories | deps: {[d.name for d in detect_deps(fetcher)]}")

    budgets = {}
    for h in hosts:
        budgets[h] = host_credits(h)
        print(f"  {h}: {budgets[h]} credits")
        if not dry_run:
            deploy(h, repo)

    if resume:
        for h in hosts:
            done = done_categories(repo, h)
            if done:
                print(f"  {h}: {len(done)} categories already fetched — skipping on resume")
                cats = [c for c in cats if c not in done]

    plan = allocate(cats, budgets, per_category)
    total_pages = sum(estimate_pages(per_category) for c in cats)
    print(f"allocation (est. {total_pages} pages ≈ {total_pages*10} credits):")
    for h, cs in plan.items():
        print(f"  {h}: {len(cs)} cats — {cs[:6]}{'…' if len(cs) > 6 else ''}")

    if dry_run:
        return

    for h, cs in plan.items():
        if not cs:
            continue
        print(f"launching {h}: {len(cs)} cats")
        launch(h, repo, cs, per_category, months, sleep)

    if not poll(repo, hosts, timeout_s):
        print("WARNING: poll timeout — collect what finished; rerun with --resume to finish the rest")
    time.sleep(5)

    hostfiles = []
    for h in hosts:
        f = out / f"{h.replace('@', '_').replace('.', '_')}.yaml"
        try:
            subprocess.run(["scp", "-q", f"{h}:~/openalex/{repo.name}/papers.yaml", str(f)],
                           check=True, capture_output=True, timeout=120)
            hostfiles.append(f)
            print(f"collected {h} -> {f.name}")
        except Exception as e:
            print(f"  collect {h} failed: {e}")

    if hostfiles:
        n = merge(repo, hostfiles)
        errors, _ = validate(repo)
        print(f"validate: {errors} errors")
        if errors and errors > 0:
            print("ERRORS present — not committing")
        elif commit:
            subprocess.run(["git", "-C", str(repo), "add", "papers.yaml"], check=True)
            subprocess.run(["git", "-C", str(repo), "commit", "-q", "-m",
                            f"OpenAlex bulk fetch via distributed hosts ({','.join(hosts)}): {n} papers"],
                           check=True)
            print(f"committed {n} papers")
            if push:
                subprocess.run(["git", "-C", str(repo), "push", "-q", "origin", "HEAD:main"], check=True)
                print("pushed")


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("repo", nargs="?", help="local repo directory (e.g. agent-learning-research)")
    ap.add_argument("--config", help="YAML config with hosts + repos (batch mode)")
    ap.add_argument("--hosts", help="space-separated SSH aliases")
    ap.add_argument("--per-category", type=int, default=100)
    ap.add_argument("--months", type=int, default=60)
    ap.add_argument("--sleep", type=int, default=1)
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--commit", action="store_true", help="git commit after merge")
    ap.add_argument("--push", action="store_true", help="git push after commit")
    ap.add_argument("--resume", action="store_true", help="skip categories already fetched")
    ap.add_argument("--merge-only", metavar="DIR", help="only merge _distributed/*.yaml from DIR and exit")
    ap.add_argument("--timeout", type=int, default=7200, help="poll timeout seconds")
    args = ap.parse_args()

    if args.merge_only:
        repo = Path(args.repo).resolve()
        files = sorted(Path(args.merge_only).glob("*.yaml"))
        if not files:
            sys.exit(f"no host yaml files in {args.merge_only}")
        merge(repo, files)
        return

    if args.config:
        import yaml as _y
        cfg = _y.safe_load(Path(args.config).read_text())
        hosts = cfg["hosts"]
        for name, rc in cfg["repos"].items():
            repo = Path(rc.get("repo", name)).resolve()
            print(f"\n########## {name} ##########", flush=True)
            run_repo(repo, hosts, rc.get("per-category", args.per_category),
                     rc.get("months", args.months), rc.get("sleep", args.sleep),
                     args.dry_run, args.commit, args.push, args.resume, args.timeout)
        return

    if not args.repo or not args.hosts:
        ap.error('need <repo-dir> --hosts "..." or --config')
    repo = Path(args.repo).resolve()
    run_repo(repo, args.hosts.split(), args.per_category, args.months, args.sleep,
             args.dry_run, args.commit, args.push, args.resume, args.timeout)


if __name__ == "__main__":
    main()
