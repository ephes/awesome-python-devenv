# Machine Setup

This page covers the machine-level setup for a new macOS development environment.

The setup order lives in [setup.md](setup.md). This page explains the machine-specific steps in more detail.

## Update macOS first

Before installing developer tools, bring macOS itself up to date and reboot if needed.

This removes a class of avoidable issues caused by outdated system components.

## Apply essential macOS settings early

Apply the settings that immediately make the machine tolerable to use before continuing with the rest of the bootstrap.

### Keyboard repeat rate

For this setup, keyboard repeat rate is one of the first changes:

```sh
defaults write -g InitialKeyRepeat -int 10
defaults write -g KeyRepeat -int 1
```

This usually requires logging out and back in to fully take effect.

### Input Sources shortcuts

If tmux uses `Ctrl+Space` as its prefix, disable the macOS Input Sources shortcuts that capture `Ctrl+Space` before the terminal sees it.

This is a manual setting in System Settings under Keyboard / Keyboard Shortcuts / Input Sources:

- disable `Select the previous input source`
- disable `Select next source in Input menu`

Why: with the default macOS shortcuts still enabled, `Ctrl+Space` may never reach Ghostty, Kitty, or tmux, which makes the tmux prefix appear broken.

### Dock behavior

The Dock should move to the right, auto-hide, and use a bit of magnification:

```sh
defaults write com.apple.dock orientation -string right
defaults write com.apple.dock autohide -bool true
defaults write com.apple.dock magnification -bool true
defaults write com.apple.dock largesize -int 64
killall Dock
```

### Wallpaper

Set the wallpaper to Pro Black as part of the first-day machine setup.

This is documented as a manual preference rather than an automated step unless the actual wallpaper asset becomes part of the managed setup.

### iCloud sync preferences

Enable iCloud Desktop and Documents sync if this machine should keep those folders in iCloud Drive.

This is a manual preference in System Settings:

1. Open `System Settings`
2. Open the Apple Account / iCloud section
3. Open `Drive`
4. Enable `Desktop & Documents Folders`

This is a convenience and storage decision rather than a development-tool bootstrap step, but it belongs early in the new-machine setup because it affects where important files live.

### Spaces behavior

Disable automatic reordering of Spaces.

This is a manual setting in System Settings under Desktop & Dock / Mission Control:

- disable `Automatically rearrange Spaces based on most recent use`

This keeps desktop order stable, which makes keyboard and window-management workflows much less annoying.

These kinds of changes do not need to wait for SSH, Homebrew, or `chezmoi`. If a default setting makes the machine actively unpleasant to use, change it early.

## Rename the machine early

Set the machine name before getting too far into setup so the intended name shows up consistently in macOS sharing, shell prompts, and hostname-based workflows.

Use the same value for the three macOS names unless you have a specific reason to split them:

```sh
sudo scutil --set ComputerName <machine-name>
sudo scutil --set LocalHostName <machine-name>
sudo scutil --set HostName <machine-name>
```

Then verify:

```sh
scutil --get ComputerName
scutil --get LocalHostName
scutil --get HostName
```

`ComputerName` is the user-facing name shown in places like AirDrop and Sharing settings. `LocalHostName` is the Bonjour name used on the local network. `HostName` is the system hostname used by shells and some network tooling.

Using one stable short name keeps prompts, SSH, and machine-to-machine references predictable.

## Install Xcode Command Line Tools before Homebrew

Install Apple's command line developer tools first:

```sh
xcode-select --install
```

Why this comes before Homebrew:

- It provides the Apple compiler toolchain and SDK used by many development tools.
- It reduces the chance of Homebrew or package builds stopping early to request missing system tools.
- It makes later steps like Python and native package installation more predictable.

This is not a hard technical requirement in every case, but it is the safer bootstrap order on a fresh Mac.

## Install Homebrew

Use the current official installer:

```sh
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
```

Homebrew is the base package manager for the rest of this machine setup.

## Set up SSH access before chezmoi

If your dotfiles repo is private, set up SSH access before running `chezmoi init`.

The preferred approach on a new Mac is to create a new machine-specific SSH key, add the public key to your Git host, and use that key for repository access.

For a shared SSH config managed with `chezmoi`, use a stable logical key path across machines and keep the actual private key machine-specific. In practice that means the filename stays the same, but each machine has its own key material at that path.

Example shared SSH config:

```sshconfig
Host github.com
  HostName github.com
  User git
  IdentityFile ~/.ssh/github_personal
  IdentitiesOnly yes
  AddKeysToAgent yes
  IgnoreUnknown UseKeychain
  UseKeychain yes
```

Why this pattern works:

- The SSH config can stay in shared dotfiles.
- Non-macOS machines ignore the macOS-only `UseKeychain` option.
- Each machine can generate its own private key at `~/.ssh/github_personal`.
- Existing explicit service-specific key names like `~/.ssh/company_git` can stay as they are.
- The Git host only sees a normal SSH public key, not a special machine-sharing setup.

If you already use `chezmoi` templates heavily, an OS-specific template is also fine. Otherwise `IgnoreUnknown UseKeychain` keeps the shared config portable with less templating.

Typical flow:

```sh
mkdir -p ~/.ssh
chmod 700 ~/.ssh
ssh-keygen -t ed25519 -f ~/.ssh/github_personal -C "you@example.com"
eval "$(ssh-agent -s)"
ssh-add --apple-use-keychain ~/.ssh/github_personal
pbcopy < ~/.ssh/github_personal.pub
```

Then add the copied public key to your Git host and verify access:

```sh
ssh -T git@github.com
```

Using a new key per machine is usually cleaner than copying an old private key around. Reuse an existing private key only when you explicitly need continuity with existing allowlists or server access.

## Install chezmoi early

Install `chezmoi` right after Homebrew:

```sh
brew install chezmoi
```

Then initialize and apply your managed dotfiles:

```sh
chezmoi init --apply <your-dotfiles-repo>
```

`chezmoi` is the source of truth for machine configuration in this setup. Prefer documenting what a config does and pointing to the managed source instead of copying large snippets into these docs.

## Configure SOPS before applying encrypted dotfiles

If the dotfiles repo includes encrypted files, make sure the machine has the required SOPS decryption setup before running `chezmoi apply`.

The exact key source, storage location, and decryption mechanism depend on how secrets are managed. The important point for bootstrap is simple: `chezmoi` can initialize the repo before SOPS is configured, but applying encrypted files requires the decryption identity to already exist on the machine.

## Install packages and CLI tools

After `chezmoi` has applied the machine configuration, install the standard package set from Homebrew, usually via the managed Brewfile or equivalent bootstrap script.

For a bootstrap-friendly Homebrew global setup, keep the Brewfile at `~/.Brewfile` and use:

```sh
brew bundle --global
```

`brew bundle --global` reads from Homebrew's global locations, such as `${XDG_CONFIG_HOME}/homebrew/Brewfile` if `XDG_CONFIG_HOME` is set, `~/.homebrew/Brewfile`, or `~/.Brewfile`, unless `HOMEBREW_BUNDLE_FILE_GLOBAL` is set.

This step needs to happen before switching the login shell, because tools like `fish` must exist before they can become the default shell.

### Remove packages no longer present in the Brewfile

If packages were previously installed with Homebrew but have since been removed
from the managed global Brewfile, prune them explicitly instead of assuming
`brew bundle --global` will uninstall them.

First preview what would be removed:

```sh
brew bundle cleanup --global
```

Then perform the cleanup:

```sh
brew bundle cleanup --global --force
```

If you prefer a single install-and-prune step during machine maintenance, use:

```sh
brew bundle install --global --cleanup
```

Be careful with cleanup on machines that also have intentionally unmanaged
packages installed via Homebrew, because `brew bundle cleanup` removes anything
not present in the Brewfile for the selected scope.

### Manual installs not covered by Homebrew

Some apps still need manual installation from their official sites:

- [Ivory](https://tapbots.com/ivory/)
- [DigiDoc4 / ID software](https://www.id.ee/en/rubriik/id-software/)
- [FortiClient](https://www.fortinet.com/support/product-downloads#vpn)
- [Aseprite](https://www.aseprite.com/)
- [Bill 2](https://e-bill.app/)
- [LDtk](https://ldtk.io/)
- [Hemingway Editor](https://hemingwayapp.com/)
- [Paprika Recipe Manager](https://www.paprikaapp.com/)
- [REAPER](https://www.reaper.fm/download-old.php?ver=6x)
- [Ultraschall](https://ultraschall.fm/)

`Paprika Recipe Manager` remains a manual install because it is not currently available via Homebrew. `REAPER` is kept as a manual install here because this setup needs version `6.83` from the old-version download page instead of the current Homebrew cask version. `Ultraschall` also remains a manual install.

### Install MonoLisa manually

This setup uses [MonoLisa](https://www.monolisa.dev/) as the main terminal and editor font, so install it manually on a new machine from the MonoLisa download page.

Use Font Book or copy the font files into `~/Library/Fonts`, then restart Ghostty and any GUI editors so they pick up the installed font.

## Switch the login shell to fish

Once the Brewfile or package-install step has installed `fish`, make it the login shell before settling into the terminal workflow.

Use the installed `fish` binary path instead of hard-coding `/usr/local/bin/fish` or `/opt/homebrew/bin/fish`:

```sh
fish_path="$(command -v fish)"
grep -qx "$fish_path" /etc/shells || echo "$fish_path" | sudo tee -a /etc/shells
chsh -s "$fish_path"
```

Then log out and back in, or start a new login session, so macOS and terminal apps pick up the new default shell.

This belongs after the Homebrew package install step because `fish` needs to exist first, but it is worth doing before spending time in Ghostty, terminal configuration, or shell-specific tooling.

## Next machine topics

This page now covers the active machine setup flow. Any remaining legacy flat-file material should either move here in updated form or be deleted once it is no longer useful.
