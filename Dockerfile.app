FROM python:3.9-slim-buster

WORKDIR /service

COPY pyproject.toml poetry.lock ./
COPY loggingconfig.conf ./
COPY service ./

RUN pip install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev

CMD ["python", "-m", "app"]
