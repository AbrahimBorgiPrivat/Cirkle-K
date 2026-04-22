FROM python:3.11-slim

ENV POETRY_VERSION=2.1.3 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_CREATE=false \
    PYTHONPATH=/app

WORKDIR /app

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir "poetry==$POETRY_VERSION"

COPY source/code/pyproject.toml ./pyproject.toml
COPY source/code/poetry.lock ./poetry.lock
COPY source/code/README.md ./README.md
RUN poetry install --only main --no-root --no-ansi

COPY source/code/service/etl/service_json_to_client/app ./app
COPY source/code/libraries ./libraries
COPY source/code/runtime_definitions/service_json_to_client ./runtime_definitions/service_json_to_client

CMD ["poetry", "run", "python", "app/main.py"]
