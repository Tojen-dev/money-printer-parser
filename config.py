import os
from dotenv import load_dotenv

load_dotenv()

# Telegram Configuration
TELEGRAM_API_ID = "29644709"
TELEGRAM_API_HASH = "b7d2e834f95f653c85e1954e0f68b4c7"
TELEGRAM_PHONE = "+380939691649"
TELEGRAM_SESSION_NAME = "news_trader_session"
TELEGRAM_CHANNEL_USERNAME = "@BWEnews"  # Канал BWEnews

# RSS Configuration
RSS_URL = "https://rss-public.bwe-ws.com/"
RSS_UPDATE_INTERVAL = 3  # секунды (уменьшено для более быстрого получения)

# WebSocket Configuration
WEBSOCKET_URL = "wss://bwenews-api.bwe-ws.com/ws"
WEBSOCKET_PING_INTERVAL = 30  # секунды

# Proxy Configuration
USE_PROXY = False  # Временно отключаем прокси для тестирования Telegram
PROXY_CONFIG = {
    "http": "http://CMNR730357:GNPSVW25@5.249.188.170:2236",  # HTTP прокси с аутентификацией
    "https": "http://CMNR730357:GNPSVW25@5.249.188.170:2236",  # HTTPS прокси с аутентификацией
    "socks5": "socks5://CMNR730357:GNPSVW25@5.249.188.170:2236",  # SOCKS5 прокси с аутентификацией
}

# General Configuration
LOG_LEVEL = "INFO"
MAX_RETRIES = 3
RETRY_DELAY = 5  # секунды

# Icons for different sources
SOURCE_ICONS = {"telegram": "📱", "rss": "📡", "websocket": "🔌"}

# Logging Configuration
NEWS_LOG_FILE = "bwe_news_log.txt"  # Файл для логирования новостей
