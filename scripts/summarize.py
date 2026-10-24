"""Turn the per-job result files into a markdown table for the run summary.

Usage: python scripts/summarize.py <results-dir>
"""

import json
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
ICON = {"pass": "✅", "fail": "❌", "error": "⚠️ setup", None: "–"}

results = {}
for f in Path(sys.argv[1]).glob("*.json"):
    r = json.loads(f.read_text())
    results[(r["name"], r["pint"])] = r

with open(ROOT / "projects.toml", "rb") as f:
    projects = tomllib.load(f)["project"]

rows, regressions, skipped = [], [], []
for p in projects:
    name = p["name"]
    if p.get("skip"):
        skipped.append(f"- **{name}**: {p['skip']}")
        continue
    rel, mas = results.get((name, "release"), {}), results.get((name, "master"), {})
    if not rel and not mas:
        continue
    if rel.get("outcome") == "pass" and mas.get("outcome") != "pass":
        regressions.append(name)
    ref = rel.get("ref") or mas.get("ref") or ""
    rows.append(
        f"| {name} | `{ref}` | {ICON[rel.get('outcome')]} | {ICON[mas.get('outcome')]} |"
    )

print("# Pint downstream results\n")
if regressions:
    print("**Pass with pint release but not with master:** " + ", ".join(regressions) + "\n")
else:
    print("No project passes with the pint release and fails with master.\n")
print("| Project | Tested ref | pint release | pint master |")
print("|---|---|:-:|:-:|")
print("\n".join(rows))
if skipped:
    print("\n## Skipped\n")
    print("\n".join(skipped))
