[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Preocts/egggist/main.svg)](https://results.pre-commit.ci/latest/github/Preocts/egggist/main)
[![Python package](https://github.com/Preocts/egggist/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/Preocts/egggist/actions/workflows/python-tests.yml)

# egggist

CLI utility to post file(s) to a Gist.  Posts are, by default, public however the CLI allows you to flag them as private (secret) if desired. A personal access token is required, see `CLI Usage` below.

---

### Requirements
- Python >= 3.8

---

### Installation

**Note**: Replace `v1.0.0` with the desired version number or `main` for lastest (unstable) version

Install via pip:
```bash
# Linux/MacOS
python3 -m pip install git+https://github.com/preocts/egggist@v1.0.0

# Windows
py -m pip install git+https://github.com/preocts/egggist@v1.0.0
```

---

### CLI Usage

EggGist will prompt for your GitHub username and a user token. The token only needs `gist` permissions and can be created in Profile -> Settings -> Developer Settings -> Personal Access Tokens.

**Note**: Your personal access token is stored, in plain-text, in your user home directory as `.egggist_conf`.  This file can be deleted at anytime and I **strongly** recommend restricting the token perimissions to only `gist`.

```bash
usage: prfiles [-h] [--set-username NAME] [--set-token TOKEN] [--private] [--debug] [filename [filename ...]]

Send a file to your GitHub Gist.

positional arguments:
  filename             One, or more, files to be added to the gist (utf-8 encoding)

optional arguments:
  -h, --help           show this help message and exit
  --set-username NAME  Store your username in '~/.egggist_conf
  --set-token TOKEN    Set your user token in `~/.egggist_conf
  --private            Make the gist private
  --debug              Turns internal logging level to DEBUG.
```

Sample, posting three files to one private gist:
```bash
$ egggist file1.txt file2.txt file3.txt --private
```

---

## Local developer installation

It is **highly** recommended to use a `venv` for installation. Leveraging a `venv` will ensure the installed dependency files will not impact other python projects.

Clone this repo and enter root directory of repo:
```bash
$ git clone https://github.com/[name]/[module_name]
$ cd [module_name]
```

Create and activate `venv`:
```bash
# Linux/MacOS
python3 -m venv venv
. venv/bin/activate

# Windows
python -m venv venv
venv\Scripts\activate.bat
# or
py -m venv venv
venv\Scripts\activate.bat
```

Your command prompt should now have a `(venv)` prefix on it.

Install editable library and development requirements:
```bash
# Linux/MacOS
pip install -r requirements-dev.txt
pip install --editable .

# Windows
python -m pip install -r requirements-dev.txt
python -m pip install --editable .
# or
py -m pip install -r requirements-dev.txt
py -m pip install --editable .
```

Install pre-commit hooks to local repo:
```bash
pre-commit install
pre-commit autoupdate
```

Run tests
```bash
tox
```

To exit the `venv`:
```bash
deactivate
```

---

### Makefile

This repo has a Makefile with some quality of life scripts if your system supports `make`.

- `install` : Clean all artifacts, update pip, install requirements with no updates
- `update` : Clean all artifacts, update pip, update requirements, install everything
- `clean-pyc` : Deletes python/mypy artifacts
- `clean-tests` : Deletes tox, coverage, and pytest artifacts
- `build-dist` : Build source distribution and wheel distribution
- `stats` : Shows line counts of `*.py` code
