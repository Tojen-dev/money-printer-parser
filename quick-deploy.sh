#!/bin/bash

# Быстрый скрипт развертывания BWEnews Speed Test
# Использование: ./quick-deploy.sh username@server-ip

if [ $# -eq 0 ]; then
    echo "Использование: $0 username@server-ip"
    echo "Пример: $0 user@192.168.1.100"
    exit 1
fi

SERVER=$1
REMOTE_DIR="~/bwe-news-speed-test"

echo "🚀 Быстрое развертывание на $SERVER..."

# Создаем временный архив
echo "📦 Создание архива..."
tar -czf deploy.tar.gz \
    main.py config.py \
    telegram_monitor.py rss_monitor.py websocket_monitor.py \
    news_display.py news_logger.py \
    requirements.txt README.md server-setup.md \
    install.sh

# Копируем на сервер
echo "📤 Копирование на сервер..."
scp deploy.tar.gz $SERVER:$REMOTE_DIR/

# Выполняем установку на сервере
echo "🔧 Установка на сервере..."
ssh $SERVER << 'EOF'
    cd ~/bwe-news-speed-test
    
    # Распаковываем
    tar -xzf deploy.tar.gz
    rm deploy.tar.gz
    
    # Делаем скрипт установки исполняемым
    chmod +x install.sh
    
    # Запускаем установку
    ./install.sh
EOF

# Удаляем локальный архив
rm deploy.tar.gz

echo "✅ Развертывание завершено!"
echo "📊 Проверьте статус: ssh $SERVER 'sudo systemctl status bwe-news-speed-test'"
echo "📋 Логи: ssh $SERVER 'sudo journalctl -u bwe-news-speed-test -f'"
