FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir uv

COPY pyproject.toml uv.lock README.md ./
COPY src ./src
COPY resource ./resource

RUN uv sync --frozen --no-dev

CMD ["uv", "run", "python", "src/bot.py"]
