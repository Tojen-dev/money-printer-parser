#!/bin/bash

# Скрипт развертывания BWEnews Speed Test
# Копирует файлы проекта на сервер

set -e

# Конфигурация
SERVER_USER="your-username"
SERVER_HOST="your-server-ip"
SERVER_PATH="~/bwe-news-speed-test"

echo "🚀 Развертывание BWEnews Speed Test на сервер..."

# Список файлов для копирования
FILES=(
    "main.py"
    "config.py"
    "telegram_monitor.py"
    "rss_monitor.py"
    "websocket_monitor.py"
    "news_display.py"
    "news_logger.py"
    "requirements.txt"
    "README.md"
)

# Создаем архив проекта
echo "📦 Создание архива проекта..."
tar -czf bwe-news-speed-test.tar.gz "${FILES[@]}"

# Копируем на сервер
echo "📤 Копирование файлов на сервер..."
scp bwe-news-speed-test.tar.gz $SERVER_USER@$SERVER_HOST:$SERVER_PATH/

# Выполняем команды на сервере
echo "🔧 Установка на сервере..."
ssh $SERVER_USER@$SERVER_HOST << 'EOF'
    cd ~/bwe-news-speed-test
    
    # Распаковываем архив
    tar -xzf bwe-news-speed-test.tar.gz
    rm bwe-news-speed-test.tar.gz
    
    # Активируем виртуальное окружение
    source venv/bin/activate
    
    # Обновляем зависимости
    pip install -r requirements.txt
    
    # Перезапускаем сервис
    sudo systemctl restart bwe-news-speed-test
    
    echo "✅ Развертывание завершено!"
    echo "📊 Статус сервиса:"
    sudo systemctl status bwe-news-speed-test
EOF

# Удаляем локальный архив
rm bwe-news-speed-test.tar.gz

echo "🎉 Развертывание завершено!"
