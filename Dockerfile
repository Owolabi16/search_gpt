# Builder stage
FROM python:3.10-slim as builder

WORKDIR /app
ENV PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip wheel --no-cache-dir --no-deps --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.10-slim

WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

COPY --from=builder /app/wheels /wheels
RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels

COPY . .
EXPOSE 8000
ENTRYPOINT ["python"]
CMD ["app.py"]
