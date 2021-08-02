# python-template
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit&logoColor=white)](https://github.com/pre-commit/pre-commit)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/Preocts/egggist/main.svg)](https://results.pre-commit.ci/latest/github/Preocts/egggist/main)
[![Python package](https://github.com/Preocts/egggist/actions/workflows/python-tests.yml/badge.svg?branch=main)](https://github.com/Preocts/egggist/actions/workflows/python-tests.yml)

# egggist

Module Description

### Requirements
- Python >= 3.8

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
