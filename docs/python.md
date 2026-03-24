# Python Tooling

This page covers the Python-specific setup and daily workflow for this machine.

The setup order lives in [setup.md](setup.md). This page explains what "Bring up Python tooling" means in practice.

## Use uv as the Python toolchain manager

This setup uses `uv` for Python installation, project environments, dependency syncing, and command execution.

That is the whole workflow. Do not reintroduce `pyenv`, `pipx`, `virtualfish`, Poetry, or `pip install --user` as the normal path on this machine.

`uv` is installed as part of the machine bootstrap. Once it is present, use it to install the Python versions you actually need:

```sh
uv python install 3.14
```

`django-cast` currently declares `requires-python = ">=3.11"` and `django-indieweb` declares `requires-python = ">=3.10"` in `pyproject.toml`, so both projects fit naturally into the same `uv`-managed workflow.

For this machine, Python `3.14` is the current default interpreter to have available locally. `EDITOR` is `nvim`, and the Neovim Python host is managed separately through `chezmoi`. Treat that host interpreter as editor plumbing, not as a shared project environment.

For Python CLI tools that are not tied to one repository, use `uv tool install` or `uvx` instead of `pipx`.

- `uv tool install <package>` is the persistent install path for a reusable CLI
- `uvx <tool> ...` is the one-shot execution path when you do not want to keep the tool installed

That keeps Python tool installation in the same toolchain instead of splitting the workflow between `uv` and a second installer.

## Keep environments local to each project

The expected project shape is a repository with a checked-in `pyproject.toml` and `uv.lock`, plus a local `.venv` created inside the repository.

In normal use, you do not need to create the environment manually first. Run:

```sh
uv sync
```

That gives you the standard local environment for the current checkout and installs the dependencies declared by the project metadata.

This setup prefers a project-local `.venv` over one big shared environment because it keeps dependencies isolated, makes editor integration predictable, and matches how the example projects already work.

If you ever need an empty environment before syncing, `uv venv` is still available, but the common workflow here is `uv sync`, not hand-building environments and then populating them with ad hoc `pip` commands.

## Sync dependencies from project metadata

`uv sync` is the baseline command after cloning a project, switching branches, or pulling dependency changes.

It reads the dependency declarations from `pyproject.toml`, uses `uv.lock` as the resolved source of truth, and updates the local `.venv` to match.

That is why both example projects keep their `install` recipe extremely small:

```just
install:
    uv sync
```

This is the expected style for projects in this setup. The project metadata stays in `pyproject.toml`, the fully resolved dependency graph lives in `uv.lock`, and the environment is recreated from those files rather than curated by hand.

## Run project commands with uv run

Use `uv run` to execute Python tools inside the project environment:

```sh
uv run pytest
uv run mypy
uv run ruff check --fix .
uv run ruff format .
```

This keeps the command bound to the project's local environment without requiring manual activation first.

That command style shows up consistently in the real projects:

- `django-cast` uses `uv run` for `pytest`, `coverage`, `mypy`, `ruff`, `pre-commit`, `tox`, Django management commands, documentation builds, and helper scripts.
- `django-indieweb` uses `uv run` for `pytest`, `mypy`, `ruff`, documentation generation, and its local `beadsflow` helpers.

If a command should be reproducible for everyone working on the project, it should usually run through `uv run` directly or through a `just` recipe that wraps `uv run`.

## Use uv tools for global or one-off Python CLIs

Repository work should stay centered on `uv sync` and `uv run`, but some Python CLIs are machine-level tools rather than project dependencies.

For those, use:

```sh
uv tool install <package>
uvx <tool> --help
```

This is the replacement for older `pipx`-style guidance on this machine.

Use `uv tool install` when you want a persistent command available across projects. Use `uvx` when you want to run a tool without adding it to a project or keeping a long-lived install around.

## Keep uv.lock in version control

`uv.lock` is part of the normal project state, not a disposable local artifact.

The lockfile records the exact resolved dependency set that `uv sync` should install. That is what makes fresh clones, CI, and existing local checkouts converge on the same dependency graph.

The example projects both check in `uv.lock`, and both lockfiles also reflect their supported Python ranges:

- `django-cast` locks for `>=3.11` and includes resolution markers for multiple Python versions.
- `django-indieweb` locks for `>=3.10` with its own marker set.

When dependency metadata changes, update the lockfile in the same change. Do not edit the environment first and hope the metadata catches up later.

## Use direnv for project variables, not for Python version management

`direnv` is part of the normal shell setup on this machine, and it fits cleanly alongside `uv`.

The division of responsibility is simple:

- `uv` manages Python interpreters, the local `.venv`, and Python command execution.
- `direnv` loads project-specific environment variables when you enter the repository.

Allow a project's `.envrc` once per checkout:

```sh
direnv allow
```

After that, the shell loads the file automatically when you `cd` into the project.

The example repositories both use `.envrc`, but for project state rather than dependency management:

- `django-cast` exports `SPECSYNC_WORKSPACE_ROOT`.
- `django-indieweb` exports `BEADS_NO_DAEMON`, `BEADS_DIR`, `BEADSFLOW_CONFIG`, and related helper variables.

That is the pattern to keep. Use `.envrc` for environment variables, secrets wiring, and local helper configuration. Do not use it to replace `uv sync`, `uv run`, or the checked-in project metadata.

## Treat just as the human-friendly entry point

This setup expects `just` to be part of the everyday Python workflow, not an afterthought.

`uv` is the engine underneath, but `just` is often the better command surface for repeated tasks because it gives each repository a small, readable set of standard verbs.

Both example projects use the same basic shape:

- `just install` delegates to `uv sync`
- `just lint` runs `ruff`
- `just typecheck` runs `mypy`
- `just test` runs `pytest`
- `just check` composes lint, type checking, and tests

`django-cast` then expands that pattern into richer project workflows:

- `just dev` starts the development stack
- `just docs` rebuilds Sphinx documentation
- `just coverage` opens the HTML coverage report
- `just pre-commit` runs repository hooks
- `just tox` runs multi-environment testing

Its `dev` recipe is also a good example of the boundary between tools:

- `just` provides the stable project command
- `uvx` (one-shot tool execution) starts `honcho` for the multi-process dev setup
- `uv run python manage.py runserver ...` keeps Django itself inside the project environment

`django-indieweb` shows the smaller version of the same idea. The Justfile stays short, but it still gives the project a standard `install`, `check`, `test`, `typecheck`, and `docs` interface, plus a few repository-specific helper commands.

The practical rule is:

- use raw `uv run ...` when you are experimenting or doing one-off work
- add or use `just` recipes for the commands that define the normal project workflow

## Verify with a real project after setup

The machine setup is not done when `uv` is installed. It is done when a real project works end to end.

`django-cast` is the better primary verification target because it exercises more of the stack:

```sh
cd ~/projects/django-cast
direnv allow
uv sync
just check
just dev
```

That verifies several important things at once:

- the shell loads project variables correctly
- the project environment resolves and syncs cleanly
- `ruff`, `mypy`, and `pytest` run through the local environment
- the repository's normal task entry points work
- the Django development server can start through the expected workflow

For a smaller second check, `django-indieweb` should work with the same shape:

```sh
cd ~/projects/django-indieweb
direnv allow
uv sync
just check
just docs
```

If those flows work, the Python tooling on the machine is in the state this setup expects.

## Summary

The active Python workflow for this machine is straightforward:

1. Install interpreters with `uv python install`.
2. Enter a project and allow `direnv` if it has an `.envrc`.
3. Run `uv sync` to create or update the local `.venv`.
4. Use `uv run ...` for direct project commands.
5. Use `just` as the standard task interface for the repository.
6. Keep `pyproject.toml` and `uv.lock` in sync and under version control.

That is the current setup. If future docs or project templates contradict it, the docs or templates should be updated rather than reviving older tooling patterns.
