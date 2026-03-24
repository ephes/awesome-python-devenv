# CLI Tools

This page covers the everyday command-line tools that support the workflow on
this machine.

The setup order lives in [setup.md](setup.md). This page is not another package
install guide. It explains which CLI tools matter in daily use, what role they
play, and where they fit relative to the other topical docs.

## Keep the package list in the managed Brewfile

The actual machine-level package inventory lives in the managed global Brewfile,
not in this page.

On the machine that is `~/.Brewfile`; in the `chezmoi` source it is
`dot_Brewfile`.

That is the source of truth for what gets installed. This page is the curated
overview of the tools that are worth remembering and using.

## Use a small set of CLI tools heavily

This setup has a lot of packages available, but the important point is not
"install everything." The important point is to have a small set of reliable
tools that make navigation, search, project entry, and day-to-day shell work
faster.

The core ones for this machine are:

- `direnv` for project-specific environment variables
- `zoxide` for jumping to frequently used directories
- `fzf` for interactive fuzzy selection
- `fd` for fast file discovery
- `rg` for fast content search
- `bat` for readable file previews
- `btop` for interactive system and process inspection
- `eza` for directory listings
- `just` for human-friendly project task entry points

Other tools exist in the Brewfile, but these are the ones that most directly
shape the interactive shell workflow.

## Use direnv for project-local variables

`direnv` is part of the normal workflow on this machine.

Its job is narrow and important: load project-specific environment variables
when you enter a repository.

That means:

- use `.envrc` for repository-local environment setup
- run `direnv allow` once per checkout when needed
- keep `direnv` focused on project variables rather than using it as a second
  Python environment manager

For the Python-specific boundary and examples, see
[python.md](python.md#use-direnv-for-project-variables-not-for-python-version-management).

## Use zoxide for directory navigation

`zoxide` is the everyday replacement for manually typing the same long paths
over and over.

Use it to jump back into frequently used repositories and workspaces quickly.

The point is not that it is clever. The point is that it removes friction from
moving around the filesystem, which matters when most work still starts in the
shell.

## Use fzf for interactive selection

`fzf` is the general-purpose interactive selector in this setup.

Use it when you want fuzzy selection instead of manually typing or scrolling
through long lists.

Typical uses include:

- picking files to open
- searching shell history
- narrowing down command output interactively

The exact keybindings and shell wiring belong in the managed dotfiles. Do not
treat this page as the source of truth for live shell configuration.

## Use fd and rg as the default search tools

For normal shell work on this machine:

- use `fd` when you are searching for files by name or path
- use `rg` when you are searching file contents

That is the expected baseline. They are faster and more pleasant than falling
back to older default tools for the same jobs.

This repository itself follows that pattern in practice.

## Use bat and eza for readable output

`bat` and `eza` are quality-of-life tools rather than workflow owners, but they
pull their weight.

- `bat` is the nicer default for file preview in the terminal
- `eza` is the nicer directory listing tool

Use them where they make terminal output easier to scan, but keep scripts and
shared commands conservative when plain `cat` or `ls` is the more portable
choice.

## Use btop for interactive system inspection

`btop` is the preferred full-screen system monitor in this setup.

Use it when you want a quick interactive view of CPU load, memory usage, and
the current process list without dropping into Activity Monitor or stitching
together several shell commands.

For process inspection, `btop` is usually the first thing to open when the
machine feels slow or a runaway process needs to be identified.

For the current keybindings and sort controls, use `h` inside `btop` to open
the built-in help instead of relying on stale notes here.

## Use just as the project command surface

`just` belongs in this page because it is part of the everyday CLI workflow,
even though its project-specific role is covered more fully in
[python.md](python.md#treat-just-as-the-human-friendly-entry-point).

The practical split is:

- use raw commands when you are exploring
- use `just` recipes for the repeated commands that define normal project work

That keeps repository workflows readable without forcing people to remember a
pile of shell aliases.

## Keep the workflow coherent across tools

These tools should fit together cleanly instead of each creating their own
workflow silo.

In practice that means:

- `fish` is the shell
- `direnv` loads project variables
- `zoxide` gets you to the right repository quickly
- `fd`, `rg`, and `fzf` help you find what you need
- `just` gives the repository a stable command surface

That is the real value of the tool set on this machine. The tools are useful on
their own, but they are more useful because they work together.

## Verify the CLI workflow on a fresh machine

After the Brewfile install step and `chezmoi apply`, check the shell tools in a
real session instead of assuming package installation was enough:

```sh
command -v fish
command -v direnv
command -v zoxide
command -v fzf
command -v fd
command -v rg
command -v btop
command -v just
```

Then verify the normal project flow with a real repository:

```sh
cd ~/projects/django-cast
direnv allow
just check
```

That confirms several important things at once:

- the shell environment is in place
- the normal CLI tools are available
- `direnv` still fits the project workflow
- the repository's main task entry points work as expected

## Summary

The useful CLI story for this machine is straightforward:

1. install the packages from the managed Brewfile
2. keep shell configuration in `chezmoi`
3. use a small set of tools heavily instead of documenting everything
4. treat `direnv`, `zoxide`, `fzf`, `fd`, `rg`, and `just` as the everyday core
5. verify the workflow with a real project, not only with package installation

That keeps this page focused on the tools that actually shape daily work instead
of turning it into a dump of every package on the machine.
