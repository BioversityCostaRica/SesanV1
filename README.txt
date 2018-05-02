ss_sesan
========

Getting Started
---------------

- Change directory into your newly created project.

    cd ss_sesan

- Create a Python virtual environment.

    python3 -m venv env

- Upgrade packaging tools.

    env/bin/pip install --upgrade pip setuptools

- Install the project in editable mode with its testing requirements.

    env/bin/pip install -e ".[testing]"

- Run your project's tests.

    env/bin/pytest

- Run your project.

    env/bin/pserve development.ini
- Create models.py
    sqlacodegen mysql://root:inspinia4@localhost/sesan_v1