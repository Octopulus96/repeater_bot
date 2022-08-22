FROM python:3.9-slim-buster

RUN pip install poetry
RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-dev
#убрать service после ./
COPY service ./service

CMD ["uvicorn", "service.app.main:app", "--host", "0.0.0.0"]
