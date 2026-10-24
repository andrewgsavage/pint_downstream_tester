# Pint Downstream Tester

[![Downstream tests](https://github.com/andrewgsavage/pint_downstream_tester/actions/workflows/downstream.yml/badge.svg)](https://github.com/andrewgsavage/pint_downstream_tester/actions/workflows/downstream.yml)

Runs the test suites of projects that depend on [Pint](https://github.com/hgrecco/pint)
against Pint `master`, to catch backwards-incompatible changes before they are released.

Each project is tested twice: against Pint `master` and against the latest Pint release.
A failure only on `master` points at a Pint regression; a failure on both is a problem
in the downstream project (or its pinned version) itself.

## Projects tested

Listed in [`projects.toml`](projects.toml):

- [pint-xarray](https://github.com/xarray-contrib/pint-xarray)
- [pint-pandas](https://github.com/hgrecco/pint-pandas)
- [pyEQL](https://github.com/KingsburyLab/pyEQL)

To add a project, add a `[[project]]` entry there; CI picks it up automatically.

## Running locally

Requires Python 3.11+ and git. Uses [uv](https://docs.astral.sh/uv/) if installed.

```bash
python run_downstream.py                      # every project, Pint master
python run_downstream.py pint-xarray          # one project
python run_downstream.py --pint release       # baseline against released Pint
python run_downstream.py --pint-ref my-branch # a Pint branch, tag or SHA
```

## CI

GitHub Actions runs on pushes, pull requests, weekly, and on demand
(*Actions → Downstream tests → Run workflow*, optionally with a Pint ref).
