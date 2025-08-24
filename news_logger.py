import logging
from datetime import datetime
import os

import config

class NewsLogger:
    def __init__(self, log_file=None):
        self.log_file = log_file or config.NEWS_LOG_FILE
        self.logger = self._setup_logger()
        
    def _setup_logger(self):
        """Настройка логгера для новостей"""
        # Создаем логгер
        logger = logging.getLogger('news_logger')
        logger.setLevel(logging.INFO)
        
        # Очищаем существующие обработчики
        logger.handlers.clear()
        
        # Создаем обработчик для файла
        file_handler = logging.FileHandler(self.log_file, encoding='utf-8')
        file_handler.setLevel(logging.INFO)
        
        # Создаем форматтер
        formatter = logging.Formatter('%(message)s')
        file_handler.setFormatter(formatter)
        
        # Добавляем обработчик к логгеру
        logger.addHandler(file_handler)
        
        return logger
    
    def log_news(self, news_data):
        """Логирование новости в файл"""
        try:
            # Форматируем дату
            timestamp = news_data['timestamp']
            date_str = timestamp.strftime('%Y-%m-%d %H:%M:%S')
            
            # Получаем источник
            source = news_data['source']
            
            # Получаем текст новости
            content = news_data['content']
            
            # Создаем запись для лога
            log_entry = f"""
{date_str} | {source.upper()}
{content}
{'-' * 80}
"""
            
            # Записываем в файл
            self.logger.info(log_entry)
            
        except Exception as e:
            print(f"Ошибка логирования новости: {e}")
    
    def log_startup(self):
        """Логирование информации о запуске системы"""
        startup_info = f"""
{'=' * 80}
СИСТЕМА МОНИТОРИНГА BWEnews ЗАПУЩЕНА
Время запуска: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 80}

"""
        self.logger.info(startup_info)
    
    def log_shutdown(self):
        """Логирование информации о завершении работы"""
        shutdown_info = f"""

{'=' * 80}
СИСТЕМА МОНИТОРИНГА BWEnews ОСТАНОВЛЕНА
Время остановки: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
{'=' * 80}
"""
        self.logger.info(shutdown_info)
