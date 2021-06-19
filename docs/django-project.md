# Django Project

#### Project Structure
```html
.
├── Pipfile
├── Pipfile.lock
├── README.md
├── <span style="color:blue">config</span>
│   ├── app.example.ini
│   └── app.ini
├── <span style="color:blue">docs</span>
│   ├── django-project.md
│   ├── help.md
│   └── <span style="color:blue">screenshots</span>
│       ├── pre-commit-example.png
│       └── pre-commit-failed.png
├── <span style="color:blue">public</span>
│   ├── <span style="color:blue">media</span>
│   └── <span style="color:blue">static</span>
├── pyproject.toml
├── setup.cfg
└── <span style="color:blue">src</span>
    ├── <span style="color:blue">core</span>
    │   ├── __init__.py
    │   ├── asgi.py
    │   ├── db.sqlite3
    │   ├── <span style="color:blue">settings</span>
    │   │   ├── __init__.py
    │   │   ├── base.py
    │   │   ├── dev.py
    │   │   ├── production.py
    │   │   └── tests.py
    │   ├── <span style="color:blue">static</span>
    │   │   ├── <span style="color:blue">app</span>
    │   │   └── <span style="color:blue">locale</span>
    │   ├── <span style="color:blue">templates</span>
    │   ├── urls.py
    │   └── wsgi.py
    └── <span style="color:yellow">manage.py</span>

<span style="color:blue">15 directories, 28 files</span>

```

#### DEFAULT APP.INI Configurations

```ini

[app]
url = http://localhost:8000
domain = localhost
debug = True
hosts = *
secret = 8&bz667r9srud=6u$js60*bprqid%gcos6@pm7pt()b83=!4=o

[database]
engine = django.db.backends.sqlite3
port = 5432
host = localhost
name = yoyo_weather_app
user = yoyo
password = yoyo

[test_database]
port = 5432
host = localhost
name = yoyo_weather_app_test
user = yoyo
password = yoyo
```
