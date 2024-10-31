#!/bin/sh

set -e

until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -d "$DB_NAME" -c '\q'; do
  >&2 echo "База данных недоступна - ждем..."
  sleep 1
done

echo "Применяем миграции..."
poetry run python manage.py migrate --verbosity 3

poetry run python manage.py collectstatic --noinput --verbosity 3 --clear

exec "$@"
