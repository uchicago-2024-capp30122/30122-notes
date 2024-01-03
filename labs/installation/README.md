# Dev Environment

The goal of this "lab" is to set up your dev environment to work in Python. Even if you already have an environment set up, it is worth making sure you can run the tools we will use this quarter.

### Installing Python on MacOS (Optional)

Python is already installed on MacOS, but it is a good idea to have a separate installation of Python for development.

1. Download the latest version of Python 3 from [python.org](https://www.python.org/downloads/).
2. Run the installer and follow the instructions.
3. Open a terminal and run `python3 --version` to verify that Python 3 is installed.

### Installing pipx on MacOS

If you use Homebrew, you can install pipx with `brew install pipx`.

If you do not use Homebrew, you can install pipx with `python3 -m pip install --user pipx`.

Before doing this, be sure `python3` is referring to the correct Python installation.

### Installing poetry on MacOS

The recommended way to install poetry is with pipx: `pipx install poetry`.

If you are using homebrew, you can also install poetry with `brew install poetry`.

### Adding to your PATH on MacOS

MacOS uses the `PATH` environment variable to determine where to look for executables. This means when installing new tools you may need to make sure they wind up on your PATH.

To do this, add lines like:

```bash
# adds to beginning of path
export PATH="/Users/jamesturk/.pyenv/shims:$PATH"
```

to your ~/.zshrc file (or ~/.bashrc if you are using bash).

You can verify that this worked by running `echo $PATH` in a new terminal, and checking that `which` returns the correct path for the tool you installed.

## Windows

### Installing Python on Windows

1. Download the latest version of Python 3 from [python.org](https://www.python.org/downloads/).
2. Run the installer and follow the instructions.
3. Open a terminal and run `python --version` to verify that Python 3 is installed.

### Installing pipx on Windows

If you are using the default Python installation, you can install pipx with `python3 -m pip install --user pipx`.

Before doing this, be sure `python3` is referring to the correct Python installation.

### Installing poetry on Windows

The recommended way to install poetry is with pipx: `pipx install poetry`.

## Advanced (Using pyenv to manage Python versions)

If you want to have the option to manage multiple versions of Python you may wish to install `pyenv` instead.

To do this, read the "How it Works" and "Installation" sections of the [pyenv documentation](https://github.com/pyenv/pyenv).
