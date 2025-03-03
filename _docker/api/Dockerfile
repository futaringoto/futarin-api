ARG ENV
# devlopment stage
FROM python:3.12-slim as development

WORKDIR /api

RUN apt update && apt install -y --no-install-recommends \
    gcc libffi-dev build-essential curl rustc cargo

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY ./api/pyproject.toml .
COPY ./api/poetry.lock .

RUN poetry config virtualenvs.create false
RUN poetry install --no-root

COPY ./api/ .

ARG ENV
# production stage
FROM python:3.12-slim as production

WORKDIR /api

RUN apt update && apt install -y --no-install-recommends \
    gcc libffi-dev build-essential curl rustc cargo

RUN curl -sSL https://install.python-poetry.org | python3 -
ENV PATH="/root/.local/bin:$PATH"

COPY ./api/pyproject.toml .
COPY ./api/poetry.lock .

RUN poetry config virtualenvs.create false
RUN poetry install --no-root --without dev

COPY ./api/ .

# 最終ステージを選択
FROM ${ENV} as final

ARG ENV
WORKDIR /api
COPY --from=production /api /api

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
