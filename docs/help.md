# YOYO Weather API Help

### Pipenv usage

for general help:

`pipenv help`

for specific

```bash

pipenv install # installs all apps in Pipfile:[packages]

pipenv install some-package # a specific package you wish to install Pipfile:[packages]

pipenv install some-package --dev # a specific package you wish to install but only used in development Pipfile:[dev-packages]

pipenv lock # locks the current versions installed on your local

pipenv lock --requirements > ./requirements.txt # is similar to pip freeze > requirements.txt but only uses the app packages not dev-packages Pipfile:[packages]

pipenv lock --dev-only --requirements > ./dev-requirements.txt # exports only dev packages Pipfile:[dev-packages]

```

### Pre-Commit

pre-commit has been set up to ensure the following standards:

1. Flake8: Flake8 is the wrapper which verifies pep8, pyflakes and circular complexity
2. Black: Black is the uncompromising Python code formatter
3. iSort: isort is a Python utility / library to sort imports alphabetically, and automatically separated into sections and by type.
4. pre-commit-hook - Some out-of-the-box hooks for pre-commit:
    - trailing-whitespace
    - end-of-file-fixer
    - check-toml
    - check-merge-conflict

##### Pre-Commit Install

after running `pre-commit install` you should end up with something like the following:

```bash

#!/usr/bin/env python3.9
# File generated by pre-commit: https://pre-commit.com
# ID: 138fd403232d2ddd5efb44317e38bf03
import os
import sys

# we try our best, but the shebang of this script is difficult to determine:
# - macos doesn't ship with python3
# - windows executables are almost always `python.exe`
# therefore we continue to support python2 for this small script
if sys.version_info < (3, 3):
    from distutils.spawn import find_executable as which
else:
    from shutil import which

# work around https://github.com/Homebrew/homebrew-core/issues/30445
os.environ.pop('__PYVENV_LAUNCHER__', None)

# start templated
INSTALL_PYTHON = '/Users/matthewstuart/.virtualenvs/YoYoWeatherAPI/bin/python'
ARGS = ['hook-impl', '--config=.pre-commit-config.yaml', '--hook-type=pre-commit']
# end templated
ARGS.extend(('--hook-dir', os.path.realpath(os.path.dirname(__file__))))
ARGS.append('--')
ARGS.extend(sys.argv[1:])

DNE = '`pre-commit` not found.  Did you forget to activate your virtualenv?'
if os.access(INSTALL_PYTHON, os.X_OK):
    CMD = [INSTALL_PYTHON, '-mpre_commit']
elif which('pre-commit'):
    CMD = ['pre-commit']
else:
    raise SystemExit(DNE)

CMD.extend(ARGS)
if sys.platform == 'win32':  # https://bugs.python.org/issue19124
    import subprocess

    if sys.version_info < (3, 7):  # https://bugs.python.org/issue25942
        raise SystemExit(subprocess.Popen(CMD).wait())
    else:
        raise SystemExit(subprocess.call(CMD))
else:
    os.execvp(CMD[0], CMD)


```

##### Pre-Commit usage

your commits to git would contain the following during the general git-workflow:

```bash
git add .
git commit -m "My commit message"
# At this point the git-hook is executed and will look as follows

```
###### FAILED:
![alt text](./screenshots/pre-commit-failed.png)

###### PASSED:
![alt text](./screenshots/pre-commit-example.png)
