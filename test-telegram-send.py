#!/usr/bin/env python3
"""
Тестовый скрипт для отправки файла в Telegram
"""

import asyncio
import os
from telethon import TelegramClient
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE, TELEGRAM_SESSION_NAME

async def test_send_file():
    """Тест отправки файла в Telegram"""
    try:
        # Создаем клиент
        client = TelegramClient(TELEGRAM_SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)
        await client.start(phone=TELEGRAM_PHONE)
        
        print("✅ Telegram клиент подключен")
        
        # Проверяем существование файла
        log_file = "bwe_news_log.txt"
        if not os.path.exists(log_file):
            print(f"❌ Файл {log_file} не найден")
            # Создаем тестовый файл
            with open(log_file, 'w', encoding='utf-8') as f:
                f.write("Тестовый лог файл\n")
                f.write("2025-01-27 12:00:00 - TEST - Тестовая новость\n")
            print(f"✅ Создан тестовый файл {log_file}")
        
        # Отправляем файл себе
        print("📤 Отправка файла...")
        await client.send_file("me", log_file, caption="📋 Лог файл BWEnews Speed Test")
        print("✅ Файл отправлен себе")
        
        # Пытаемся найти пользователя @Tojen
        print("🔍 Поиск пользователя @Tojen...")
        try:
            user = await client.get_entity("@Tojen")
            print(f"✅ Пользователь найден: {user.first_name} {user.last_name or ''}")
            
            # Отправляем файл пользователю
            await client.send_file(user, log_file, caption="📋 Лог файл BWEnews Speed Test")
            print("✅ Файл отправлен пользователю @Tojen")
            
        except Exception as e:
            print(f"❌ Ошибка поиска/отправки пользователю @Tojen: {e}")
            print("💡 Попробуйте отправить файл вручную или проверьте username")
        
        await client.disconnect()
        print("✅ Клиент отключен")
        
    except Exception as e:
        print(f"❌ Ошибка: {e}")

if __name__ == "__main__":
    asyncio.run(test_send_file())
