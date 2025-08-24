# 🔄 Руководство по миграции на сервер

## 📋 Подготовка к миграции

### 1. Экспорт текущей конфигурации

Перед миграцией сохраните текущие настройки:

```bash
# Копируем конфигурацию
cp config.py config_backup.py

# Экспортируем переменные окружения
cat > .env << EOF
TELEGRAM_API_ID=29644709
TELEGRAM_API_HASH=b7d2e834f95f653c85e1954e0f68b4c7
TELEGRAM_PHONE=+380939691649
TELEGRAM_SESSION_NAME=news_trader_session
USE_PROXY=false
EOF
```

### 2. Подготовка файлов сессии Telegram

```bash
# Копируем файл сессии (если есть)
cp news_trader_session.session session_backup.session

# Или создаем новый
echo "При первом запуске на сервере потребуется повторная авторизация"
```

## 🚀 Варианты миграции

### Вариант 1: Автоматическая миграция

```bash
# Используем быстрый скрипт развертывания
./quick-deploy.sh username@server-ip
```

### Вариант 2: Ручная миграция

#### Шаг 1: Подготовка сервера

```bash
# Подключаемся к серверу
ssh username@server-ip

# Создаем директорию
mkdir -p ~/bwe-news-speed-test
cd ~/bwe-news-speed-test
```

#### Шаг 2: Копирование файлов

```bash
# С локальной машины
scp -r ./* username@server-ip:~/bwe-news-speed-test/
```

#### Шаг 3: Установка на сервере

```bash
# На сервере
cd ~/bwe-news-speed-test

# Запускаем установку
./install.sh
```

### Вариант 3: Docker миграция

```bash
# Копируем Docker файлы
scp docker-compose.yml Dockerfile env.example username@server-ip:~/

# На сервере
docker-compose up -d
```

## ⚙️ Настройка после миграции

### 1. Обновление конфигурации

Отредактируйте `config.py` на сервере:

```python
# Обновите пути для логов
NEWS_LOG_FILE = "/home/username/bwe-news-speed-test/bwe_news_log.txt"

# Настройте прокси (если нужно)
USE_PROXY = True
PROXY_CONFIG = {
    "http": "http://user:pass@host:port",
    "https": "http://user:pass@host:port",
}
```

### 2. Настройка автозапуска

```bash
# Включаем автозапуск
sudo systemctl enable bwe-news-speed-test

# Проверяем статус
sudo systemctl status bwe-news-speed-test
```

### 3. Настройка мониторинга

```bash
# Создаем скрипт мониторинга
cat > ~/monitor.sh << 'EOF'
#!/bin/bash
echo "=== BWEnews Speed Test Status ==="
sudo systemctl status bwe-news-speed-test --no-pager
echo ""
echo "=== Recent News ==="
tail -10 ~/bwe-news-speed-test/bwe_news_log.txt
echo ""
echo "=== System Resources ==="
df -h | grep -E "(Filesystem|/dev/)"
free -h
EOF

chmod +x ~/monitor.sh
```

## 🔧 Устранение проблем миграции

### Проблема: Telegram не авторизуется

```bash
# Удаляем старую сессию
rm ~/bwe-news-speed-test/news_trader_session.session

# Перезапускаем сервис
sudo systemctl restart bwe-news-speed-test

# Проверяем логи
sudo journalctl -u bwe-news-speed-test -f
```

### Проблема: Недостаточно прав

```bash
# Проверяем права на файлы
ls -la ~/bwe-news-speed-test/

# Исправляем права
chmod +x ~/bwe-news-speed-test/*.py
chmod +x ~/bwe-news-speed-test/*.sh

# Проверяем права systemd
sudo systemctl status bwe-news-speed-test
```

### Проблема: Прокси не работает

```bash
# Тестируем прокси
curl --proxy http://user:pass@host:port https://api.telegram.org

# Проверяем настройки в config.py
grep -A 10 "PROXY_CONFIG" ~/bwe-news-speed-test/config.py
```

## 📊 Проверка после миграции

### 1. Проверка сервиса

```bash
# Статус сервиса
sudo systemctl status bwe-news-speed-test

# Логи в реальном времени
sudo journalctl -u bwe-news-speed-test -f
```

### 2. Проверка источников

```bash
# Проверяем логи новостей
tail -f ~/bwe-news-speed-test/bwe_news_log.txt

# Проверяем статистику
grep -c "RSS\|TELEGRAM\|WEBSOCKET" ~/bwe-news-speed-test/bwe_news_log.txt
```

### 3. Проверка производительности

```bash
# Использование ресурсов
htop

# Сетевые соединения
netstat -tulpn | grep python
```

## 🔄 Откат изменений

### Восстановление из резервной копии

```bash
# Останавливаем сервис
sudo systemctl stop bwe-news-speed-test

# Восстанавливаем конфигурацию
cp config_backup.py config.py

# Перезапускаем
sudo systemctl start bwe-news-speed-test
```

### Полная переустановка

```bash
# Удаляем сервис
sudo systemctl stop bwe-news-speed-test
sudo systemctl disable bwe-news-speed-test
sudo rm /etc/systemd/system/bwe-news-speed-test.service

# Удаляем файлы
rm -rf ~/bwe-news-speed-test

# Переустанавливаем
./install.sh
```

## 📞 Поддержка миграции

При проблемах с миграцией:

1. Проверьте логи: `sudo journalctl -u bwe-news-speed-test -f`
2. Проверьте конфигурацию: `cat ~/bwe-news-speed-test/config.py`
3. Проверьте права: `ls -la ~/bwe-news-speed-test/`
4. Проверьте сеть: `ping api.telegram.org`

## 📝 Чек-лист миграции

- [ ] Создана резервная копия конфигурации
- [ ] Экспортированы переменные окружения
- [ ] Скопированы файлы на сервер
- [ ] Установлены зависимости
- [ ] Настроен systemd сервис
- [ ] Протестирована авторизация Telegram
- [ ] Проверена работа всех источников
- [ ] Настроен автозапуск
- [ ] Создан мониторинг
- [ ] Документированы изменения
