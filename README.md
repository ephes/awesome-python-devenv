# Python Development Environment [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)

Just a collection of tips and tools to improve your python development
experience inspired by
[this blogpost](https://jacobian.org/2019/nov/11/python-environment-2020/).

Since the escape key is back, it's now possible to use macbooks as development
machines again. So I got one and had to redo my python development setup. After
some time I thought that I should write down the required steps, because
otherwise I would have to google this stuff all over again next time. After
some more time I thought that it might be a good idea to publish those steps.
Because I clearly have no clue what I'm doing and just asking for help wouldn't
be as effective as posting the wrong answer and waiting for a poor soul to take
the bait. So here we are :).

# macOS

The macOS specific stuff has [pages of its own](docs/setup.md) in the `docs/` directory, with the setup order in [docs/setup.md](docs/setup.md) and the machine-level details in [docs/machine.md](docs/machine.md).

# Vibe Coding (Remote Dev with tmux/zellij)

SSH into a remote machine, use tmux or zellij for persistent sessions, and sync
code with vsync. The full workflow and keybindings are on a
[page of their own](vibe-coding.md).

# Neovim / LazyVim

Keybindings and tips for Neovim with LazyVim are on a
[page of their own](nvim.md).

# Shell

This setup uses `fish` directly and keeps shell configuration in dotfiles.

# Python

## Update Python

The current setup uses `uv` only for Python installation and project-local
virtual environments.

Install or update Python with `uv` and create project-local virtual
environments as needed:

```shell
$ uv python install 3.14
$ uv venv
```

# Getting A Django Project Up And Running

## Environment Variables

This setup uses [direnv](https://direnv.net/) for project-specific environment
variables. The fish shell config is managed in dotfiles and loads `direnv`
automatically when it is installed.

For a project, put the environment setup in `.envrc` and allow it once:

```shell
$ direnv allow
```

A simple `.envrc` might look like this:

```shell
export DJANGO_SETTINGS_MODULE=config.settings.local
export DATABASE_URL=postgres:///myproject
```

# Using fzf

[fzf](https://github.com/junegunn/fzf) is a really great tool, and the
most enjoyed recent addition to my toolbelt.

Install it with Homebrew:

```shell
$ brew install fzf
$(brew --prefix)/opt/fzf/install  # install useful key bindings and fuzzy completion
```

The active `fzf` shell configuration lives in the managed fish dotfiles rather
than in an ad hoc local shell config edit.

Here are some examples on how to use it:

```shell
$ vim (fzf)  # search for file and open in Neovim
$ history | fzf +s --tac  # search in history in reverse order and dont sort result
$ fzf --preview 'bat --style=numbers --color=always {} | head -500'  # use fzf with bat preview
```

# Useful Command Line Tools

The current CLI tool set is defined in the managed global Brewfile rather than
as a separate hand-maintained list. On the machine this is `~/.Brewfile`; in
the chezmoi source it is `dot_Brewfile`.

Cask apps are also part of the Brewfile but are intentionally not listed here.

Current Brewfile `brew` packages:

- `age`, `asciinema`, `ast-grep`, `bat`, `bfg`, `chezmoi`, `cloc`
- `colima`, `composer`, `coreutils`, `direnv`, `docker`, `docker-compose`, `docker-buildx`, `podman`
- `duf`, `duti`, `eza`, `fd`, `ffmpeg`, `fish`, `fzf`
- `git-delta`, `gh`, `glab`, `gnu-sed`, `go`, `gource`, `graphviz`
- `hexyl`, `htop`, `imapsync`, `influxdb`, `jpegoptim`, `just`
- `lazygit`, `libmemcached`, `libxmlsec1`, `luarocks`
- `mosh`, `most`, `multitail`
- `neofetch`, `neovim`, `nmap`, `node`, `ntopng`
- `opencode`, `openjdk@17`, `openssl@3`, `optipng`
- `pandoc`, `php`, `pngpaste`, `pnpm`, `poppler`, `postgresql@17`, `pwgen`
- `ruby`, `ripgrep`, `rsync`
- `sloccount`, `slurm`, `sops`, `starship`
- `telnet`, `tig`, `tldr`, `tmux`, `tree`
- `uv`, `vim`
- `wget`, `whisper-cpp`
- `yq`, `yt-dlp`
- `zellij`, `zoxide`

# Sources

Further books, podcasts, newsletters, and videos live on a
[page of their own](sources.md).
