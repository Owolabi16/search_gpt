# Builder stage
FROM python:3.10-slim AS builder

WORKDIR /app

# Copy only requirements file to leverage Docker cache
COPY . .

# Install dependencies
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.10-slim AS app

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1
# Install only runtime dependencies
COPY --from=builder /app/wheels /wheels

RUN pip install --no-cache-dir --no-index --find-links=/wheels/ /wheels/* \
    && rm -rf /wheels

# Copy the entire application code
COPY . .

# Expose port
EXPOSE 8000

# Run the application
CMD ["python", "app.py"]

# Migration stage - uses the main app as base
FROM app AS migration

# Set working directory (already done in base)
WORKDIR /app

# Run the migration command instead of the app
CMD ["python", "migrations.py"]