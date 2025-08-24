#!/usr/bin/env python3
"""
BWEnews Speed Test - Система тестирования скорости получения новостей
Мониторит три источника: Telegram, RSS, WebSocket
"""

import asyncio
import logging
import signal
import sys
from datetime import datetime

from telegram_monitor import TelegramMonitor
from rss_monitor import RSSMonitor
from websocket_monitor import WebSocketMonitor
from news_display import NewsDisplay
from news_logger import NewsLogger
import config

# Настройка логирования
logging.basicConfig(
    level=getattr(logging, config.LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bwe_news.log'),
        logging.StreamHandler(sys.stdout)
    ]
)

logger = logging.getLogger(__name__)

class NewsSpeedTest:
    def __init__(self):
        self.display = NewsDisplay()
        self.news_logger = NewsLogger()
        self.monitors = {}
        self.is_running = False
        
    async def news_callback(self, news_data):
        """Callback для обработки новостей от всех источников"""
        try:
            # Добавляем дополнительную информацию
            news_data['received_at'] = datetime.now()
            
            # Отображаем новость
            self.display.display_news(news_data)
            
            # Логируем новость в файл
            self.news_logger.log_news(news_data)
            
        except Exception as e:
            logger.error(f"Ошибка в callback: {e}")
    
    async def start_monitoring(self):
        """Запуск мониторинга всех источников"""
        self.is_running = True
        
        # Логируем запуск системы
        self.news_logger.log_startup()
        
        # Отображаем информацию о запуске
        self.display.display_startup_info()
        
        # Создаем задачи для каждого монитора
        tasks = []
        
        # Telegram мониторинг
        telegram_monitor = TelegramMonitor(self.news_callback)
        self.monitors['telegram'] = telegram_monitor
        tasks.append(asyncio.create_task(telegram_monitor.start()))
        logger.info("Telegram мониторинг добавлен")
        
        # RSS мониторинг
        rss_monitor = RSSMonitor(self.news_callback)
        self.monitors['rss'] = rss_monitor
        tasks.append(asyncio.create_task(rss_monitor.start()))
        logger.info("RSS мониторинг добавлен")
        
        # WebSocket мониторинг
        websocket_monitor = WebSocketMonitor(self.news_callback)
        self.monitors['websocket'] = websocket_monitor
        tasks.append(asyncio.create_task(websocket_monitor.start()))
        logger.info("WebSocket мониторинг добавлен")
        
        # Ждем завершения всех задач
        try:
            await asyncio.gather(*tasks, return_exceptions=True)
        except Exception as e:
            logger.error(f"Ошибка в мониторинге: {e}")
    
    async def stop_monitoring(self):
        """Остановка всех мониторов"""
        self.is_running = False
        
        logger.info("Остановка всех мониторов...")
        
        # Останавливаем все мониторы
        for name, monitor in self.monitors.items():
            try:
                await monitor.stop()
                logger.info(f"Монитор {name} остановлен")
            except Exception as e:
                logger.error(f"Ошибка остановки монитора {name}: {e}")
        
        # Логируем завершение работы
        self.news_logger.log_shutdown()
        
        # Отображаем информацию о завершении
        self.display.display_shutdown()
    
    def signal_handler(self, signum, frame):
        """Обработчик сигналов для корректного завершения"""
        logger.info(f"Получен сигнал {signum}, завершение работы...")
        asyncio.create_task(self.stop_monitoring())

async def main():
    """Главная функция приложения"""
    # Создаем экземпляр тестера
    speed_test = NewsSpeedTest()
    
    # Регистрируем обработчики сигналов
    signal.signal(signal.SIGINT, speed_test.signal_handler)
    signal.signal(signal.SIGTERM, speed_test.signal_handler)
    
    try:
        # Запускаем мониторинг
        await speed_test.start_monitoring()
    except KeyboardInterrupt:
        logger.info("Получен сигнал прерывания")
    except Exception as e:
        logger.error(f"Критическая ошибка: {e}")
        speed_test.display.display_error(str(e))
    finally:
        # Останавливаем мониторинг
        await speed_test.stop_monitoring()

if __name__ == "__main__":
    # Проверяем наличие необходимых зависимостей
    try:
        import telethon
        import feedparser
        import websocket
        import rich
    except ImportError as e:
        print(f"❌ Ошибка: Не установлены необходимые зависимости: {e}")
        print("Установите зависимости командой: pip install -r requirements.txt")
        sys.exit(1)
    
    # Запускаем приложение
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n🛑 Приложение остановлено пользователем")
    except Exception as e:
        print(f"❌ Критическая ошибка: {e}")
        sys.exit(1)
