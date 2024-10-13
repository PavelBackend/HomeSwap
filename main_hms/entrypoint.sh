#!/bin/sh

# Выходим при ошибке
set -e

# 1. Ожидаем, пока база данных станет доступна
until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -c '\q'; do
  >&2 echo "База данных недоступна - ждем..."
  sleep 1
done

# 2. Применяем миграции
poetry run python manage.py migrate

# 3. Собираем статику
poetry run python manage.py collectstatic --noinput

# 4. Запускаем сервер Daphne
poetry run daphne -b 0.0.0.0 -p 8000 main_hms.asgi:application
