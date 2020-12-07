# macOS

Since the escape key is back, it's now possible to use macbooks as development
machines again. So I got one and had to redo my python development setup. After
some time I thought that I should write down the required steps, because
otherwise I would have to google this stuff all over again next time. After
some more time I thought that it might be a good idea to publish those steps.
Because I clearly have no clue what I'm doing and just asking for help wouldn't
be as effective as posting the wrong answer and waiting for a poor soul to take
the bait. So here we are :).

## Installing Software / Package Management

Since there's no builtin package manager in macOS, one of the first things I
usually do is to install [homebrew](https://brew.sh).

```shell
$ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"
```

For M1 Macs use rosetta2:
```shell
softwareupdate --install-rosetta
arch -x86_64 /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install.sh)"
```

### Things I usually install via Homebrew

```shell
brew install \
    fd \
    fzf \
    bat \
    tree \
    wget \
    tldr \
    tmux \
    fish \
    pyenv \
    slurm \
    gource \
    pandoc \
    ntopng \
    ripgrep \
    postgres \
    git-flow \
    neofetch \
    asciinema \
    multitail \
    gitversion \
    pyenv-virtualenv
```

## Terminal / Shell
### Terminal

iTerm2 got it's [onw page](iterm.md) now.

### Shell
The default macOS terminal is not as bad as it used to be, but I still like to
use [iTerm2](iterm.md). I
used [bash](https://www.gnu.org/software/bash/) as shell for a long time but
got adventurous in the past few years and went from
using [zsh](https://www.zsh.org/) to [fish](https://fishshell.com/):

```shell
$ brew install fish
$ sudo sh -c "echo /usr/local/bin/fish >> /etc/shells"
$ chsh -s /usr/local/bin/fish
```

I like fish quite a lot, but it still feels weird not using bash. Where's my
beloved ctrl + r for example (found a [solution using
fzf](https://github.com/junegunn/fzf#key-bindings-for-command-line)?  With zsh
it was the same - tabcompletion just felt different. Yes, it probably was
better in some cases, but it wasn't the same. Also just pressing return is a
lot faster in bash than in zsh or fish and I don't know why.

## Fixing Things Broken By Default

### Keyboard Key Repeat Rate

This one drives me crazy. The default key repeat rate is just way too slow.
Computers are unbelievable fast nowadays and watching them paint letter after
letter to the terminal seemingly unable to keep up with the typing speed of a
puny human is just embarrassing.

```shell
$ defaults write -g InitialKeyRepeat -int 10
$ defaults write -g KeyRepeat -int 1
```

You have to logout / login (not just from your shell but from your macOS UI)
for those changes to take effect.

### Xcode Command Line Tools

A lot of essential header files are missing and you wont be able to compile a
lot of software unless you install those:

```shell
$ xcode-select --install
```

Now you also have to notify the compiler about where those headers are, because
since catalina /usr is read only and you cant link them just there. I'm putting
a line in ~/.config/fish/config.fish to set  CPATH, but I don't know whether
that's the proper way to do it:

```shell
# header files for gcc from apple command line tools
set -x CPATH $CPATH (xcrun --show-sdk-path)/usr/include
```

While we're already at setting environment variables - the openssl package from
homebrew is keg-only, which means it is not linked into /usr/local because it
otherwise would mask the openssl/libressl system installation from macOS. But
since I need the homebrew package (for installing psycopg2 for example) I have
to set following variables in~/.config/fish/config.fish, too:

```shell
# enable compiling against homebrew openssl
set -gx LDFLAGS "-L/usr/local/opt/openssl@1.1/lib"
set -gx CPPFLAGS "-I/usr/local/opt/openssl@1.1/include"
set -gx PKG_CONFIG_PATH "/usr/local/opt/openssl@1.1/lib/pkgconfig"
```
