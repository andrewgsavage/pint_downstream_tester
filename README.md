# Pint Downstream Tester

[![Downstream tests](https://github.com/andrewgsavage/pint_downstream_tester/actions/workflows/downstream.yml/badge.svg)](https://github.com/andrewgsavage/pint_downstream_tester/actions/workflows/downstream.yml)

Runs the test suites of projects that depend on [Pint](https://github.com/hgrecco/pint)
against Pint `master`, to catch backwards-incompatible changes before they are released.

Each project is tested twice: against Pint `master` and against the latest Pint release
the project allows. Many pinned releases have some tests that fail regardless of Pint
(newer numpy or pandas, network access, missing solvers), so results are compared test by
test: only tests that fail with `master` but pass with the release point at a Pint
regression.

## Projects tested

Listed in [`projects.toml`](projects.toml). [`downstream_candidates.md`](downstream_candidates.md)
describes each one and how they were chosen.

To add a project, add a `[[project]]` entry there; CI picks it up automatically.

## Running locally

Requires Python 3.11+ and git. Uses [uv](https://docs.astral.sh/uv/) if installed.

```bash
python run_downstream.py                      # every project, Pint master
python run_downstream.py pint-xarray          # one project
python run_downstream.py --pint release       # baseline against released Pint
python run_downstream.py --pint-ref my-branch # a Pint branch, tag or SHA
```

Projects marked `qt = true` need a display; locally they run without `xvfb`.
Projects with a `python` key need uv, which creates an environment for that version.

## CI

GitHub Actions runs on pushes, pull requests, weekly, and on demand
(*Actions → Downstream tests → Run workflow*, optionally with a Pint ref and a regex
of project names to test). The Pint ref is resolved to one commit at the start of the run,
so every job tests the same Pint.

Test jobs only fail when a project can't be installed. The `summary` job compares each
project's failing tests under both Pint versions, lists the tests that fail only with
`master`, and fails the run if there are any. Each test has a 10-minute limit and each
job a 60-minute limit.
