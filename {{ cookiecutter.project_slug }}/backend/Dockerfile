FROM python:3.12-slim

# Системные пакеты (psycopg, nc и прочее)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    libpq-dev \
    netcat-openbsd && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Кладём только requirements для кэша
COPY backend/requirements /app/requirements

# Установим pip, pip-tools и базовые зависимости (только base.txt — dev.txt не тащим в образ)
RUN python -m pip install --upgrade pip setuptools wheel pip-tools && \
    pip install -r /app/requirements/base.txt

# Кладём весь backend (код монтируем томом в compose, но базово пусть будет)
COPY backend /app

# На dev хотим settings.dev, а env придёт через compose (env_file)
ENV DJANGO_SETTINGS_MODULE={{ cookiecutter.project_slug }}.settings.dev \
    PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# entrypoint скрипт (миграции + старт)
COPY backend/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

EXPOSE 8000
ENTRYPOINT ["/entrypoint.sh"]