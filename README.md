# awesome-python-devenv

Just a collection of tips and tools to improve your python development experience

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

## Terminal / Shell

The default macOS terminal is not as bad as it used to be, but I still like to
use [iTerm2](https://iterm2.com/). I
used [bash](https://www.gnu.org/software/bash/) as shell for a long time but
got adventurous in the past few years and went from
using [zsh](www.zsh.org/) to [fish](https://fishshell.com/):

```shell
$ brew install fish
$ sudo echo /usr/local/bin/fish >> /etc/shells
$ chsh -s /usr/local/bin/fish
```

I like fish quite a lot, but it still feels weird not using bash. Where's my
beloved ctrl + r for example? With zsh it was the same - tabcompletion just
felt different. Yes, it probably was better in some cases, but it wasn't the
same. Also just pressing return is a lot faster in bash than in zsh or fish and
I don't know why.

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

## Python

Installing python on macOS (or any other OS I know of) is much more difficult
than you would expect. After using a mixture of system provided python, python
installed by homebrew and python installed by conda I finally settled
using [pyenv](github.com/pyenv/pyenv). With pyenv it's easy to install a lot of
different python versions. After that you are able to define which python
version should be used per directory. Even things like pypy or miniconda are
possible. Together with [pyenv-virtualenv](github.com/pyenv/pyenv-virtualenv) I
use it for my data science conda environments and my web development
virtualenvs. Environments are automatically switched by entering the respective
project directory:

```shell
$ brew install xz pyenv pyenv-virtualenv
```

There should be something like this in .config/fish/config.fish:

```shell
    # pyenv virtualenvs
    status --is-interactive; and source (pyenv init -|psub)
    status --is-interactive; and source (pyenv virtualenv-init -|psub)
```

## Getting A Django Project Up And Running

### Database

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

### Environment Variables

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

### Virtualenv

You should now be able to just clone one of your old django projects from
github for example, create a new virtualenv and install the requirements:

```shell
$ pyenv virtualenv 3.8.0 venv_name
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

## Getting A Data Science Project Up And Running

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

## Fixing Vim

Use homebrew to install vim:

```shell
$ brew install vim
```

### Install Vundle

```shell
$ git clone https://github.com/VundleVim/Vundle.vim.git ~/.vim/bundle/Vundle.vim
```

List of vim plugins I like to use:

* [fugitive.vim](github.com/tpope/vim-fugitive) interacting with git from vim
* [jedi-vim](github.com/davidhalter/jedi-vim) autocompletion and code navigation
* [Command-T](github.com/wincent/command-t) fuzzy search/open files from vim
* [supertab](github.com/ervandew/supertab) configure <tab> behaviour
* [YouCompleteMe](github.com/ycm-core/YouCompleteMe) code completion engine
* [psf/black](github.com/psf/black) vim plugin for python formatting
