#!/usr/bin/env python3
"""
Скрипт для отправки логов в Telegram
"""

import asyncio
import os
import time
from datetime import datetime
from telethon import TelegramClient
from config import TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE, TELEGRAM_SESSION_NAME

class TelegramLogger:
    def __init__(self, chat_id=None):
        self.chat_id = chat_id or "me"  # Отправляем себе, если chat_id не указан
        self.client = None
        self.last_position = 0
        
    async def setup_client(self):
        """Настройка Telegram клиента"""
        try:
            self.client = TelegramClient(TELEGRAM_SESSION_NAME, TELEGRAM_API_ID, TELEGRAM_API_HASH)
            await self.client.start(phone=TELEGRAM_PHONE)
            print(f"✅ Telegram клиент подключен")
            return True
        except Exception as e:
            print(f"❌ Ошибка подключения к Telegram: {e}")
            return False
    
    async def send_log(self, message, log_type="INFO"):
        """Отправка сообщения в Telegram"""
        if not self.client:
            return False
            
        try:
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            formatted_message = f"📋 **{log_type}** [{timestamp}]\n\n{message}"
            
            await self.client.send_message(self.chat_id, formatted_message, parse_mode='markdown')
            return True
        except Exception as e:
            print(f"❌ Ошибка отправки в Telegram: {e}")
            return False
    
    async def send_file(self, file_path, caption=""):
        """Отправка файла в Telegram"""
        if not self.client or not os.path.exists(file_path):
            return False
            
        try:
            await self.client.send_file(self.chat_id, file_path, caption=caption)
            return True
        except Exception as e:
            print(f"❌ Ошибка отправки файла: {e}")
            return False
    
    async def monitor_logs(self, log_file, interval=30):
        """Мониторинг лог файла и отправка новых записей"""
        if not await self.setup_client():
            return
            
        print(f"📊 Начинаю мониторинг файла: {log_file}")
        await self.send_log(f"🚀 Мониторинг логов запущен\nФайл: `{log_file}`\nИнтервал: {interval} сек")
        
        while True:
            try:
                if os.path.exists(log_file):
                    with open(log_file, 'r', encoding='utf-8') as f:
                        f.seek(self.last_position)
                        new_content = f.read()
                        
                        if new_content:
                            # Отправляем новые записи
                            lines = new_content.strip().split('\n')
                            if lines and lines[0]:
                                await self.send_log(f"📝 Новые записи в логе:\n\n```\n{new_content[-1000:]}\n```")
                            
                            # Обновляем позицию
                            self.last_position = f.tell()
                else:
                    await self.send_log("⚠️ Лог файл не найден")
                    
            except Exception as e:
                await self.send_log(f"❌ Ошибка мониторинга: {e}")
                
            await asyncio.sleep(interval)
    
    async def send_current_logs(self, log_file, lines=50):
        """Отправка последних записей из лог файла"""
        if not await self.setup_client():
            return
            
        try:
            if os.path.exists(log_file):
                with open(log_file, 'r', encoding='utf-8') as f:
                    all_lines = f.readlines()
                    last_lines = all_lines[-lines:] if len(all_lines) > lines else all_lines
                    content = ''.join(last_lines)
                    
                    if content.strip():
                        await self.send_log(f"📋 Последние {len(last_lines)} записей:\n\n```\n{content}\n```")
                    else:
                        await self.send_log("📋 Лог файл пуст")
            else:
                await self.send_log("⚠️ Лог файл не найден")
                
        except Exception as e:
            await self.send_log(f"❌ Ошибка чтения лога: {e}")

async def main():
    """Главная функция"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Telegram Logger для BWEnews')
    parser.add_argument('--log-file', default='bwe_news_log.txt', help='Путь к лог файлу')
    parser.add_argument('--chat-id', help='ID чата для отправки (по умолчанию себе)')
    parser.add_argument('--interval', type=int, default=30, help='Интервал мониторинга в секундах')
    parser.add_argument('--lines', type=int, default=50, help='Количество строк для отправки')
    parser.add_argument('--mode', choices=['monitor', 'send'], default='monitor', 
                       help='Режим: monitor - мониторинг, send - отправить текущие логи')
    
    args = parser.parse_args()
    
    logger = TelegramLogger(args.chat_id)
    
    if args.mode == 'monitor':
        await logger.monitor_logs(args.log_file, args.interval)
    else:
        await logger.send_current_logs(args.log_file, args.lines)
        await logger.client.disconnect()

if __name__ == "__main__":
    asyncio.run(main())
