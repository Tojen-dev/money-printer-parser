# ⚡ Быстрый старт BWEnews Speed Test

## 🚀 Развертывание на сервер за 5 минут

### 1. Подготовка сервера

```bash
# Подключаемся к серверу
ssh username@your-server-ip

# Создаем директорию
mkdir -p ~/bwe-news-speed-test
cd ~/bwe-news-speed-test
```

### 2. Автоматическая установка

```bash
# Скачиваем и запускаем установку
wget -O install.sh https://raw.githubusercontent.com/your-repo/install.sh
chmod +x install.sh
./install.sh
```

### 3. Настройка конфигурации

```bash
# Редактируем конфигурацию
nano config.py

# Основные настройки:
# - TELEGRAM_API_ID, TELEGRAM_API_HASH, TELEGRAM_PHONE
# - USE_PROXY (True/False)
# - PROXY_CONFIG (если нужен прокси)
```

### 4. Запуск

```bash
# Запускаем сервис
sudo systemctl start bwe-news-speed-test

# Проверяем статус
sudo systemctl status bwe-news-speed-test

# Включаем автозапуск
sudo systemctl enable bwe-news-speed-test
```

### 5. Мониторинг

```bash
# Логи в реальном времени
sudo journalctl -u bwe-news-speed-test -f

# Новости в реальном времени
tail -f ~/bwe-news-speed-test/bwe_news_log.txt

# Статистика
tail -100 ~/bwe-news-speed-test/bwe_news_log.txt | grep -c "RSS\|TELEGRAM\|WEBSOCKET"
```

## 📋 Основные команды

```bash
# Управление сервисом
sudo systemctl start bwe-news-speed-test    # Запуск
sudo systemctl stop bwe-news-speed-test     # Остановка
sudo systemctl restart bwe-news-speed-test  # Перезапуск
sudo systemctl status bwe-news-speed-test   # Статус

# Логи
sudo journalctl -u bwe-news-speed-test -f   # Системные логи
tail -f bwe_news_log.txt                    # Логи новостей

# Обновление
git pull origin main                        # Обновить код
sudo systemctl restart bwe-news-speed-test  # Перезапустить
```

## 🔧 Быстрое устранение проблем

### Telegram не работает

```bash
# Удалить сессию и перезапустить
rm news_trader_session.session
sudo systemctl restart bwe-news-speed-test
```

### RSS не работает

```bash
# Проверить доступность
curl -I https://rss-public.bwe-ws.com/
```

### WebSocket не работает

```bash
# Проверить соединение
wscat -c wss://bwenews-api.bwe-ws.com/ws
```

## 📊 Проверка работы

```bash
# Создаем скрипт проверки
cat > check-status.sh << 'EOF'
#!/bin/bash
echo "=== BWEnews Speed Test Status ==="
sudo systemctl status bwe-news-speed-test --no-pager
echo ""
echo "=== Recent News (last 5) ==="
tail -5 ~/bwe-news-speed-test/bwe_news_log.txt
echo ""
echo "=== Statistics ==="
echo "RSS: $(grep -c "RSS" ~/bwe-news-speed-test/bwe_news_log.txt)"
echo "Telegram: $(grep -c "TELEGRAM" ~/bwe-news-speed-test/bwe_news_log.txt)"
echo "WebSocket: $(grep -c "WEBSOCKET" ~/bwe-news-speed-test/bwe_news_log.txt)"
EOF

chmod +x check-status.sh
./check-status.sh
```

## 🎯 Готово!

Ваша система мониторинга BWEnews работает!

- 📱 **Telegram**: Получает новости из @BWEnews
- 📡 **RSS**: Опрашивает каждые 3 секунды
- 🔌 **WebSocket**: Real-time новости
- 📝 **Логи**: Сохраняются в `bwe_news_log.txt`

## 📞 Поддержка

- 📖 Полная документация: `server-setup.md`
- 🔄 Миграция: `migration-guide.md`
- 🐛 Проблемы: Проверьте логи выше
