"""Compare each project's test failures under released Pint and Pint master.

Usage: python summarize.py <results-dir>

Prints a markdown report for the run summary. Many pinned releases have tests
that fail regardless of Pint (newer numpy, pandas, network access...), so a
project is only flagged when tests fail with Pint master that pass with the
release. Exits 1 if any project has such tests.
"""

import json
import os
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def base(test_id):
    """Test ID without its parameters: some include timestamps that differ per run."""
    return test_id.split("[", 1)[0]

MAX_LISTED = 20

results = {}
for f in Path(sys.argv[1]).rglob("*.json"):
    r = json.loads(f.read_text())
    results[(r["name"], r["pint"])] = r

with open(ROOT / "projects.toml", "rb") as f:
    projects = tomllib.load(f)["project"]


def cell(r):
    if r is None:
        return "– no result"
    if r["outcome"] == "error":
        return "⚠️ setup failed"
    n = len(r.get("failed", []))
    if r["outcome"] == "pass":
        return "✅ pass"
    # No failed tests but a non-zero exit: collection or usage error, or no tests found.
    return f"{n} failing" if n else f"pytest exit {r.get('exit_code')}"


rows, regressions, skipped = [], {}, []
for p in projects:
    name = p["name"]
    if p.get("skip"):
        skipped.append(f"- **{name}**: {p['skip']}")
        continue
    rel, mas = results.get((name, "release")), results.get((name, "master"))
    if rel is None and mas is None:
        continue
    status = ""
    if rel and mas and "error" not in (rel["outcome"], mas["outcome"]):
        # New means no variant of the test failed with released Pint.
        rel_failed = {base(t) for t in rel.get("failed", [])}
        new = sorted(t for t in mas.get("failed", []) if base(t) not in rel_failed)
        if new or (mas["outcome"] == "fail" and rel["outcome"] == "pass"):
            regressions[name] = new
            status = f"❌ {len(new) or 'some'} new"
        else:
            status = "✅ none"
    elif mas and mas["outcome"] == "error" and rel and rel["outcome"] != "error":
        regressions[name] = []
        status = "❌ setup fails only on master"
    rows.append(f"| {name} | `{p['requirement']}` | {cell(rel)} | {cell(mas)} | {status} |")

print("# Pint downstream results\n")
if os.environ.get("PINT_MASTER_SHA"):
    sha = os.environ["PINT_MASTER_SHA"]
    print(f"Pint master: [`{sha[:9]}`](https://github.com/hgrecco/pint/commit/{sha})\n")
if regressions:
    print(f"**{len(regressions)} project(s) have failures with Pint master that pass with released Pint.**\n")
    for name, new in regressions.items():
        print(f"<details><summary>{name}: {len(new)} new failure(s)</summary>\n")
        for t in new[:MAX_LISTED]:
            print(f"- `{t}`")
        if len(new) > MAX_LISTED:
            print(f"- ...and {len(new) - MAX_LISTED} more")
        print("\n</details>\n")
else:
    print("No tests fail with Pint master that pass with released Pint.\n")
print("| Project | Tested | Pint release | Pint master | New failures on master |")
print("|---|---|---|---|---|")
print("\n".join(rows))
if skipped:
    print("\n## Skipped\n")
    print("\n".join(skipped))
sys.exit(1 if regressions else 0)
