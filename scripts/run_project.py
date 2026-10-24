"""Clone one downstream project, install it with a given pint, and run its tests.

Usage: python scripts/run_project.py <name> <release|master>

Writes results/<name>-<pint>.json and exits non-zero if setup or tests fail.
"""

import json
import os
import shlex
import subprocess
import sys
import tomllib
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
WORK = ROOT / "work"
RESULTS = ROOT / "results"

PINT_REPO = os.environ.get("PINT_REPO", "hgrecco/pint")
PINT_REF = os.environ.get("PINT_REF", "master")
PINT_SPECS = {
    "release": ["pint"],
    "master": [f"pint @ git+https://github.com/{PINT_REPO}@{PINT_REF}"],
}
TEST_EXTRAS = ("test", "tests", "testing")
TEST_REQUIREMENTS = (
    "requirements-test.txt",
    "requirements_test.txt",
    "test-requirements.txt",
    "test_requirements.txt",
    "requirements-tests.txt",
    "requirements/test.txt",
    "requirements/tests.txt",
    "requirements/testing.txt",
    "requirements-dev.txt",
    "requirements_dev.txt",
)
QT_APT = (
    "xvfb libegl1 libgl1 libxkbcommon-x11-0 libxcb-icccm4 libxcb-image0 "
    "libxcb-keysyms1 libxcb-randr0 libxcb-render-util0 libxcb-xinerama0 "
    "libxcb-xfixes0 libxcb-shape0 libxcb-cursor0 libdbus-1-3"
).split()


def load(name):
    with open(ROOT / "projects.toml", "rb") as f:
        projects = tomllib.load(f)["project"]
    for p in projects:
        if p["name"] == name:
            return p
    sys.exit(f"unknown project {name!r}")


def run(cmd, cwd=None, shell=False):
    shown = cmd if shell else shlex.join(cmd)
    print(f"::group::{shown}", flush=True)
    try:
        subprocess.run(cmd, cwd=cwd, shell=shell, check=True)
    finally:
        print("::endgroup::", flush=True)


def pip(*args, cwd=None):
    run([sys.executable, "-m", "pip", *args], cwd=cwd)


def latest_release(repo):
    """Tag of the repo's latest GitHub release, or None to use the default branch."""
    req = urllib.request.Request(f"https://api.github.com/repos/{repo}/releases/latest")
    token = os.environ.get("GH_TOKEN")
    if token:
        req.add_header("Authorization", f"Bearer {token}")
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.load(r)["tag_name"]
    except urllib.error.HTTPError as e:
        if e.code == 404:
            return None
        raise


def checkout(p):
    url = p.get("url") or f"https://github.com/{p['repo']}"
    ref = p.get("ref", "release")
    if ref == "release":
        ref = latest_release(p["repo"]) if "url" not in p else None
    elif ref == "default":
        ref = None
    dest = WORK / p["name"]
    cmd = ["git", "clone", "--depth", "1", "--filter=blob:limit=5m"]
    if ref:
        cmd += ["--branch", ref]
    if p.get("submodules"):
        cmd += ["--recurse-submodules", "--shallow-submodules"]
    run([*cmd, url, str(dest)])
    sha = subprocess.check_output(["git", "rev-parse", "--short", "HEAD"], cwd=dest, text=True).strip()
    # Custom install/test commands can use the checked-out tag, e.g. to pip install that release.
    os.environ["DOWNSTREAM_REF"] = ref or ""
    return dest, ref or f"default@{sha}"


def default_install(p, src):
    """pip install the checkout with whatever test dependencies it declares."""
    pyproject = {}
    if (src / "pyproject.toml").exists():
        with open(src / "pyproject.toml", "rb") as f:
            pyproject = tomllib.load(f)

    declared = pyproject.get("project", {}).get("optional-dependencies", {})
    extras = [e for e in TEST_EXTRAS if e in declared]
    if declared and not extras and "dev" in declared:
        extras = ["dev"]
    if not declared:
        # setup.py/setup.cfg projects: pip only warns about extras that don't exist
        extras = list(TEST_EXTRAS)
    extras += p.get("extras", [])
    target = f".[{','.join(extras)}]" if extras else "."
    editable = ["-e"] if p.get("editable", True) else []
    pip("install", *editable, target, cwd=src)

    groups = pyproject.get("dependency-groups", {})
    for g in (*TEST_EXTRAS, "dev"):
        if g in groups:
            pip("install", "--group", g, cwd=src)
            break

    poetry = pyproject.get("tool", {}).get("poetry", {}).get("group", {})
    for g in (*TEST_EXTRAS, "dev"):
        if g in poetry:
            names = [n for n in poetry[g].get("dependencies", {}) if n != "python"]
            if names:
                pip("install", *names)
            break

    for req in TEST_REQUIREMENTS:
        if (src / req).exists():
            pip("install", "-r", req, cwd=src)
            break


def setup(p, src, variant):
    apt = list(p.get("apt", []))
    if p.get("qt"):
        apt += QT_APT
    if apt:
        run(["sudo", "apt-get", "update", "-q"])
        run(["sudo", "apt-get", "install", "-yq", *apt])

    pip("install", "-U", "pip", "setuptools", "wheel")
    if "install" in p:
        run(p["install"], cwd=src, shell=True)
    else:
        default_install(p, src)
    pip("install", "pytest", *p.get("deps", []))
    # Force the pint under test, overriding any upper pin the project declares.
    pip("install", "-U", *PINT_SPECS[variant])
    run([sys.executable, "-c", "import pint; print('pint', pint.__version__, pint.__file__)"])


def test(p, src):
    cmd = p.get("test", "python -m pytest -ra -q -p no:cacheprovider")
    if p.get("pytest_args"):
        cmd += " " + p["pytest_args"]
    if p.get("qt") or p.get("xvfb"):
        cmd = "xvfb-run -a " + cmd
    print(f"$ {cmd}", flush=True)
    return subprocess.run(cmd, cwd=src, shell=True).returncode


def main():
    name, variant = sys.argv[1], sys.argv[2]
    p = load(name)
    result = {"name": name, "pint": variant, "ref": None, "pint_version": None}
    RESULTS.mkdir(exist_ok=True)
    out = RESULTS / f"{name}-{variant}.json"
    try:
        src, result["ref"] = checkout(p)
        setup(p, src, variant)
        result["pint_version"] = subprocess.check_output(
            [sys.executable, "-c", "import pint; print(pint.__version__)"], text=True
        ).strip()
    except subprocess.CalledProcessError as e:
        print(f"::error::setup failed: {e}")
        result["outcome"] = "error"
        out.write_text(json.dumps(result))
        sys.exit(1)

    code = test(p, src)
    result["outcome"] = "pass" if code == 0 else "fail"
    out.write_text(json.dumps(result))
    sys.exit(code)


if __name__ == "__main__":
    main()
