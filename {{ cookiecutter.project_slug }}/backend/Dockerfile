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

# pip + инструменты для компиляции pyproject → requirements
# (pip-tools свежий, плюс build/pyproject_hooks/packaging)
RUN python -m pip install --upgrade pip setuptools wheel \
 && python -m pip install "pip-tools>=7.4" build pyproject_hooks packaging

# Диагностика (можешь удалить потом)
RUN ls -la /app/requirements || true \
 && ( [ -f /app/requirements/pyproject.toml ] && head -n 20 /app/requirements/pyproject.toml || echo "NO pyproject.toml in /app/requirements" )

# ВАЖНО: компилим из той директории, где лежит pyproject.toml
RUN if [ -f /app/requirements/pyproject.toml ]; then \
        cd /app/requirements && pip-compile --resolver=backtracking pyproject.toml -o base.txt ; \
    else \
        echo "ERROR: /app/requirements/pyproject.toml not found — either add it, or commit base.txt" && exit 1 ; \
    fi

# Ставим зависимости
RUN pip install -r /app/requirements/base.txt

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