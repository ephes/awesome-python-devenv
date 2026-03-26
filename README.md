# Python Development Environment [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)

This repository documents the current macOS Python development setup for this
machine.

It started as a collection of notes inspired by
[this blogpost](https://jacobian.org/2019/nov/11/python-environment-2020/), but
the useful part now is the documented workflow: machine bootstrap, Python
tooling, container setup, editor roles, and a few companion reference pages.

# Start Here

If you are setting up a new machine, start with the docs in `docs/`:

- [docs/setup.md](docs/setup.md) for the setup order
- [docs/machine.md](docs/machine.md) for machine-level bootstrap details
- [docs/python.md](docs/python.md) for the active Python workflow
- [docs/containers.md](docs/containers.md) for container runtime setup
- [docs/editors.md](docs/editors.md) for editor bring-up and editor roles
- [docs/cli-tools.md](docs/cli-tools.md) for the everyday command-line tools

# Current Setup

The current machine-level conventions are straightforward:

- shell and editor configuration are managed through `chezmoi`
- `fish` is the shell
- `uv` is the Python toolchain manager
- project environments stay local to each repository
- `nvim` is the default editor
- PyCharm, VS Code, and Zed are secondary tools with narrower roles
- `colima` is the default macOS container runtime

Detailed tool usage should live in the topical docs or in dedicated reference
pages, not as a second hand-maintained setup guide inside the README.

The CLI inventory also lives in the managed Brewfile rather than in this file.
On the machine that is `~/.Brewfile`; in the `chezmoi` source it is
`dot_Brewfile`.

# Other Pages

- [coding-agents.md](coding-agents.md) for coding-agent links and references
- [nvim.md](nvim.md) for Neovim / LazyVim keybindings and usage notes
- [docs/cli-tools.md](docs/cli-tools.md) for the curated CLI tool overview
- [vibe-coding.md](vibe-coding.md) for remote development with tmux or zellij
- [sources.md](sources.md) for books, podcasts, newsletters, and videos
