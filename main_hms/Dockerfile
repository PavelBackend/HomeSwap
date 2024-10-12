FROM python:3.9-slim

RUN apt update -y && \
    apt install -y python3-dev gcc libffi-dev musl-dev curl && \
    apt clean && rm -rf /var/lib/apt/lists/*

RUN curl -sSL https://install.python-poetry.org | python3 -

ENV PATH="/root/.local/bin:$PATH"

RUN mkdir /homeswapd

WORKDIR /homeswapd

COPY pyproject.toml poetry.lock /homeswapd/

RUN poetry install --no-root --no-dev

COPY . /homeswapd/

EXPOSE 8000

CMD ["sh", "-c", "poetry run daphne -b 0.0.0.0 -p 8000 main_hms.asgi:application"]
