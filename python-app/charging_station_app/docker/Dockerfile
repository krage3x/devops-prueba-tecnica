FROM python:3.12-slim


ENV PYTHONUNBUFFERED=1 \
    POETRY_VERSION=2.2.1 \
    POETRY_NO_INTERACTION=1 \
    APP_HOME=/app \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN pip install poetry==$POETRY_VERSION

USER 1001:1001
WORKDIR $APP_HOME

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-root --only main

COPY app ./app

ENTRYPOINT ["poetry", "run", "gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "app.main:app"]