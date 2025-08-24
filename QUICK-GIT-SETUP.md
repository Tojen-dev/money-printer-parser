# ⚡ Быстрое развертывание через Git

## 🚀 Пошаговая инструкция

### Шаг 1: Настройка Git репозитория

#### Выберите платформу и выполните:

```bash
# Для GitHub
./setup-git.sh github

# Для GitLab
./setup-git.sh gitlab

# Для Gitea
./setup-git.sh gitea
```

#### Следуйте инструкциям скрипта:

1. Введите имя пользователя
2. Создайте репозиторий на выбранной платформе
3. Выполните `git push -u origin main`

### Шаг 2: Установка на VPS

#### Выполните на VPS:

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Git и Python
sudo apt install -y git python3.11 python3.11-venv python3.11-pip python3-pip

# Клонирование репозитория (замените на ваш URL)
git clone https://github.com/YOUR_USERNAME/bwe-news-speed-test.git
cd bwe-news-speed-test

# Запуск установки
./install.sh
```

### Шаг 3: Проверка работы

```bash
# Статус сервиса
sudo systemctl status bwe-news-speed-test

# Логи
sudo journalctl -u bwe-news-speed-test -f

# Новости
tail -f bwe_news_log.txt
```

## 📋 Команды управления

```bash
# Запуск/остановка
sudo systemctl start bwe-news-speed-test
sudo systemctl stop bwe-news-speed-test

# Перезапуск
sudo systemctl restart bwe-news-speed-test

# Автозапуск
sudo systemctl enable bwe-news-speed-test
```

## 🔄 Обновление

```bash
# На VPS
cd ~/bwe-news-speed-test
git pull origin main
sudo systemctl restart bwe-news-speed-test
```

## 🎯 Готово!

Ваша система мониторинга BWEnews работает!

- 📱 **Telegram**: @BWEnews
- 📡 **RSS**: https://rss-public.bwe-ws.com/
- 🔌 **WebSocket**: wss://bwenews-api.bwe-ws.com/ws
- 📝 **Логи**: bwe_news_log.txt
