#!/bin/bash

# Универсальный скрипт установки BWEnews Speed Test
# Работает с любой версией Python 3.x и существующим репозиторием

set -e  # Остановка при ошибке

echo "🚀 Установка BWEnews Speed Test..."

# Обновляем систему
echo "📦 Обновление системы..."
sudo apt update && sudo apt upgrade -y

# Определяем доступную версию Python
echo "🔍 Поиск доступной версии Python..."
PYTHON_VERSION=""

# Проверяем разные версии Python
for version in python3.11 python3.10 python3.9 python3.8 python3; do
    if command -v $version &> /dev/null; then
        PYTHON_VERSION=$version
        echo "✅ Найдена версия: $PYTHON_VERSION"
        break
    fi
done

if [ -z "$PYTHON_VERSION" ]; then
    echo "❌ Python не найден. Устанавливаем Python 3..."
    sudo apt install -y python3 python3-venv python3-pip
    PYTHON_VERSION="python3"
fi

# Устанавливаем системные зависимости
echo "🔧 Установка системных зависимостей..."
sudo apt install -y git curl wget build-essential libssl-dev libffi-dev python3-dev

# Проверяем существование проекта
echo "📁 Проверка директории проекта..."
if [ ! -d "$HOME/money-printer-parser" ]; then
    echo "❌ Директория проекта не найдена!"
    echo "Сначала выполните: git clone https://github.com/Tojen-dev/money-printer-parser.git ~/money-printer-parser"
    exit 1
fi

# Переходим в директорию проекта
cd ~/money-printer-parser

# Проверяем, что это git репозиторий
if [ ! -d ".git" ]; then
    echo "❌ Это не git репозиторий!"
    echo "Убедитесь, что проект был клонирован правильно"
    exit 1
fi

# Обновляем проект из git (если нужно)
echo "📥 Обновление проекта из Git..."
git pull origin main

# Проверяем наличие requirements.txt
if [ ! -f "requirements.txt" ]; then
    echo "❌ Файл requirements.txt не найден!"
    echo "Убедитесь, что проект содержит все необходимые файлы"
    exit 1
fi

# Создаем виртуальное окружение (если не существует)
echo "🔐 Создание виртуального окружения..."
if [ ! -d "venv" ]; then
    $PYTHON_VERSION -m venv venv
    echo "✅ Виртуальное окружение создано"
else
    echo "✅ Виртуальное окружение уже существует"
fi

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
WorkingDirectory=$HOME/money-printer-parser
Environment=PATH=$HOME/money-printer-parser/venv/bin
ExecStart=$HOME/money-printer-parser/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Перезагружаем systemd
sudo systemctl daemon-reload

# Включаем автозапуск
sudo systemctl enable bwe-news-speed-test

# Создаем скрипт управления
echo "📝 Создание скрипта управления..."
cat > ~/bwe-news-control.sh << 'EOF'
#!/bin/bash

# Скрипт управления BWEnews Speed Test
# Использование: ./bwe-news-control.sh [start|stop|restart|status|logs|news]

case "$1" in
    start)
        echo "🚀 Запуск BWEnews Speed Test..."
        sudo systemctl start bwe-news-speed-test
        ;;
    stop)
        echo "⏹️ Остановка BWEnews Speed Test..."
        sudo systemctl stop bwe-news-speed-test
        ;;
    restart)
        echo "🔄 Перезапуск BWEnews Speed Test..."
        sudo systemctl restart bwe-news-speed-test
        ;;
    status)
        echo "📊 Статус BWEnews Speed Test..."
        sudo systemctl status bwe-news-speed-test
        ;;
    logs)
        echo "📋 Логи BWEnews Speed Test..."
        sudo journalctl -u bwe-news-speed-test -f
        ;;
    news)
        echo "📰 Новости BWEnews Speed Test..."
        tail -f ~/money-printer-parser/bwe_news_log.txt
        ;;
    *)
        echo "Использование: $0 {start|stop|restart|status|logs|news}"
        echo ""
        echo "Команды:"
        echo "  start   - Запустить сервис"
        echo "  stop    - Остановить сервис"
        echo "  restart - Перезапустить сервис"
        echo "  status  - Показать статус"
        echo "  logs    - Показать логи в реальном времени"
        echo "  news    - Показать новости в реальном времени"
        exit 1
        ;;
esac
EOF

chmod +x ~/bwe-news-control.sh

echo "✅ Установка завершена!"
echo ""
echo "📋 Команды управления:"
echo "  Запуск: sudo systemctl start bwe-news-speed-test"
echo "  Остановка: sudo systemctl stop bwe-news-speed-test"
echo "  Статус: sudo systemctl status bwe-news-speed-test"
echo "  Логи: sudo journalctl -u bwe-news-speed-test -f"
echo ""
echo "📁 Файлы логов:"
echo "  Новости: ~/money-printer-parser/bwe_news_log.txt"
echo "  Системные логи: sudo journalctl -u bwe-news-speed-test"
echo ""
echo "🎯 Для запуска выполните: sudo systemctl start bwe-news-speed-test"
echo ""
echo "📝 Или используйте скрипт управления: ~/bwe-news-control.sh start"
