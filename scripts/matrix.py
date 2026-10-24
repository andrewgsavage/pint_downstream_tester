"""Print the test matrix as JSON for GitHub Actions.

Projects with `skip` set are left out. The FILTER environment variable, if set,
is a regex matched against project names to run only some of them.
"""

import json
import os
import re
import tomllib
from pathlib import Path

DEFAULT_PYTHON = "3.12"

with open(Path(__file__).resolve().parent.parent / "projects.toml", "rb") as f:
    projects = tomllib.load(f)["project"]

pattern = os.environ.get("FILTER") or ""
entries = [
    {"name": p["name"], "python": p.get("python", DEFAULT_PYTHON)}
    for p in projects
    if not p.get("skip") and re.search(pattern, p["name"])
]
print(json.dumps(entries))
