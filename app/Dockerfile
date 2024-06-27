FROM python:3.12-alpine

WORKDIR /app

RUN apk update && apk add --no-cache \
    gcc musl-dev libffi-dev build-base curl

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY ./pyproject.toml /app/pyproject.toml
COPY ./poetry.lock /app/poetry.lock

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY ./src /app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
