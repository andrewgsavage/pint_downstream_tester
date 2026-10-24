"""Run downstream projects' test suites against a given Pint.

Usage:
    python run_downstream.py                       # all projects, Pint master
    python run_downstream.py pyEQL                 # one project
    python run_downstream.py --pint release        # baseline: released Pint from PyPI
    python run_downstream.py --pint-ref some-branch
    python run_downstream.py --list-json           # project names, for the CI matrix

Each project gets its own virtual environment under ``.downstream/``.
Uses ``uv`` when it is on PATH, otherwise ``venv`` + ``pip``.
"""

from __future__ import annotations

import argparse
import json
import os
import shutil
import stat
import subprocess
import sys
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / ".downstream"
PINT_REPO = "https://github.com/hgrecco/pint"


def load_projects() -> dict[str, dict]:
    with open(ROOT / "projects.toml", "rb") as f:
        return {p["name"]: p for p in tomllib.load(f)["project"]}


def run(cmd: list[str], **kwargs) -> None:
    print("+", " ".join(cmd), flush=True)
    subprocess.run(cmd, check=True, **kwargs)


def rmtree(path: Path) -> None:
    """Remove a directory, including git's read-only files on Windows."""
    def make_writable_and_retry(func, p, _exc):
        os.chmod(p, stat.S_IWRITE)
        func(p)
    if path.exists():
        shutil.rmtree(path, onerror=make_writable_and_retry)


def venv_python(env: Path) -> Path:
    return env / ("Scripts/python.exe" if os.name == "nt" else "bin/python")


def make_env(env: Path) -> tuple[Path, list[str]]:
    """Create a fresh environment; return its python and a pip-install command."""
    rmtree(env)
    if shutil.which("uv"):
        run(["uv", "venv", "--python", sys.executable, str(env)])
        py = venv_python(env)
        return py, ["uv", "pip", "install", "--python", str(py)]
    run([sys.executable, "-m", "venv", str(env)])
    py = venv_python(env)
    run([str(py), "-m", "pip", "install", "-q", "--upgrade", "pip"])
    return py, [str(py), "-m", "pip", "install"]


def test_project(project: dict, pint: str, pint_ref: str) -> int:
    name = project["name"]
    print(f"\n{'=' * 20} {name} (pint: {pint}) {'=' * 20}", flush=True)
    work = WORK / name
    work.mkdir(parents=True, exist_ok=True)
    py, install = make_env(work / "env")

    run([*install, project["requirement"], *project.get("test_deps", [])])
    if pint == "master":
        run([*install, "--upgrade", f"pint @ git+{PINT_REPO}@{pint_ref}"])
    run([str(py), "-c", "import pint; print('pint', pint.__version__)"])

    if "pyargs" in project:
        # Run outside any source checkout so the installed package is imported.
        cmd, cwd = ["--pyargs", project["pyargs"]], work
    else:
        src = work / "src"
        rmtree(src)
        run(["git", "clone", "--depth", "1", "--branch", project["ref"],
             project["repo"], str(src)])
        cmd, cwd = [project["test_path"]], src

    cmd += project.get("pytest_args", [])
    print("+ pytest", " ".join(cmd), flush=True)
    return subprocess.run([str(py), "-m", "pytest", *cmd], cwd=cwd).returncode


def main() -> int:
    projects = load_projects()
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("names", nargs="*", help="projects to test (default: all)")
    parser.add_argument("--pint", choices=["master", "release"], default="master",
                        help="test against Pint from git or the released PyPI version")
    parser.add_argument("--pint-ref", default="master",
                        help="git ref of Pint to test when --pint=master")
    parser.add_argument("--list-json", action="store_true",
                        help="print project names as JSON and exit")
    args = parser.parse_args()

    if args.list_json:
        print(json.dumps(list(projects)))
        return 0

    unknown = set(args.names) - set(projects)
    if unknown:
        parser.error(f"unknown project(s): {', '.join(sorted(unknown))}")

    results = {}
    for name in args.names or projects:
        try:
            results[name] = test_project(projects[name], args.pint, args.pint_ref)
        except subprocess.CalledProcessError as e:
            print(f"Setup failed for {name}: {e}", flush=True)
            results[name] = e.returncode or 1
    print("\nSummary:")
    for name, code in results.items():
        print(f"  {'PASS' if code == 0 else 'FAIL'}  {name}")
    return int(any(results.values()))


if __name__ == "__main__":
    sys.exit(main())
