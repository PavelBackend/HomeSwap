# Используем базовый образ
FROM python:3.9-slim

# Устанавливаем рабочую директорию
WORKDIR /homeswap

# Устанавливаем системные зависимости
RUN apt-get update && apt-get install -y postgresql-client

# Копируем зависимости
COPY pyproject.toml poetry.lock ./

# Устанавливаем Poetry
RUN pip install poetry

# Устанавливаем зависимости Python
RUN poetry config virtualenvs.create false && poetry install

# Копируем код приложения
COPY . .

# Копируем скрипт entrypoint
COPY entrypoint.sh /entrypoint.sh

# Делаем скрипт исполняемым
RUN chmod +x /entrypoint.sh

# Устанавливаем переменные окружения
ENV PYTHONUNBUFFERED=1

# Устанавливаем точку входа
ENTRYPOINT ["/entrypoint.sh"]
