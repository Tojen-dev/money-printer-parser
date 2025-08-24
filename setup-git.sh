#!/bin/bash

# Скрипт для настройки Git репозитория BWEnews Speed Test
# Использование: ./setup-git.sh [github|gitlab|gitea]

set -e

# Цвета для вывода
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Проверка аргументов
if [ $# -eq 0 ]; then
    print_error "Укажите платформу: github, gitlab или gitea"
    echo "Использование: $0 [github|gitlab|gitea]"
    exit 1
fi

PLATFORM=$1

case $PLATFORM in
    github)
        BASE_URL="https://github.com"
        ;;
    gitlab)
        BASE_URL="https://gitlab.com"
        ;;
    gitea)
        BASE_URL="https://gitea.com"
        ;;
    *)
        print_error "Неизвестная платформа: $PLATFORM"
        echo "Поддерживаемые платформы: github, gitlab, gitea"
        exit 1
        ;;
esac

print_info "Настройка Git репозитория для $PLATFORM..."

# Запрос имени пользователя
read -p "Введите ваше имя пользователя на $PLATFORM: " USERNAME

if [ -z "$USERNAME" ]; then
    print_error "Имя пользователя не может быть пустым"
    exit 1
fi

REPO_URL="$BASE_URL/$USERNAME/bwe-news-speed-test.git"

print_info "Инициализация Git репозитория..."

# Инициализация Git
if [ ! -d ".git" ]; then
    git init
    print_success "Git репозиторий инициализирован"
else
    print_warning "Git репозиторий уже существует"
fi

# Добавление файлов
print_info "Добавление файлов в репозиторий..."
git add .

# Первый коммит
print_info "Создание первого коммита..."
git commit -m "Initial commit: BWEnews Speed Test"

# Переименование ветки в main
git branch -M main

# Добавление удаленного репозитория
print_info "Добавление удаленного репозитория..."
git remote add origin $REPO_URL

print_success "Удаленный репозиторий добавлен: $REPO_URL"

# Инструкции для пользователя
echo ""
print_info "📋 СЛЕДУЮЩИЕ ШАГИ:"
echo ""
echo "1. Создайте репозиторий на $PLATFORM:"
echo "   - Название: bwe-news-speed-test"
echo "   - Сделайте его публичным"
echo "   - НЕ инициализируйте с README"
echo ""
echo "2. После создания репозитория выполните:"
echo "   git push -u origin main"
echo ""
echo "3. На VPS выполните:"
echo "   git clone $REPO_URL"
echo "   cd bwe-news-speed-test"
echo "   ./install.sh"
echo ""

print_success "Настройка Git завершена!"
print_info "Не забудьте создать репозиторий на $PLATFORM перед push!"
