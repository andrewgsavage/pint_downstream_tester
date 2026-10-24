.. image:: https://github.com/andrewgsavage/pint_downstream_tester/actions/workflows/downstream.yml/badge.svg
    :target: https://github.com/andrewgsavage/pint_downstream_tester/actions/workflows/downstream.yml


Pint Downstream Tester
======================

This repository tests projects that use `Pint <https://github.com/hgrecco/pint>`_
against both the latest Pint release and Pint master, to catch changes in Pint
that break downstream code before they are released.

The projects tested are listed in ``projects.toml``; ``downstream_candidates.md``
describes each one and how the list was chosen.


How it works
------------

The ``downstream`` GitHub Actions workflow runs nightly, on pushes to master and
on pull requests. For every project it runs two jobs, one with the latest Pint
release and one with Pint master. Each job:

1. clones the project at its latest GitHub release (or default branch if it has none),
2. installs it with its test dependencies,
3. force-installs the Pint under test, overriding any version pin the project has,
4. runs the project's test suite.

The run summary has a table of results and lists any project that passes with
the Pint release but fails with master.

To run a subset, or test a different Pint branch or fork, start the workflow by
hand with its ``filter``, ``pint_repo`` and ``pint_ref`` inputs.

To run one project locally::

    python scripts/run_project.py pint-pandas master


Adding a project
----------------

Add an entry to ``projects.toml``::

    [[project]]
    name = "pint-pandas"
    repo = "hgrecco/pint-pandas"

Most projects need nothing else. Optional fields:

``ref``
    Tag or branch to test. ``"release"`` (default) uses the latest GitHub
    release, ``"default"`` uses the default branch.
``url``
    Clone URL, for projects not hosted on GitHub.
``python``
    Python version (default 3.12).
``extras``
    Extra pip extras to install the project with.
``deps``
    Additional pip packages to install.
``apt``
    Ubuntu packages to install.
``qt``
    ``true`` to install Qt system libraries and run tests under ``xvfb``.
``install``
    Shell command replacing the default install. ``$DOWNSTREAM_REF`` holds the
    checked-out tag.
``test``
    Shell command replacing the default ``python -m pytest -ra -q``.
``pytest_args``
    Arguments appended to the test command.
``submodules``
    ``true`` to clone git submodules.
``skip``
    Reason the project is not run; it is listed in the run summary instead.
