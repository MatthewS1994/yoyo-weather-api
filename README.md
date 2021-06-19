# YOYO Weather API

### Requirements

- [Python > 3.6](https://www.python.org/downloads/)
- [Pip3](https://pip.pypa.io/en/stable/installing/)
- [NodeJS > 12.x](https://nodejs.org/en/docs/)
    - [NVM](https://github.com/nvm-sh) *(OPTIONAL) But helps with changing between version*
- [Virtualenv](https://virtualenv.pypa.io/en/latest/installation.html)
- [Virtualenvwrapper](https://virtualenvwrapper.readthedocs.io/en/latest/install.html) *(OPTIONAL)*
- [Pipenv](https://pypi.org/project/pipenv/)
  - [in-app usage](./docs/help.md#pipenv-usage)
- [Pre-Commit](https://pre-commit.com/)
  - [Pre-Commit Help](./docs/help.md#pre-commit)

# Contents:
- [Installation](#setup)
    - [Setup](#setup)
      - [Virtual environment](#virtual-environment)
      - [Pre-Commit installation:](#pre-commit-installation-developer)


# Installation

## Setup

#### Virtual environment

[see requirements](#Requirements)
- Virtualenv
- Virtualenvwrapper *(OPTIONAL)*
- Pipenv

```bash

mkvirtualenv --python=`which python3` WorkBuzzNLPTrainerAPI
# OR
virtualenv venv -p `which python3`

pipenv install

// include dev packages (optional) but required for development

pipenv install --dev

```

#### Pre-Commit installation (DEVELOPER):

[see requirements](#Requirements)
- Pre-Commit

> A framework for managing and maintaining multi-language pre-commit hooks.


see more about [pre-commit](https://pre-commit.com/)

```bash

pipenv install --dev

pre-commit install

```
