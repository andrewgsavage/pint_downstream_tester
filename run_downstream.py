"""Run downstream projects' test suites against a given Pint.

Usage:
    python run_downstream.py                       # all projects, Pint master
    python run_downstream.py pyEQL                 # one project
    python run_downstream.py --pint release        # baseline: released Pint from PyPI
    python run_downstream.py --pint-ref some-branch
    python run_downstream.py --list-json           # project names, for the CI matrix
    python run_downstream.py --list-json --filter 'pint-'  # only names matching a regex

Each project gets its own virtual environment under ``.downstream/``.
Uses ``uv`` when it is on PATH, otherwise ``venv`` + ``pip``.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import stat
import subprocess
import sys
import tomllib
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
WORK = ROOT / ".downstream"
PINT_REPO = "https://github.com/hgrecco/pint"
# System libraries Qt needs to start under xvfb on Ubuntu.
QT_APT = [
    "xvfb", "libegl1", "libgl1", "libxkbcommon-x11-0", "libxcb-icccm4", "libxcb-image0",
    "libxcb-keysyms1", "libxcb-randr0", "libxcb-render-util0", "libxcb-xinerama0",
    "libxcb-xfixes0", "libxcb-shape0", "libxcb-cursor0", "libdbus-1-3",
]


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


def make_env(env: Path, python: str | None = None) -> tuple[Path, list[str]]:
    """Create a fresh environment; return its python and a pip-install command.

    ``python`` picks another Python version for the environment; this needs uv.
    """
    rmtree(env)
    if shutil.which("uv"):
        run(["uv", "venv", "--python", python or sys.executable, str(env)])
        py = venv_python(env)
        return py, ["uv", "pip", "install", "--python", str(py)]
    if python:
        raise RuntimeError(f"uv is needed to create a Python {python} environment")
    run([sys.executable, "-m", "venv", str(env)])
    py = venv_python(env)
    run([str(py), "-m", "pip", "install", "-q", "--upgrade", "pip"])
    return py, [str(py), "-m", "pip", "install"]


def failed_tests(junit: Path) -> list[str]:
    """Test IDs that failed or errored, from a pytest JUnit XML report."""
    if not junit.exists():
        return []
    failed = []
    for case in ET.parse(junit).iter("testcase"):
        if case.find("failure") is not None or case.find("error") is not None:
            failed.append(f"{case.get('classname')}::{case.get('name')}")
    return sorted(failed)


def test_project(project: dict, pint: str, pint_ref: str) -> tuple[int, list[str]]:
    """Install and test one project; return pytest's exit code and the failed tests."""
    name = project["name"]
    print(f"\n{'=' * 20} {name} (pint: {pint}) {'=' * 20}", flush=True)
    work = WORK / name
    work.mkdir(parents=True, exist_ok=True)
    py, install = make_env(work / "env", project.get("python"))

    apt = project.get("apt", []) + (QT_APT if project.get("qt") else [])
    if apt and os.environ.get("CI") and shutil.which("apt-get"):
        run(["sudo", "apt-get", "update", "-q"])
        run(["sudo", "apt-get", "install", "-yq", *apt])

    # Pint is optional for some projects, so always ask for it; the resolver picks
    # the newest release the project allows.
    run([*install, project["requirement"], *project.get("test_deps", []), "pint"])
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

    junit = work / "junit.xml"
    junit.unlink(missing_ok=True)
    cmd += [*project.get("pytest_args", []), f"--junitxml={junit}"]
    print("+ pytest", " ".join(cmd), flush=True)
    pytest = [str(py), "-m", "pytest", *cmd]
    if project.get("qt") and shutil.which("xvfb-run"):
        pytest = ["xvfb-run", "-a", *pytest]
    code = subprocess.run(pytest, cwd=cwd).returncode
    return code, failed_tests(junit)


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
    parser.add_argument("--filter", default="",
                        help="with --list-json, only names matching this regex")
    parser.add_argument("--results-dir", type=Path,
                        help="write a <project>-<pint>.json outcome file per project here")
    parser.add_argument("--report-only", action="store_true",
                        help="exit 0 when tests fail (setup failures still exit 1); "
                             "for CI, where the summary compares failures across Pint versions")
    args = parser.parse_args()

    if args.list_json:
        print(json.dumps([n for n, p in projects.items()
                          if not p.get("skip") and re.search(args.filter, n)]))
        return 0

    unknown = set(args.names) - set(projects)
    if unknown:
        parser.error(f"unknown project(s): {', '.join(sorted(unknown))}")

    results = {}
    setup_failed = False
    for name in args.names or projects:
        if projects[name].get("skip") and not args.names:
            print(f"Skipping {name}: {projects[name]['skip']}")
            continue
        failed = []
        try:
            results[name], failed = test_project(projects[name], args.pint, args.pint_ref)
            outcome = "pass" if results[name] == 0 else "fail"
        except (subprocess.CalledProcessError, RuntimeError) as e:
            print(f"Setup failed for {name}: {e}", flush=True)
            results[name] = getattr(e, "returncode", 1) or 1
            outcome = "error"
            setup_failed = True
        if args.results_dir:
            args.results_dir.mkdir(parents=True, exist_ok=True)
            out = args.results_dir / f"{name}-{args.pint}.json"
            out.write_text(json.dumps({"name": name, "pint": args.pint,
                                       "outcome": outcome, "exit_code": results[name],
                                       "failed": failed}))
    print("\nSummary:")
    for name, code in results.items():
        print(f"  {'PASS' if code == 0 else 'FAIL'}  {name}")
    if args.report_only:
        return int(setup_failed)
    return int(any(results.values()))


if __name__ == "__main__":
    sys.exit(main())
