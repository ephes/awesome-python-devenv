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

The example libraries' `develop` metadata was checked on 2026-11-07:

- [django-cast](https://github.com/ephes/django-cast/blob/develop/pyproject.toml) declares `requires-python = ">=3.11"`.
- [django-indieweb](https://github.com/ephes/django-indieweb/blob/develop/pyproject.toml) declares `requires-python = ">=3.11"`.

These are package minimums, separate from this machine's preferred interpreter. Check the linked metadata and each repository's test matrix for the checkout you are using; these examples do not freeze upstream compatibility.

For this machine, Python `3.14` is the current default interpreter to have available locally. `EDITOR` is `nvim`, and the Neovim Python host is managed separately through `chezmoi`. Treat that host interpreter as editor plumbing, not as a shared project environment.

For Python CLI tools that are not tied to one repository, use `uv tool install` or `uvx` instead of `pipx`.

- `uv tool install <package>` is the persistent install path for a reusable CLI
- `uvx <tool> ...` is the one-shot execution path when you do not want to keep the tool installed

That keeps Python tool installation in the same toolchain instead of splitting the workflow between `uv` and a second installer.

## Keep environments local to each project

The expected project shape is a repository with a checked-in `pyproject.toml`, plus a local `.venv` created inside the repository. Whether `uv.lock` is committed follows the [repository's lockfile policy](#follow-the-repositorys-lockfile-policy).

In normal use, you do not need to create the environment manually first. Run:

```sh
uv sync
```

That gives you the standard local environment for the current checkout and installs the dependencies declared by the project metadata.

This setup prefers a project-local `.venv` over one big shared environment because it keeps dependencies isolated, makes editor integration predictable, and matches how the example projects already work.

If you ever need an empty environment before syncing, `uv venv` is still available, but the common workflow here is `uv sync`, not hand-building environments and then populating them with ad hoc `pip` commands.

## Sync dependencies from project metadata

`uv sync` is the baseline command after cloning a project, switching branches, or pulling dependency changes.

It reads the dependency declarations from `pyproject.toml`, creates or updates `uv.lock` as needed, and updates the local `.venv` to match. A repository may commit that resolution or keep it local; follow its own instructions after switching branches or changing metadata.

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
- `django-indieweb` uses `uv run` for `pytest`, `mypy`, `ruff`, documentation generation, and `prek` hooks.

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

## Follow the repository's lockfile policy

For applications in this setup, commit `uv.lock` alongside `pyproject.toml` and update both when dependency metadata changes. The lockfile records the resolved dependency set so fresh clones and existing checkouts can use the same graph.

Libraries can choose a different policy. The two examples do not share one committed-lock convention (checked on 2026-11-07):

- `django-cast` does not track `uv.lock`: it tests several supported Django and Wagtail branches. Follow its [development environment and audit instructions](https://github.com/ephes/django-cast/blob/develop/docs/development.rst#setting-up-the-python-environment). In that checkout, resolve locally, then audit the runtime resolution including optional extras:

```sh
uv sync
just audit-dependencies
```

- `django-indieweb` tracks [`uv.lock`](https://github.com/ephes/django-indieweb/blob/develop/uv.lock) for reproducible release dependency review, as described in its [development guide](https://github.com/ephes/django-indieweb/blob/develop/docs/development.rst#building-and-publishing-releases).

Keep dependency declarations in `pyproject.toml`; follow each repository's resolution, audit, and lockfile-update instructions rather than changing its policy to match this machine guide.

## Use direnv for project variables, not for Python version management

`direnv` is part of the normal shell setup on this machine, and it fits cleanly alongside `uv`.

The division of responsibility is simple:

- `uv` manages Python interpreters, the local `.venv`, and Python command execution.
- `direnv` loads project-specific environment variables when you enter the repository.

If a project has an `.envrc`, inspect it and allow it once per checkout:

```sh
direnv allow
```

After that, the shell loads the file automatically when you `cd` into the project.

For example, `django-indieweb` tracks an [`.envrc`](https://github.com/ephes/django-indieweb/blob/develop/.envrc) for `BEADS_NO_DAEMON`, `BEADS_DIR`, `BEADSFLOW_CONFIG`, and related helper variables. `django-cast` does not track an `.envrc`; a local one is optional.

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

`django-cast` is the better primary verification target because it exercises more of the stack. Complete its [development setup](https://github.com/ephes/django-cast/blob/develop/docs/development.rst) first, including JavaScript dependencies and the example database. From your existing `develop` checkout (allow `direnv` first if you have a local `.envrc`):

```sh
uv sync
just check
just dev
```

That verifies several important things at once:

- the shell loads project variables correctly, if configured
- the project environment resolves and syncs cleanly
- `ruff`, `mypy`, and `pytest` run through the local environment
- the repository's normal task entry points work
- the Django development server can start through the expected workflow

For a smaller second check, from your existing `django-indieweb` `develop` checkout:

```sh
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
6. Keep `pyproject.toml` under version control and follow the repository's lockfile policy.

That is the current setup. If future docs or project templates contradict it, the docs or templates should be updated rather than reviving older tooling patterns.
