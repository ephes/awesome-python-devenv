# Setup a New Mac

This page is the chronological checklist for bringing up a new Mac for development.

Use it for order. Use the linked topical pages for the details.

## 1. Update macOS

Install the latest available macOS updates first and reboot if required.

Why: it reduces avoidable installer and compatibility problems later in the setup.

## 2. Apply essential macOS settings

Apply the macOS settings that immediately reduce friction, starting with keyboard repeat rate, Dock behavior, wallpaper, iCloud sync preferences, and Space behavior.

If tmux uses `Ctrl+Space` as its prefix, disable the macOS Input Sources shortcuts early as part of this step so the prefix reaches the terminal.

Why: some defaults are annoying enough that they make the rest of the setup harder than it needs to be.

Details: [machine.md](machine.md#apply-essential-macos-settings-early)

## 3. Install Xcode Command Line Tools

Install Apple's command line developer tools before Homebrew:

```sh
xcode-select --install
```

Why: many development tools assume the Apple compiler toolchain and SDK are already present. Installing this early avoids bootstrap failures later.

Details: [machine.md](machine.md#install-xcode-command-line-tools-before-homebrew)

## 4. Install Homebrew

Install Homebrew after the command line tools are in place.

Why: Homebrew is the package bootstrap for the rest of the machine setup.

Details: [machine.md](machine.md#install-homebrew)

## 5. Set up SSH access

If your dotfiles repo is private, create a machine-specific SSH key and add the public key to your Git host before initializing `chezmoi`.

Why: `chezmoi init` needs repository access, and a new machine should generally get its own SSH key instead of reusing an old private key.

Details: [machine.md](machine.md#set-up-ssh-access-before-chezmoi)

## 6. Install chezmoi and apply dotfiles

Install `chezmoi`, initialize your dotfiles repo, and apply the managed configuration as early as possible.

Why: chezmoi is the source of truth for shell, editor, and other machine configuration.

If the dotfiles repo contains encrypted files, configure SOPS decryption before running `chezmoi apply`.

Why: encrypted managed files cannot be rendered or applied until the decryption identity is available on the machine.

Details: [machine.md](machine.md#install-chezmoi-early)
SOPS details: [machine.md](machine.md#configure-sops-before-applying-encrypted-dotfiles)

## 7. Install packages and CLI tools

Run the Homebrew package install step, including your Brewfile-managed dependencies, before changing shells or editor settings.

Why: this provides the baseline tools the rest of the workflow expects, including `fish`.

Details: [machine.md](machine.md#install-packages-and-cli-tools)

## 8. Switch the login shell to fish

After the Brewfile/package install step has installed `fish`, change the login shell before spending time in a new terminal setup.

Why: the shell should match the managed machine configuration before daily terminal use starts.

Details: [machine.md](machine.md#switch-the-login-shell-to-fish)

## 9. Configure Mail

Configure Mail once the main machine setup is in place.

Why: this is part of the normal new-Mac setup, but it is a manual account step rather than a documented tooling workflow here.

## 10. Install MonoLisa

Install MonoLisa before settling into the terminal and editor setup.

Why: this setup uses MonoLisa as the main terminal and editor font, so installing it early avoids doing visual setup work twice.

Details: [machine.md](machine.md#install-monolisa-manually)

## 11. Set up backup

Set up the backup strategy for the new Mac.

Why: backup is part of the normal machine setup and should be in place before the machine starts accumulating important local state.

For this setup, that includes mounting the SMB share used for backups with the user `timemachine`.

## 12. Bring up Python tooling

Install and verify the Python development stack.

Why: this enables project work after the machine-level tools are ready.

Details: [python.md](python.md)

## 13. Bring up container tooling

Install and verify your container runtime and related tooling.

Why: container tooling is part of the standard new-Mac workflow for this setup.

Details: [containers.md](containers.md)

## 14. Bring up editors

Install editors and ensure their configuration comes from your managed dotfiles.

Why: editor setup should follow the machine bootstrap so config and plugins land in the expected place.

Planned detail page: `docs/editors.md`

## 15. Verify with a real project

Open an existing project, confirm shell configuration loads, confirm Python works, and confirm container tooling works where needed.

Why: the setup is only complete when a real project starts cleanly.
