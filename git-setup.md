# 🚀 Развертывание BWEnews Speed Test через Git

## 📋 Варианты развертывания

### Вариант 1: GitHub (рекомендуется)

#### 1. Создайте репозиторий на GitHub

- Зайдите на https://github.com
- Создайте новый репозиторий: `bwe-news-speed-test`
- Сделайте его публичным

#### 2. Загрузите файлы в репозиторий

```bash
# Инициализируйте Git в локальной папке
git init
git add .
git commit -m "Initial commit: BWEnews Speed Test"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/bwe-news-speed-test.git
git push -u origin main
```

#### 3. На VPS клонируйте репозиторий

```bash
git clone https://github.com/YOUR_USERNAME/bwe-news-speed-test.git
cd bwe-news-speed-test
```

### Вариант 2: GitLab

#### 1. Создайте проект на GitLab

- Зайдите на https://gitlab.com
- Создайте новый проект: `bwe-news-speed-test`

#### 2. Загрузите файлы

```bash
git init
git add .
git commit -m "Initial commit: BWEnews Speed Test"
git branch -M main
git remote add origin https://gitlab.com/YOUR_USERNAME/bwe-news-speed-test.git
git push -u origin main
```

#### 3. На VPS клонируйте

```bash
git clone https://gitlab.com/YOUR_USERNAME/bwe-news-speed-test.git
cd bwe-news-speed-test
```

### Вариант 3: Gitea (самый простой)

#### 1. Создайте аккаунт на Gitea

- Зайдите на https://gitea.com
- Создайте аккаунт
- Создайте репозиторий: `bwe-news-speed-test`

#### 2. Загрузите файлы

```bash
git init
git add .
git commit -m "Initial commit: BWEnews Speed Test"
git branch -M main
git remote add origin https://gitea.com/YOUR_USERNAME/bwe-news-speed-test.git
git push -u origin main
```

#### 3. На VPS клонируйте

```bash
git clone https://gitea.com/YOUR_USERNAME/bwe-news-speed-test.git
cd bwe-news-speed-test
```

## 🔧 Установка на VPS через Git

### Полная команда для VPS:

```bash
# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка Git и Python
sudo apt install -y git python3.11 python3.11-venv python3.11-pip python3-pip

# Клонирование репозитория
git clone https://github.com/YOUR_USERNAME/bwe-news-speed-test.git
cd bwe-news-speed-test

# Создание виртуального окружения
python3.11 -m venv venv
source venv/bin/activate

# Установка зависимостей
pip install --upgrade pip
pip install -r requirements.txt

# Создание systemd сервиса
sudo tee /etc/systemd/system/bwe-news-speed-test.service > /dev/null <<EOF
[Unit]
Description=BWEnews Speed Test
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$HOME/bwe-news-speed-test
Environment=PATH=$HOME/bwe-news-speed-test/venv/bin
ExecStart=$HOME/bwe-news-speed-test/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Настройка systemd
sudo systemctl daemon-reload
sudo systemctl enable bwe-news-speed-test

# Запуск сервиса
sudo systemctl start bwe-news-speed-test

# Проверка статуса
sudo systemctl status bwe-news-speed-test
```

## 📁 Структура файлов для Git

Убедитесь, что в репозитории есть все необходимые файлы:

```
bwe-news-speed-test/
├── main.py
├── config.py
├── telegram_monitor.py
├── rss_monitor.py
├── websocket_monitor.py
├── news_display.py
├── news_logger.py
├── requirements.txt
├── README.md
├── install.sh
└── .gitignore
```

## 🎯 Быстрая установка (одной командой)

Создайте файл `install.sh` в репозитории:

```bash
#!/bin/bash

# Быстрая установка BWEnews Speed Test
set -e

echo "🚀 Установка BWEnews Speed Test..."

# Обновление системы
sudo apt update && sudo apt upgrade -y

# Установка зависимостей
sudo apt install -y git python3.11 python3.11-venv python3.11-pip python3-pip

# Создание виртуального окружения
python3.11 -m venv venv
source venv/bin/activate

# Установка Python зависимостей
pip install --upgrade pip
pip install -r requirements.txt

# Создание systemd сервиса
sudo tee /etc/systemd/system/bwe-news-speed-test.service > /dev/null <<EOF
[Unit]
Description=BWEnews Speed Test
After=network.target

[Service]
Type=simple
User=$USER
WorkingDirectory=$PWD
Environment=PATH=$PWD/venv/bin
ExecStart=$PWD/venv/bin/python main.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
EOF

# Настройка systemd
sudo systemctl daemon-reload
sudo systemctl enable bwe-news-speed-test

echo "✅ Установка завершена!"
echo "🚀 Запуск: sudo systemctl start bwe-news-speed-test"
echo "📊 Статус: sudo systemctl status bwe-news-speed-test"
```

## 🔄 Обновление через Git

```bash
# На VPS
cd ~/bwe-news-speed-test
git pull origin main
sudo systemctl restart bwe-news-speed-test
```

## 📞 Поддержка

Если возникнут проблемы:

1. Проверьте права доступа к репозиторию
2. Убедитесь, что все файлы загружены
3. Проверьте логи: `sudo journalctl -u bwe-news-speed-test -f`
4. Проверьте статус: `sudo systemctl status bwe-news-speed-test`
