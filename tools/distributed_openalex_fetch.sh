#!/usr/bin/env bash
# distributed_openalex_fetch.sh — run OpenAlex bulk fetches across multiple SSH hosts
# to multiply the daily credit budget (OpenAlex free tier = 1,000 credits/IP/day,
# resets midnight UTC; 10 credits/page). Each host's public IP gets its own budget.
#
# Usage:
#   ./distributed_openalex_fetch.sh <repo-dir> --hosts "h1 h2 h3" \
#       [--per-category 100] [--months 60] [--sleep 1]
#
# Flow: rsync fetcher + papers.yaml to each host -> launch nohup fetch -> poll ->
#       scp papers.yaml back to ./_distributed/<host>.yaml
# Then merge results locally with tools/merge_papers_hosts.py.
#
# Example (4 hosts, 4 repos, parallel):
#   for repo in agent-learning-research agentic-vr-research ...; do ... done
#
# Requirements: ssh access to hosts (see ~/.ssh/config.d/personal.conf),
# python3 + requests + pyyaml on hosts (pip install --user pyyaml if missing).

set -euo pipefail

REPO="${1:?usage: distributed_openalex_fetch.sh <repo-dir> --hosts \"h1 h2 ...\" [opts]}"
shift
HOSTS=""
PER_CATEGORY=100
MONTHS=60
SLEEP=1

while [[ $# -gt 0 ]]; do
  case "$1" in
    --hosts) HOSTS="$2"; shift 2 ;;
    --per-category) PER_CATEGORY="$2"; shift 2 ;;
    --months) MONTHS="$2"; shift 2 ;;
    --sleep) SLEEP="$2"; shift 2 ;;
    *) echo "unknown arg: $1"; exit 1 ;;
  esac
done

[ -n "$HOSTS" ] || { echo "--hosts required"; exit 1; }
FETCHER="$REPO/scripts/fetch/fetch_openalex_bulk.py"
PAPERS="$REPO/papers.yaml"
[ -f "$FETCHER" ] || { echo "no fetcher at $FETCHER"; exit 1; }

# The fetcher may import sibling modules (fetch_new_papers.py, domain.py) — deploy them too.
EXTRA=()
for dep in fetch_new_papers.py domain.py; do
  [ -f "$REPO/scripts/fetch/$dep" ] && EXTRA+=("$REPO/scripts/fetch/$dep")
  [ -f "$REPO/scripts/$dep" ] && EXTRA+=("$REPO/scripts/$dep")
done

mkdir -p _distributed
for host in $HOSTS; do
  echo "== deploying to $host =="
  ssh "$host" "mkdir -p ~/openalex/$(basename "$REPO")/scripts/fetch"
  rsync -az --quiet "$FETCHER" "$host:~/openalex/$(basename "$REPO")/scripts/fetch/"
  for dep in "${EXTRA[@]:-}"; do
    [ -f "$dep" ] && rsync -az --quiet "$dep" "$host:~/openalex/$(basename "$REPO")/scripts/$(basename "$dep")"
  done
  rsync -az --quiet "$PAPERS" "$host:~/openalex/$(basename "$REPO")/"
  # ensure python deps
  ssh "$host" 'python3 -c "import requests, yaml" 2>/dev/null || python3 -m pip install --user --quiet pyyaml requests || true'
  ssh "$host" "cd ~/openalex/$(basename "$REPO") && nohup python3 scripts/fetch/fetch_openalex_bulk.py \
      --per-category $PER_CATEGORY --months $MONTHS --sleep $SLEEP > fetch.log 2>&1 & echo launched"
done

echo "Launched on: $HOSTS — poll with:"
for host in $HOSTS; do
  echo "  ssh $host 'tail ~/openalex/$(basename "$REPO")/fetch.log'"
done
echo "Check budget per host:"
echo "  ssh <host> 'curl -sI \"https://api.openalex.org/works?per-page=1&mailto=business@tobias-weiss.org\" | grep -i x-ratelimit-remaining'"
echo "Collect:"
echo "  for host in $HOSTS; do scp \$host:~/openalex/$(basename "$REPO")/papers.yaml _distributed/\$host.yaml; done"
