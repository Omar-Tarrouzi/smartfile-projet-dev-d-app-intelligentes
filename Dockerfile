FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml uv.lock ./
RUN pip install --no-cache-dir uv && uv sync --frozen --no-dev
COPY app.py ./
COPY smartfiles ./smartfiles
COPY demo ./demo
USER 10001:10001
EXPOSE 5000
CMD [".venv/bin/waitress-serve", "--host=0.0.0.0", "--port=5000", "app:app"]
