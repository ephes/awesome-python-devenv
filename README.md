# Python Development Environment 2022 Edition [![Awesome](https://cdn.rawgit.com/sindresorhus/awesome/d7305f38d29fed78fa85652e3a63e154dd8e8829/media/badge.svg)](https://github.com/sindresorhus/awesome)

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

The macOS specific stuff has a [page on it's own](macOS.md).

# Shell

## Package Manager

Using a package manager for your shell makes things a lot easier. You
can get [oh-my-fish](https://github.com/oh-my-fish/oh-my-fish) by typing:

```shell
$ curl -L https://get.oh-my.fish | fish
```

Update your packages and install one:

```shell
$ omf update
$ omf install bobthefish
```

Use a theme from [this list](https://github.com/oh-my-fish/oh-my-fish/blob/master/docs/Themes.md)
of available themes.

```shell
$ omf theme bobthefish
```

If you see strange character appearing in your prompt, you probably have to
installed a powerline patched font. You can install one line this:

```shell
$ omf install fonts
$ fonts install --powerline Inconsolata
```

Maybe you have to restart iTerm and change your font setting for your iTerm profile, too.

## Config

To start the web based fish configuration call:

```shell
$ fish_config
```

# Python

## Update Python

Make sure pyenv is up to date:

```shell
$ cd ~/.pyenv
$ git pull
```

Install new python version:

```shell
$ pyenv install new.version.number
```

Uninstall virtualfish
```shell
$ vf uninstall
$ pipx uninstall virtualfish
```

Use new python version:
```shell
$ pyenv global new.version.number
```

Upgrade pipx
```shell
$ pipx upgrade-all
```

Install virtualfish
```shell
$ pipx install virtualfish
$ vf install compat_aliases projects environment auto_activation
```

## Outdated Stuff
Installing python on macOS (or any other OS I know of) is much more difficult
than you would expect. After using a mixture of system provided python, python
installed by homebrew and python installed by conda I finally settled
using [pyenv](https://github.com/pyenv/pyenv). With pyenv it's easy to install a lot of
different python versions. After that you are able to define which python
version should be used per directory. Even things like pypy or miniconda are
possible. Together with [pyenv-virtualenv](https://github.com/pyenv/pyenv-virtualenv) I
use it for my data science conda environments and my web development
virtualenvs. Environments are automatically switched by entering the respective
project directory:

When installing miniconda3-latest, make sure PYTHON_CONFIGURE_OPTS="--enable-framework"
is not set (you might need this for some vim plugins etc.) otherwise miniconda installation
will fail.

```shell
$ brew install xz pyenv pyenv-virtualenv
```

There should be something like this in .config/fish/config.fish:

```shell
    # pyenv / pyenv-virtualenv
    set -gx PYENV_ROOT $HOME/.pyenv
    set -gx PATH $PYENV_ROOT/bin $PATH
    status --is-interactive; and source (pyenv init -|psub)
    status --is-interactive; and source (pyenv virtualenv-init -|psub)
```

Use a recent python version as system python:

```shell
$ pyenv global 3.9.0
```

### Caveats

* pyenv shims are masking system commands (ffmpeg/ffprobe for me) - I found [pyenv-which-ext](get_rendition_or_not_found) helpful

## Using poetry for packages and dependency management

Install poetry:

```shell
$ curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python3
```

If you used pyenv to create your virtualenv, you have to activate it.
Otherwise poetry will create an own virtualenv on poetry install.

```shell
$ pyenv activate your_env
```

# Getting A Django Project Up And Running

## Database

At first you also have to install postgres via homebrew:

```shell
$ brew install postgresql
$ brew services start postgresql   # to have launchd start postgres
```

To simplify the creation of databases for my projects I created a little helper
fish function and put it into ~/.config/fish/functions:

```shell
function init_django_db
  set user $argv[1]
  set dbname $argv[2]
  dropdb $dbname
  dropuser $user
  createdb $dbname
  createuser $user
  psql -d $dbname -c "GRANT ALL PRIVILEGES ON DATABASE $dbname to $user;"
end
```

Recreating a database and user with access to this database is just a call to
this function:

```shell
$ init_django_db username dbname
```

## Environment Variables

There are usually a lot of environment variables that need to be set for each
project. I usually keep them in an .env file in the root project directory. Now
I only have to make sure those variables get set when I enter the projects
directory and this is done by the following function
in ~/.config/fish/config.fish:

```shell
# on pwd change look for env file and load it
function load_env --on-variable PWD
  if test -e .env
    export (grep -Ev '^\s*$|^\s*\#' .env)
  end
end
```

Yeah, I know about
[autoenv](https://github.com/inishchith/autoenv) and [direnv](https://direnv.net/),
but I'm also
using [python-dotenv](https://github.com/theskumar/python-dotenv) and need to
resolve some compatibility issues first.

## Virtualenv

You should now be able to just clone one of your old django projects from
github for example, create a new virtualenv and install the requirements:

```shell
$ pyenv virtualenv 3.8.1 venv_name
$ cd projects/project_name
$ pyenv local venv_name    # store the name of the venv you like to use for this dir in .python-version
$ pyenv virtualenvs        # check the right virtualenv is activated on entering project directory
$ pip install -r requirements/local.txt
```

Create the database and run the development server:

```shell
$ ./manage.py migrate
$ ./manage.py runserver 0.0.0.0:8000
```

# Getting A Data Science Project Up And Running

To activate a conda environment automatically on entering a directory
containing an environment.yml file, I use a small function
in .config/fish/config.fish:

```shell
# on pwd change look for conda environment.yml and activate conda env
function activate_conda_env --on-variable PWD
  if test -e environment.yml
    pyenv activate (pyenv virtualenvs | grep miniconda | cut -d " " -f 3)
    conda activate (grep name environment.yml | cut -d " " -f 2)
  end
end
```

Setting up the virtual environment:

``` shell
$ pyenv activate miniconda3-latest
$ conda env create        # after creating an environment.yml
$ conda deactivate
$ cd
$ cd projects/project_dir
$ conda env list             # right environment should be activated
```

# Using fzf

[fzf](https://github.com/junegunn/fzf) is a really great tool, and the
most enjoyed recent addition to my toolbelt.

Install it with:

```shell
$ brew install fzf
/opt/fzf/install  # install useful key bindings and fuzzy completion
```

You can put some helpful environment variables in ~/.config/fish/config.fish:
```shell
# fzf
set -gx FZF_DEFAULT_COMMAND "fd --type f"
set -gx FZF_DEFAULT_OPTS "-layout=reverse --inline-info"
```

Here are some examples on how to use it:

```shell
$ vim (fzf)  # search for file and open in vim
$ history | fzf +s --tac  # search in history in reverse order and dont sort result
$ fzf --preview 'bat --style=numbers --color=always {} | head -500'  # use fzf with bat preview
```

## macOS quirks

On OS X, Alt-c (Option-c) types ç by default. In iTerm2, you can send the right
escape sequence with Esc-c. If you configure the option key to act as +Esc
(iTerm2 Preferences > Profiles > Default > Keys > Left option (⌥) acts as: >
+Esc), then alt-c will work for fzf as documented

# Fixing Vim

Use homebrew to install vim:

```shell
$ brew install vim
```

## Install Vundle

```shell
$ git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
```

List of vim plugins I like to use:

* [fugitive.vim](https://github.com/tpope/vim-fugitive) interacting with git from vim
* [jedi-vim](https://github.com/davidhalter/jedi-vim) autocompletion and code navigation
* [Command-T](https://github.com/wincent/command-t) fuzzy search/open files from vim
* [supertab](https://github.com/ervandew/supertab) configure <tab> behaviour
* [YouCompleteMe](https://github.com/ycm-core/YouCompleteMe) code completion engine
* [psf/black](https://github.com/psf/black) vim plugin for python formatting :BlackUpgrade to update

[Awesome list](https://vimawesome.com/) of vim plugins.

# Useful Command Line Tools
* [bat](https://github.com/sharkdp/bat)
* [tree](http://mama.indstate.edu/users/ice/tree/)
* [ripgrep](https://github.com/BurntSushi/ripgrep)
* [fd](https://github.com/sharkdp/fd)
* [fzf](https://github.com/junegunn/fzf)
* git-flow brew install git-flow
* [wget](https://www.gnu.org/software/wget/)
* [tldr](https://github.com/tldr-pages/tldr-cpp-client)
* [asciinema](https://asciinema.org/)
* [multitail](https://www.vanheusden.com/multitail/)
* [ntop](https://www.ntop.org/products/traffic-analysis/ntop/) (brew install ntopng)
* slurm brew install slurm
* [gitversion](https://github.com/GitTools/GitVersion)
* [gource](https://gource.io/)
* [pandoc](https://pandoc.org/)
* [tmux](https://github.com/tmux/tmux/wiki)
* [neofetch](https://github.com/dylanaraps/neofetch)
