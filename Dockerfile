FROM ghcr.io/astral-sh/uv:python3.11-alpine

WORKDIR /app

COPY . /app

RUN uv sync

CMD ["uv", "run", "examples/quickstart.py"]
