"""Turn the CI jobs' result files into a markdown table for the run summary.

Usage: python summarize.py <results-dir>
"""

import json
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ICON = {"pass": "✅", "fail": "❌", "error": "⚠️ setup", None: "–"}

results = {}
for f in Path(sys.argv[1]).glob("*.json"):
    r = json.loads(f.read_text())
    results[(r["name"], r["pint"])] = r["outcome"]

with open(ROOT / "projects.toml", "rb") as f:
    projects = tomllib.load(f)["project"]

rows, regressions, skipped = [], [], []
for p in projects:
    name = p["name"]
    if p.get("skip"):
        skipped.append(f"- **{name}**: {p['skip']}")
        continue
    rel, mas = results.get((name, "release")), results.get((name, "master"))
    if rel is None and mas is None:
        continue
    if rel == "pass" and mas != "pass":
        regressions.append(name)
    rows.append(f"| {name} | `{p['requirement']}` | {ICON[rel]} | {ICON[mas]} |")

print("# Pint downstream results\n")
if regressions:
    print("**Pass with released Pint, fail with Pint master:** " + ", ".join(regressions) + "\n")
else:
    print("No project passes with released Pint and fails with Pint master.\n")
print("| Project | Tested | Pint release | Pint master |")
print("|---|---|:-:|:-:|")
print("\n".join(rows))
if skipped:
    print("\n## Skipped\n")
    print("\n".join(skipped))
