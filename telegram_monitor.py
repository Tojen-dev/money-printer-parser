import asyncio
import logging
from datetime import datetime
from telethon import TelegramClient, events
from telethon.tl.types import Channel
from telethon.network import ConnectionTcpFull
import config

logger = logging.getLogger(__name__)


class TelegramMonitor:
    def __init__(self, callback):
        self.callback = callback
        self.client = None
        self.channel = None
        self.is_running = False
        self.last_message_id = 0
        self.processed_messages = set()  # Для избежания дублирования

    async def start(self):
        """Запуск мониторинга Telegram канала с максимальной скоростью"""
        try:
            # Настройка прокси для Telegram
            proxy_config = None
            if config.USE_PROXY:
                try:
                    # Пробуем сначала HTTP прокси, потом SOCKS5
                    proxy_url = config.PROXY_CONFIG["http"]
                    if proxy_url.startswith("http://"):
                        # Извлекаем данные из URL: http://user:pass@host:port
                        auth_part = proxy_url[7:]  # Убираем http://
                        if "@" in auth_part:
                            credentials, address = auth_part.split("@")
                            username, password = credentials.split(":")
                            host, port = address.split(":")

                            proxy_config = {
                                "proxy_type": "http",
                                "addr": host,
                                "port": int(port),
                                "username": username,
                                "password": password,
                                "rdns": True,
                            }
                            logger.info(
                                f"Используется HTTP прокси для Telegram: {host}:{port}"
                            )
                        else:
                            # Без аутентификации
                            host, port = auth_part.split(":")
                            proxy_config = {
                                "proxy_type": "http",
                                "addr": host,
                                "port": int(port),
                                "username": None,
                                "password": None,
                                "rdns": True,
                            }
                            logger.info(
                                f"Используется HTTP прокси для Telegram: {host}:{port}"
                            )
                except Exception as e:
                    logger.warning(f"Ошибка настройки прокси для Telegram: {e}")

            # Создаем клиент с вашими учетными данными
            self.client = TelegramClient(
                config.TELEGRAM_SESSION_NAME,
                api_id=config.TELEGRAM_API_ID,
                api_hash=config.TELEGRAM_API_HASH,
                device_model="Desktop",
                system_version="Windows 10",
                app_version="1.0",
                lang_code="en",
                # Оптимизации для скорости
                connection_retries=5,
                retry_delay=1,
                timeout=10,
                auto_reconnect=True,
                proxy=proxy_config,
            )

            # Подключаемся к Telegram
            await self.client.start(phone=config.TELEGRAM_PHONE)

            # Получаем информацию о канале
            self.channel = await self.client.get_entity(
                config.TELEGRAM_CHANNEL_USERNAME
            )
            logger.info(f"Подключен к каналу: {self.channel.title}")

            # Получаем последние сообщения для установки базового ID
            messages = await self.client.get_messages(self.channel, limit=1)
            if messages:
                self.last_message_id = messages[0].id
                logger.info(f"Базовый ID сообщения: {self.last_message_id}")

            # Регистрируем обработчик новых сообщений с максимальной скоростью
            @self.client.on(events.NewMessage(chats=self.channel))
            async def handle_new_message(event):
                await self._process_message(event.message)

            # Запускаем основной мониторинг через события (самый быстрый способ)
            self.is_running = True

            logger.info(
                f"Telegram мониторинг запущен для канала {config.TELEGRAM_CHANNEL_USERNAME}"
            )

            # Держим клиент активным
            await self.client.run_until_disconnected()

        except Exception as e:
            logger.error(f"Ошибка запуска Telegram мониторинга: {e}")
            return False

    async def _process_message(self, message):
        """Обработка нового сообщения с максимальной скоростью"""
        try:
            # Проверяем, не обрабатывали ли мы уже это сообщение
            if message.id in self.processed_messages:
                return

            self.processed_messages.add(message.id)

            # Ограничиваем размер множества обработанных сообщений
            if len(self.processed_messages) > 1000:
                self.processed_messages = set(list(self.processed_messages)[-500:])

            timestamp = datetime.now()

            # Извлекаем текст сообщения
            if hasattr(message, "text") and message.text:
                news_text = message.text
            elif hasattr(message, "raw_text") and message.raw_text:
                news_text = message.raw_text
            elif hasattr(message, "message") and message.message:
                news_text = message.message
            else:
                news_text = ""

            # Проверяем, что это не пустое сообщение
            if news_text.strip():
                # Немедленно отправляем callback
                await self.callback(
                    {
                        "source": "telegram",
                        "timestamp": timestamp,
                        "content": news_text,
                        "message_id": message.id,
                        "raw_message": message,
                    }
                )

                logger.debug(f"Обработано Telegram сообщение ID: {message.id}")

        except Exception as e:
            logger.error(f"Ошибка обработки Telegram сообщения: {e}")

    async def stop(self):
        """Остановка мониторинга"""
        self.is_running = False
        if self.client:
            await self.client.disconnect()
        logger.info("Telegram мониторинг остановлен")
