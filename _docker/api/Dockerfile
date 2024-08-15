ARG ENV
# devlopment stage
FROM python:3.12-alpine as development

WORKDIR /api

RUN apk update && apk add --no-cache \
    gcc musl-dev libffi-dev build-base curl

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY ./api/pyproject.toml .
COPY ./api/poetry.lock .

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY ./api/ .

# production stage
FROM python:3.12-alpine as production

WORKDIR /api

RUN apk update && apk add --no-cache \
    gcc musl-dev libffi-dev build-base curl

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY ./api/pyproject.toml .
COPY ./api/poetry.lock .

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-dev

COPY ./api/ .

# 最終ステージを選択
FROM ${ENV} as final

ARG ENV
WORKDIR /api
COPY --from=production /api /api

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
