#!/bin/bash

# Скрипт установки BWEnews Speed Test для Ubuntu 24.04
# Автор: BWEnews Speed Test Team
# Версия: 1.0

set -e  # Остановка при ошибке

echo "🚀 Установка BWEnews Speed Test на Ubuntu 24.04..."

# Обновляем систему
echo "📦 Обновление системы..."
sudo apt update && sudo apt upgrade -y

# Устанавливаем Python 3.11 и pip
echo "🐍 Установка Python 3.11..."
sudo apt install -y python3.11 python3.11-venv python3.11-pip python3-pip

# Устанавливаем необходимые системные зависимости
echo "🔧 Установка системных зависимостей..."
sudo apt install -y git curl wget build-essential libssl-dev libffi-dev python3-dev

# Создаем директорию для проекта
echo "📁 Создание директории проекта..."
mkdir -p ~/bwe-news-speed-test
cd ~/bwe-news-speed-test

# Клонируем проект из Git (замените на ваш репозиторий)
echo "📥 Клонирование проекта из Git..."
git clone https://github.com/YOUR_USERNAME/bwe-news-speed-test.git .
# Или для GitLab: git clone https://gitlab.com/YOUR_USERNAME/bwe-news-speed-test.git .
# Или для Gitea: git clone https://gitea.com/YOUR_USERNAME/bwe-news-speed-test.git .

# Создаем виртуальное окружение
echo "🔐 Создание виртуального окружения..."
python3.11 -m venv venv
source venv/bin/activate

# Обновляем pip
echo "⬆️ Обновление pip..."
pip install --upgrade pip

# Устанавливаем зависимости Python
echo "📚 Установка Python зависимостей..."
pip install -r requirements.txt

# Создаем systemd сервис
echo "⚙️ Создание systemd сервиса..."
sudo tee /etc/systemd/system/bwe-news-speed-test.service > /dev/null <<EOF
[Unit]
Description=BWEnews Speed Test
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/bwe-news-speed-test
Environment=PATH=$HOME/bwe-news-speed-test/venv/bin
ExecStart=$HOME/bwe-news-speed-test/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Перезагружаем systemd
sudo systemctl daemon-reload

# Включаем автозапуск
sudo systemctl enable bwe-news-speed-test

echo "✅ Установка завершена!"
echo ""
echo "📋 Команды управления:"
echo "  Запуск: sudo systemctl start bwe-news-speed-test"
echo "  Остановка: sudo systemctl stop bwe-news-speed-test"
echo "  Статус: sudo systemctl status bwe-news-speed-test"
echo "  Логи: sudo journalctl -u bwe-news-speed-test -f"
echo ""
echo "📁 Файлы логов:"
echo "  Новости: ~/bwe-news-speed-test/bwe_news_log.txt"
echo "  Системные логи: sudo journalctl -u bwe-news-speed-test"
echo ""
echo "🎯 Для запуска выполните: sudo systemctl start bwe-news-speed-test"
