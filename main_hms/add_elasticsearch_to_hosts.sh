#!/bin/bash

# Получаем ID контейнера Elasticsearch
CONTAINER_ID=$(docker ps -qf "name=elasticsearch")

# Получаем IP-адрес контейнера Elasticsearch
CONTAINER_IP=$(docker inspect -f '{{range .NetworkSettings.Networks}}{{.IPAddress}}{{end}}' $CONTAINER_ID)

# Проверяем, если уже есть запись для elasticsearch в /etc/hosts
if grep -q "elasticsearch" /etc/hosts; then
    # Если запись есть, обновляем её
    sudo sed -i "/elasticsearch/c\\$CONTAINER_IP elasticsearch" /etc/hosts
    echo "Запись для elasticsearch обновлена в /etc/hosts"
else
    # Если записи нет, добавляем новую
    echo "$CONTAINER_IP elasticsearch" | sudo tee -a /etc/hosts > /dev/null
    echo "Запись для elasticsearch добавлена в /etc/hosts"
fi
