#!/bin/bash

# Скрипт для настройки Telegram сессии
echo "🔧 Настройка Telegram сессии..."

# Переходим в директорию проекта
cd ~/money-printer-parser

# Активируем виртуальное окружение
source venv/bin/activate

# Останавливаем сервис если запущен
echo "⏹️ Останавливаем сервис..."
sudo systemctl stop bwe-news-speed-test

# Запускаем настройку Telegram
echo "📱 Запуск настройки Telegram..."
echo "Введите код подтверждения, который придет в Telegram:"
python -c "
import asyncio
from telethon import TelegramClient
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE, TELEGRAM_SESSION_NAME

async def setup_telegram():
    try:
        client = TelegramClient(TELEGRAM_SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)
        await client.start(phone=TELEGRAM_PHONE)
        print('✅ Telegram сессия успешно настроена!')
        await client.disconnect()
    except Exception as e:
        print(f'❌ Ошибка настройки: {e}')

asyncio.run(setup_telegram())
"

echo ""
echo "✅ Настройка завершена!"
echo "Теперь можно запустить сервис:"
echo "sudo systemctl start bwe-news-speed-test"
