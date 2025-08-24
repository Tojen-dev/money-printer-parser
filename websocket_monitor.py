import asyncio
import logging
import json
import websocket
from datetime import datetime
import config

logger = logging.getLogger(__name__)


class WebSocketMonitor:
    def __init__(self, callback):
        self.callback = callback
        self.ws = None
        self.is_running = False

    async def start(self):
        """Запуск мониторинга WebSocket"""
        self.is_running = True
        logger.info(f"WebSocket мониторинг запущен для {config.WEBSOCKET_URL}")

        while self.is_running:
            try:
                await self._connect_and_monitor()
            except Exception as e:
                logger.error(f"Ошибка WebSocket соединения: {e}")
                if self.is_running:
                    await asyncio.sleep(config.RETRY_DELAY)

    async def _connect_and_monitor(self):
        """Подключение и мониторинг WebSocket"""
        try:
                        # WebSocket не поддерживает прокси напрямую
            if config.USE_PROXY:
                logger.warning("WebSocket не поддерживает прокси. Используется прямое соединение.")

            # Создаем WebSocket соединение (без прокси, так как библиотека не поддерживает)
            self.ws = websocket.WebSocketApp(
                config.WEBSOCKET_URL,
                on_open=self._on_open,
                on_message=self._on_message,
                on_error=self._on_error,
                on_close=self._on_close,
            )

            # Запускаем WebSocket в отдельном потоке
            loop = asyncio.get_event_loop()
            await loop.run_in_executor(None, self.ws.run_forever)

        except Exception as e:
            logger.error(f"Ошибка WebSocket соединения: {e}")

    def _on_open(self, ws):
        """Обработчик открытия соединения"""
        logger.info("WebSocket соединение установлено")

    def _on_message(self, ws, message):
        """Обработчик входящих сообщений"""
        try:
            # Проверяем, не является ли это pong сообщением
            if message.strip() == "pong":
                logger.debug("Получен pong")
                return

            # Парсим JSON сообщение
            data = json.loads(message)

            # Создаем событие для обработки в основном потоке
            asyncio.create_task(self._process_message(data))

        except json.JSONDecodeError:
            logger.warning(f"Получено невалидное JSON сообщение: {message}")
        except Exception as e:
            logger.error(f"Ошибка обработки WebSocket сообщения: {e}")

    def _on_error(self, ws, error):
        """Обработчик ошибок WebSocket"""
        logger.error(f"WebSocket ошибка: {error}")

    def _on_close(self, ws, close_status_code, close_msg):
        """Обработчик закрытия соединения"""
        logger.info(f"WebSocket соединение закрыто: {close_status_code} - {close_msg}")

    async def _process_message(self, data):
        """Обработка WebSocket сообщения"""
        try:
            timestamp = datetime.now()

            # Извлекаем данные из сообщения
            source_name = data.get("source_name", "BWENEWS")
            news_title = data.get("news_title", "")
            coins_included = data.get("coins_included", [])
            url = data.get("url", "")
            msg_timestamp = data.get("timestamp", "")

            # Формируем контент новости
            content_parts = []
            if news_title:
                content_parts.append(news_title)
            if coins_included:
                content_parts.append(f"Coins: {', '.join(coins_included)}")
            if url:
                content_parts.append(f"URL: {url}")

            content = "\n".join(content_parts)

            if content.strip():
                await self.callback(
                    {
                        "source": "websocket",
                        "timestamp": timestamp,
                        "content": content,
                        "source_name": source_name,
                        "coins_included": coins_included,
                        "url": url,
                        "msg_timestamp": msg_timestamp,
                        "raw_data": data,
                    }
                )

        except Exception as e:
            logger.error(f"Ошибка обработки WebSocket данных: {e}")

    async def stop(self):
        """Остановка мониторинга"""
        self.is_running = False

        if self.ws:
            self.ws.close()

        logger.info("WebSocket мониторинг остановлен")
