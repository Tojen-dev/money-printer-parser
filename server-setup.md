# 🚀 Настройка BWEnews Speed Test на Ubuntu 24.04

## 📋 Требования к серверу

- Ubuntu 24.04 LTS
- Минимум 1GB RAM
- Минимум 10GB свободного места
- Python 3.11+
- Доступ к интернету

## 🔧 Варианты установки

### Вариант 1: Автоматическая установка (рекомендуется)

```bash
# Скачиваем скрипт установки
wget https://raw.githubusercontent.com/your-repo/install.sh
chmod +x install.sh

# Запускаем установку
./install.sh
```

### Вариант 2: Ручная установка

```bash
# Обновляем систему
sudo apt update && sudo apt upgrade -y

# Устанавливаем Python 3.11
sudo apt install -y python3.11 python3.11-venv python3.11-pip

# Создаем директорию проекта
mkdir -p ~/bwe-news-speed-test
cd ~/bwe-news-speed-test

# Создаем виртуальное окружение
python3.11 -m venv venv
source venv/bin/activate

# Устанавливаем зависимости
pip install -r requirements.txt
```

### Вариант 3: Docker (для продвинутых пользователей)

```bash
# Устанавливаем Docker
sudo apt install -y docker.io docker-compose

# Клонируем проект
git clone <your-repo-url>
cd bwe-news-speed-test

# Запускаем через Docker Compose
docker-compose up -d
```

## ⚙️ Настройка конфигурации

### 1. Настройка Telegram

Отредактируйте файл `config.py`:

```python
# Telegram Configuration
TELEGRAM_API_ID = "your_api_id"
TELEGRAM_API_HASH = "your_api_hash"
TELEGRAM_PHONE = "your_phone_number"
TELEGRAM_CHANNEL_USERNAME = "@BWEnews"
```

### 2. Настройка прокси (опционально)

```python
# Proxy Configuration
USE_PROXY = True
PROXY_CONFIG = {
    "http": "http://user:pass@host:port",
    "https": "http://user:pass@host:port",
    "socks5": "socks5://user:pass@host:port"
}
```

### 3. Настройка логирования

```python
# Logging Configuration
NEWS_LOG_FILE = "/path/to/your/logs/bwe_news_log.txt"
LOG_LEVEL = "INFO"
```

## 🚀 Запуск и управление

### Systemd сервис (рекомендуется)

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

### Ручной запуск

```bash
cd ~/bwe-news-speed-test
source venv/bin/activate
python main.py
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

## 📊 Мониторинг

### Просмотр логов новостей

```bash
# В реальном времени
tail -f ~/bwe-news-speed-test/bwe_news_log.txt

# Последние 100 строк
tail -100 ~/bwe-news-speed-test/bwe_news_log.txt
```

### Системные логи

```bash
# Логи systemd
sudo journalctl -u bwe-news-speed-test -f

# Логи Docker
docker-compose logs -f
```

### Мониторинг ресурсов

```bash
# Использование CPU и памяти
htop

# Дисковое пространство
df -h

# Сетевые соединения
netstat -tulpn
```

## 🔧 Устранение неполадок

### Проблема: Telegram не подключается

```bash
# Проверяем логи
sudo journalctl -u bwe-news-speed-test | grep -i telegram

# Проверяем файл сессии
ls -la ~/bwe-news-speed-test/*.session*

# Удаляем старую сессию (если нужно)
rm ~/bwe-news-speed-test/news_trader_session.session
```

### Проблема: RSS не работает

```bash
# Проверяем доступность RSS
curl -I https://rss-public.bwe-ws.com/

# Проверяем прокси
curl --proxy http://user:pass@host:port https://rss-public.bwe-ws.com/
```

### Проблема: WebSocket не подключается

```bash
# Проверяем доступность WebSocket
wscat -c wss://bwenews-api.bwe-ws.com/ws

# Проверяем сетевые соединения
netstat -an | grep :443
```

## 🔄 Обновление

### Автоматическое обновление

```bash
# Останавливаем сервис
sudo systemctl stop bwe-news-speed-test

# Обновляем код
git pull origin main

# Обновляем зависимости
source venv/bin/activate
pip install -r requirements.txt

# Запускаем сервис
sudo systemctl start bwe-news-speed-test
```

### Docker обновление

```bash
# Останавливаем контейнеры
docker-compose down

# Пересобираем образ
docker-compose build --no-cache

# Запускаем
docker-compose up -d
```

## 📈 Оптимизация производительности

### Настройка системы

```bash
# Увеличиваем лимиты файлов
echo "* soft nofile 65536" | sudo tee -a /etc/security/limits.conf
echo "* hard nofile 65536" | sudo tee -a /etc/security/limits.conf

# Оптимизируем сетевые настройки
echo "net.core.rmem_max = 16777216" | sudo tee -a /etc/sysctl.conf
echo "net.core.wmem_max = 16777216" | sudo tee -a /etc/sysctl.conf
sudo sysctl -p
```

### Мониторинг производительности

```bash
# Установка инструментов мониторинга
sudo apt install -y htop iotop nethogs

# Мониторинг в реальном времени
htop
iotop
nethogs
```

## 🔒 Безопасность

### Firewall

```bash
# Устанавливаем UFW
sudo apt install -y ufw

# Настраиваем правила
sudo ufw default deny incoming
sudo ufw default allow outgoing
sudo ufw allow ssh
sudo ufw enable
```

### Обновления безопасности

```bash
# Автоматические обновления безопасности
sudo apt install -y unattended-upgrades
sudo dpkg-reconfigure -plow unattended-upgrades
```

## 📞 Поддержка

При возникновении проблем:

1. Проверьте логи: `sudo journalctl -u bwe-news-speed-test -f`
2. Проверьте статус сервиса: `sudo systemctl status bwe-news-speed-test`
3. Проверьте конфигурацию в `config.py`
4. Создайте issue в репозитории проекта

## 📝 Чек-лист установки

- [ ] Обновлена система
- [ ] Установлен Python 3.11
- [ ] Создано виртуальное окружение
- [ ] Установлены зависимости
- [ ] Настроена конфигурация
- [ ] Создан systemd сервис
- [ ] Протестирован запуск
- [ ] Настроен автозапуск
- [ ] Проверены логи
- [ ] Настроен мониторинг
