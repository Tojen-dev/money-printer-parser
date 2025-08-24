# BWEnews Speed Test 🚀

Система для тестирования скорости получения новостей из трех разных источников BWEnews.

## 📋 Описание

Это приложение параллельно мониторит три источника новостей BWEnews и выводит время получения каждой новости с указанием источника:

1. **📱 Telegram канал** - максимально быстрое получение сообщений через Telegram Bot API
2. **📡 RSS лента** - периодический опрос RSS feed
3. **🔌 WebSocket API** - real-time подключение к WebSocket API

## 🎯 Возможности

- ⚡ Параллельный мониторинг всех источников
- 🕐 Точное время получения новостей (с миллисекундами)
- 📊 Статистика по источникам
- 🎨 Красивый интерфейс с иконками
- 📝 Логирование всех событий
- 🔄 Автоматическое переподключение при ошибках

## 🚀 Установка

### Локальная установка

1. **Клонируйте репозиторий:**
```bash
git clone <repository-url>
cd money-printer-parser
```

2. **Установите зависимости:**
```bash
pip install -r requirements.txt
```

3. **Настройте Telegram (опционально):**
   - Учетные данные уже настроены в `config.py`
   - При первом запуске потребуется ввести код подтверждения из SMS
   - Сессия сохранится автоматически для последующих запусков

### Установка на сервер Ubuntu 24.04

#### Автоматическая установка (рекомендуется)

```bash
# Скачиваем скрипт установки
wget https://raw.githubusercontent.com/your-repo/install.sh
chmod +x install.sh

# Запускаем установку
./install.sh
```

#### Ручная установка

См. подробную инструкцию в файле [server-setup.md](server-setup.md)

#### Docker установка

```bash
# Устанавливаем Docker
sudo apt install -y docker.io docker-compose

# Запускаем через Docker Compose
docker-compose up -d
```

## 🎮 Использование

### Запуск приложения:
```bash
python main.py
```

### Что вы увидите:

1. **Информация о запуске** - список всех источников
2. **Статистика** - таблица с количеством новостей по источникам
3. **Новости** - каждая новость отображается с:
   - Иконкой источника (📱📡🔌)
   - Временем получения
   - Содержимым новости

### Остановка:
Нажмите `Ctrl+C` для корректного завершения работы.

## 🖥️ Управление на сервере

### Systemd сервис

```bash
# Запуск
sudo systemctl start bwe-news-speed-test

# Остановка
sudo systemctl stop bwe-news-speed-test

# Статус
sudo systemctl status bwe-news-speed-test

# Автозапуск
sudo systemctl enable bwe-news-speed-test

# Просмотр логов
sudo journalctl -u bwe-news-speed-test -f
```

### Docker

```bash
# Запуск
docker-compose up -d

# Остановка
docker-compose down

# Логи
docker-compose logs -f
```

### Мониторинг логов

```bash
# Новости в реальном времени
tail -f ~/bwe-news-speed-test/bwe_news_log.txt

# Последние новости
tail -100 ~/bwe-news-speed-test/bwe_news_log.txt
```

## 📊 Источники новостей

### 1. Telegram канал (@BWEnews)
- **Скорость:** Максимальная (real-time)
- **Требования:** Telegram Bot Token
- **Иконка:** 📱

### 2. RSS лента (https://rss-public.bwe-ws.com/)
- **Скорость:** Адаптивная (15-60 секунд, автоматическая регулировка)
- **Требования:** Нет
- **Иконка:** 📡
- **Особенности:** Умная система интервалов, избегает ограничений сервера

### 3. WebSocket API (wss://bwenews-api.bwe-ws.com/ws)
- **Скорость:** Высокая (real-time)
- **Требования:** Нет
- **Иконка:** 🔌

## ⚙️ Конфигурация

Основные настройки в файле `config.py`:

```python
# Интервалы обновления
RSS_UPDATE_INTERVAL = 5  # секунды
WEBSOCKET_PING_INTERVAL = 30  # секунды

# Прокси настройки
USE_PROXY = True  # Включить/выключить прокси
PROXY_CONFIG = {
    "http": "http://127.0.0.1:7890",
    "https": "http://127.0.0.1:7890", 
    "socks5": "socks5://127.0.0.1:7890"
}

# Иконки источников
SOURCE_ICONS = {
    'telegram': '📱',
    'rss': '📡', 
    'websocket': '🔌'
}
```

### 🔧 Настройка прокси

Для использования прокси:

1. **Включите прокси** в `config.py`: `USE_PROXY = True`
2. **Настройте адрес прокси** в `PROXY_CONFIG`
3. **Поддерживаемые типы прокси:**
   - HTTP/HTTPS для RSS и WebSocket
   - SOCKS5 для Telegram

## 📁 Структура проекта

```
money-printer-parser/
├── main.py                 # Главный файл приложения
├── config.py              # Конфигурация
├── telegram_monitor.py    # Мониторинг Telegram
├── rss_monitor.py         # Мониторинг RSS
├── websocket_monitor.py   # Мониторинг WebSocket
├── news_display.py        # Отображение новостей
├── requirements.txt       # Зависимости
├── env_example.txt        # Пример конфигурации
├── README.md             # Документация
└── bwe_news.log          # Лог файл (создается автоматически)
```

## 🔧 Устранение неполадок

### Telegram не работает:
- Проверьте правильность токена в `.env`
- Убедитесь, что бот добавлен в канал @BWEnews

### WebSocket не подключается:
- Проверьте интернет соединение
- WebSocket автоматически переподключится при ошибках

### RSS не обновляется:
- Проверьте доступность https://rss-public.bwe-ws.com/
- RSS может иметь задержки в обновлении

## 📈 Результаты тестирования

Приложение покажет:
- Какие источники быстрее получают новости
- Статистику по каждому источнику
- Время задержки между источниками

## 🤝 Вклад в проект

1. Fork репозитория
2. Создайте feature branch
3. Внесите изменения
4. Создайте Pull Request

## 📄 Лицензия

MIT License

## 🔗 Ссылки

- [BWEnews RSS Feed](https://rss-public.bwe-ws.com/)
- [BWEnews WebSocket API](https://telegra.ph/BWEnews-API-documentation-06-19)
- [Telegram Bot API](https://core.telegram.org/bots/api)
