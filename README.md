This repository contains practice code based on the Udemy course [Python Django - The Practical Guide](https://www.udemy.com/course/python-django-the-practical-guide/).

[![](https://github.com/asarkar/udemy-django-practical-guide/workflows/CI/badge.svg)](https://github.com/asarkar/udemy-django-practical-guide/actions)

## Syllabus

1. Getting Started
2. Course Setup
3. URLs & Views
4. Templates & Static Files

## Development

### Environment Setup

**Download all dependencies**
```
% uv sync
```
**Manually activate venv**
```
% source ./.venv/bin/activate
```

**Deactivate venv**
```
% deactivate
```

### Django Management Commands

Because we use `uv` to manage Python execution, any direct invocation of commands such as `python`, 
`django-admin`, or other executables is replaced with `uv run`. This ensures that all tools run 
within the environment managed by `uv`.

Rather than navigating into the project directory to run management commands, we run all commands 
from the **repository root**, and pass the project directory using the `--directory` flag.

For example, what would normally be executed as:
```
app% python manage.py migrate
```

becomes:
```
% uv run --directory app manage.py migrate
```

`uv` will "search upwards" from a given directory until it finds `pyproject.toml`, `.venv`, or `uv` 
configuration files. A directory containing any of these files is considered the project root. `uv` 
will use a `.venv/` if found in the root.

Thus, running a command like `uv run --directory app python -c "import sys; print(sys.executable)"` 
doesn't require manual activation of venv.

**Create a new Django project**:
```
django-admin startproject app
```

**Create a new Django application**:
```
python manage.py startapp core
```

**Apply all database migrations**:
```
python manage.py migrate
```

**Create migrations for the `core` app**:
```
python manage.py makemigrations core
```

**View the SQL statements that will be executed with the first migration**:
```
python manage.py sqlmigrate core 0001
```

**Run the Django development server**:
```
python manage.py runserver
```

**Run the development server specifying host/port and settings file**:
```
python manage.py runserver 127.0.0.1:8001 --settings=app.settings
```

**Run the Django shell**:
```
python manage.py shell
```

**Create a superuser**:
```
python manage.py createsuperuser
```

**Dump the database into a JSON file**:
```
python manage.py dumpdata auth core --indent 2 > core/fixtures/core.json
```

**Seed the database from a JSON file**:
```
python manage.py loaddata core/fixtures/core.json
```

**Delete all data from all tables**:
```
python manage.py flush --noinput
```

**Run custom management command**:
```
python manage.py seed_users
```

### Testing

**Run tests**
```
% ./.github/run.sh <project>
```
