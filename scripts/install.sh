#!/bin/bash

# Установка зависимостей
apt-get update
apt-get install -y python3 python3-pip docker.io docker-compose

# Клонирование репозитория
git clone https://github.com/your-username/meteora-service.git
cd meteora-service

# Создание и настройка .env файла
cp .env.example .env
echo "Пожалуйста, настройте файл .env перед продолжением"
read -p "Нажмите Enter для продолжения..."

# Запуск через Docker
docker-compose up -d 