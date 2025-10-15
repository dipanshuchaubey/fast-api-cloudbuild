FROM python:3.13-alpine

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

CMD [ "sleep", "infinity" ]
