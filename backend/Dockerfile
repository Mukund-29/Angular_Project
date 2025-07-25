# Stage 1 - Dependencies
FROM python:3.10-slim as builder

WORKDIR /app
COPY requirements.txt .
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Stage 2 - Final Image
FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1
WORKDIR /app

# Copy dependencies from builder
COPY --from=builder /usr/local /usr/local

# Copy project files
COPY . .

# Ensure migrations folder exists and has correct permissions
RUN mkdir -p /app/soloapp/migrations && \
    chmod -R 777 /app

# Security: create a non-root user
RUN addgroup --system appgroup && adduser --system appuser --ingroup appgroup

# Run migrations & collect static during build
RUN python manage.py migrate --noinput && \
    python manage.py collectstatic --noinput

USER appuser

EXPOSE 8080

CMD ["gunicorn", "wsgi:application", "--bind", "0.0.0.0:8080"]
