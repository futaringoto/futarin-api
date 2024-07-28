FROM python:3.12-alpine

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

EXPOSE 8000

CMD ["poetry", "run", "python3", "check_env.py"]
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80", "--reload"]
