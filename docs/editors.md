# Editor Tooling

This page covers the editor setup and daily editor roles for this machine.

The setup order lives in [setup.md](setup.md). This page explains what "Bring up editors" means in practice.

## Treat Neovim as the default editor

For this setup, `nvim` is the editor of record.

That is not just a preference. `EDITOR` is `nvim`, the Python tooling docs already assume that, and the rest of the machine setup should not quietly drift toward a different default.

Neovim is the main daily editor because it fits the shell-first workflow this machine is built around:

- it works cleanly from the terminal
- it matches the managed dotfile setup
- it fits well with project-local `.venv` environments, `uv`, `just`, and `direnv`

This does not mean every task must happen in Neovim. It means the machine should always be in a good state for Neovim first, and other editors should fit around that instead of replacing it.

For Neovim-specific keybindings and usage notes, use [../nvim.md](../nvim.md). This page is about machine bring-up and editor roles, not a full Neovim reference.

## Keep editor configuration in chezmoi

Editor configuration on this machine should come from managed dotfiles through `chezmoi`.

That includes the practical rules:

- do not hand-edit live editor config under `~/.config` and then forget how the machine got there
- update the managed `chezmoi` source instead
- re-apply the managed config with `chezmoi apply`

This matches the rest of the machine docs: `chezmoi` is the source of truth for shell, editor, and related machine configuration.

For Python specifically, [python.md](python.md) already establishes an important boundary: the Neovim Python host is managed separately through `chezmoi`, and it should be treated as editor plumbing rather than as a shared project environment.

## Bring up editors after the machine bootstrap

Editor setup belongs after the machine-level bootstrap steps are in place:

1. apply the managed dotfiles with `chezmoi`
2. install the standard packages and apps from the normal machine setup
3. install Python tooling and any interpreters you actually need
4. then verify that the editors can open real projects in the state this machine expects

That order matters.

If you start customizing editors before `chezmoi`, `uv`, the shell config, and the rest of the package set are in place, you end up debugging the bootstrap in the wrong layer. Bring the machine into its normal managed state first, then check the editor experience.

In practice, that usually means:

- `EDITOR` should already resolve to `nvim`
- Neovim config should already be present from `chezmoi`
- project-local Python environments should come from `uv sync`
- GUI editors should point at the same repository and the same local project environment instead of inventing their own parallel setup

## Use Neovim as the main daily editor

Neovim is the default path for everyday editing on this machine.

Use it for normal repository work, shell-driven editing, quick iteration, and the workflows that already assume `EDITOR=nvim`.

That also makes the machine setup more coherent:

- terminal and editor workflows stay aligned
- editor launch from the shell works the same way across repositories
- project commands and editor usage both stay close to the repo-local environment

If Neovim is not working well on a fresh machine, fix that first. Do not treat PyCharm, VS Code, or Zed as the fallback that quietly becomes the real default.

## Use PyCharm when IDE-heavy help is worth it

PyCharm is a real part of this setup, but it is a secondary editor rather than the machine default.

Its main role here is occasional IDE-heavy work, especially when the pytest integration or broader IDE assistance is worth the extra weight.

That makes it useful for tasks like:

- exploring a larger test suite in a more IDE-oriented view
- using pytest support when that is more convenient than the shell and Neovim
- occasional debugging or refactoring work where a full IDE helps

The important constraint is that PyCharm should still fit the machine's normal project model:

- open the repository you are actually working on
- use the local project environment created by `uv sync`
- keep project truth in the repository, not in editor-specific hidden state

PyCharm is useful here because it is different from Neovim, not because it should become the new baseline for every project.

## Use VS Code as an occasional compatibility check

VS Code is useful on this machine mostly as a comparison and compatibility tool.

Sometimes it is helpful to see how a project behaves in the editor many other people are likely to use. That can matter when checking workspace behavior, extension expectations, or whether a repository feels reasonable outside the primary Neovim workflow.

That is the right level to treat it at in this setup:

- open the project
- check how it behaves there
- verify that nothing important depends on Neovim-specific assumptions

VS Code is not the editor this machine is centered on, and this page does not try to turn it into one.

## Use Zed as a lightweight graphical editor

Zed fills a different role from PyCharm.

Use it when you want a graphical editor that feels lighter and simpler than a full IDE.

That makes it a good fit for cases where you want:

- a GUI window without bringing in full IDE behavior
- quick edits outside the terminal workflow
- a second graphical view on a repository without changing the overall machine defaults

In other words, Zed is closer to "simple graphical editor" than "alternate IDE strategy" in this setup.

## Keep the project workflow consistent across editors

The machine-level rule is simple: editors may differ, but the project workflow should not.

Across Neovim, PyCharm, VS Code, and Zed, the underlying project conventions stay the same:

- use the repository root as the working directory
- create or update the local environment with `uv sync`
- use the repository's checked-in project metadata and lockfile
- respect `direnv` and other repo-local workflow files instead of replacing them with ad hoc editor setup

That consistency matters more than chasing feature parity between editors.

## Verify editor setup with a real project

The editor setup is not done when apps are installed. It is done when the default editor and the secondary tools can open a real repository without fighting the machine setup.

Start with the default path:

```sh
echo $EDITOR
command -v nvim
cd ~/projects/django-cast
uv sync
nvim .
```

From there, confirm the important basics:

- `EDITOR` prints `nvim`
- Neovim starts with the managed config in place
- the repository opens normally from the shell
- Python project work still uses the repo-local environment created by `uv`

Inside Neovim, `:checkhealth` is the practical first readback if something looks wrong.

If you use the secondary editors on the machine, open the same repository in PyCharm, VS Code, or Zed after the Neovim check and confirm that they can work with the same checkout cleanly. Treat that as a secondary verification step, not the primary definition of success.

## Summary

The active editor setup for this machine is straightforward:

1. keep `nvim` as the default editor
2. keep editor configuration in `chezmoi`
3. use PyCharm, VS Code, and Zed intentionally for the cases where they add value
4. keep the project workflow centered on repo-local environments and managed machine configuration
5. verify the setup with a real project, starting with Neovim

That keeps the editor story honest: Neovim is the main path, the GUI editors are useful secondary tools, and the machine stays coherent because configuration still comes from `chezmoi`.
