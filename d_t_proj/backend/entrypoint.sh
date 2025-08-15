#!/bin/sh
set -e

# Проверим, что nc установлен (в образе должен быть netcat-openbsd)
if ! command -v nc >/dev/null 2>&1; then
  echo "ERROR: 'nc' (netcat) не найден. Установи пакет netcat-openbsd в Dockerfile."
  exit 1
fi

# Ждём базу, если указаны хост и порт
if [ -n "${DB_HOST:-}" ] && [ -n "${DB_PORT:-}" ]; then
  echo "Waiting for DB ${DB_HOST}:${DB_PORT}..."
  until nc -z -w 1 "$DB_HOST" "$DB_PORT"; do
    sleep 0.5
  done
fi

echo "Apply migrations..."
python manage.py migrate --noinput

# На dev по желанию:
# echo "Collect static..."
# python manage.py collectstatic --noinput || true

echo "Starting dev server..."
exec python manage.py runserver 0.0.0.0:8000