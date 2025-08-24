import asyncio
import logging
import feedparser
import requests
from datetime import datetime
import config

logger = logging.getLogger(__name__)


class RSSMonitor:
    def __init__(self, callback):
        self.callback = callback
        self.is_running = False
        self.last_entries = set()
        self.current_interval = config.RSS_UPDATE_INTERVAL
        self.consecutive_errors = 0
        self.max_interval = 60  # максимальный интервал в секундах
        self.min_interval = (
            3  # минимальный интервал в секундах (рискованно, но быстро!)
        )

    async def start(self):
        """Запуск мониторинга RSS ленты"""
        self.is_running = True
        logger.info(f"RSS мониторинг запущен для {config.RSS_URL}")

        while self.is_running:
            try:
                await self._check_rss()
                # Сбрасываем счетчик ошибок при успешном запросе
                if self.consecutive_errors > 0:
                    self.consecutive_errors = 0
                    # Быстро возвращаемся к минимальному интервалу при успешных запросах
                    if self.current_interval > self.min_interval:
                        self.current_interval = self.min_interval
                        logger.info(
                            f"RSS интервал восстановлен до {self.current_interval} секунд"
                        )

                await asyncio.sleep(self.current_interval)
            except Exception as e:
                logger.error(f"Ошибка RSS мониторинга: {e}")
                self.consecutive_errors += 1

                # Увеличиваем интервал при ошибках (более агрессивно)
                if self.consecutive_errors >= 2:
                    self.current_interval = min(
                        self.max_interval, self.current_interval + 15
                    )
                    logger.warning(
                        f"RSS интервал увеличен до {self.current_interval} секунд из-за ошибок"
                    )

                await asyncio.sleep(config.RETRY_DELAY)

    async def _check_rss(self):
        """Проверка RSS ленты на новые записи"""
        try:
            # Настройка прокси для RSS
            proxies = None
            if config.USE_PROXY:
                proxies = {
                    "http": config.PROXY_CONFIG["http"],
                    "https": config.PROXY_CONFIG["https"],
                }
                logger.info("Используется HTTP прокси для RSS")

            # Получаем RSS через requests с прокси
            response = requests.get(
                config.RSS_URL,
                proxies=proxies,
                timeout=10,
                headers={
                    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
                },
            )

            # Проверяем статус ответа
            if response.status_code == 429:  # Too Many Requests
                logger.warning(
                    "RSS сервер ограничил запросы (429). Увеличиваем интервал."
                )
                self.current_interval = min(
                    self.max_interval, self.current_interval + 15
                )
                return
            elif response.status_code == 503:  # Service Unavailable
                logger.warning(
                    "RSS сервер временно недоступен (503). Увеличиваем интервал."
                )
                self.current_interval = min(
                    self.max_interval, self.current_interval + 20
                )
                return

            response.raise_for_status()

            # Парсим RSS ленту
            feed = feedparser.parse(response.content)

            if feed.bozo:
                logger.warning(f"RSS feed имеет ошибки: {feed.bozo_exception}")

            # Обрабатываем новые записи
            for entry in feed.entries:
                # Создаем уникальный идентификатор для записи
                entry_id = f"{entry.get('id', '')}_{entry.get('published', '')}_{entry.get('title', '')}"

                if entry_id not in self.last_entries:
                    self.last_entries.add(entry_id)

                    # Ограничиваем размер множества для экономии памяти
                    if len(self.last_entries) > 1000:
                        self.last_entries = set(list(self.last_entries)[-500:])

                    await self._process_entry(entry)

        except requests.exceptions.RequestException as e:
            logger.error(f"Ошибка сетевого запроса RSS: {e}")
            raise
        except Exception as e:
            logger.error(f"Ошибка парсинга RSS: {e}")
            raise

    async def _process_entry(self, entry):
        """Обработка новой RSS записи"""
        try:
            timestamp = datetime.now()

            # Формируем текст новости
            title = entry.get("title", "")
            description = entry.get("description", "")
            summary = entry.get("summary", "")

            # Объединяем все доступные поля
            content_parts = []
            if title:
                content_parts.append(title)
            if description:
                content_parts.append(description)
            elif summary:
                content_parts.append(summary)

            content = "\n".join(content_parts)

            if content.strip():
                await self.callback(
                    {
                        "source": "rss",
                        "timestamp": timestamp,
                        "content": content,
                        "entry_id": entry.get("id", ""),
                        "link": entry.get("link", ""),
                        "published": entry.get("published", ""),
                        "raw_entry": entry,
                    }
                )

        except Exception as e:
            logger.error(f"Ошибка обработки RSS записи: {e}")

    async def stop(self):
        """Остановка мониторинга"""
        self.is_running = False
        logger.info("RSS мониторинг остановлен")
