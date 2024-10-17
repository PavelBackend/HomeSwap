#!/bin/sh

set -e

until PGPASSWORD=$DB_PASSWORD psql -h "$DB_HOST" -U "$DB_USER" -c '\q'; do
  >&2 echo "База данных недоступна - ждем..."
  sleep 1
done

poetry run python manage.py migrate

poetry run python manage.py collectstatic --noinput

exec "$@"
