#!/bin/bash

# Скрипт для отправки логов в Telegram
# Использование: ./telegram-logs.sh [start|stop|status|send|monitor]

LOG_FILE="bwe_news_log.txt"
PID_FILE="/tmp/telegram-logger.pid"

case "$1" in
    start)
        echo "🚀 Запуск Telegram логгера..."
        if [ -f "$PID_FILE" ]; then
            echo "⚠️ Логгер уже запущен (PID: $(cat $PID_FILE))"
            exit 1
        fi
        
        cd ~/money-printer-parser
        source venv/bin/activate
        
        # Запускаем в фоне
        nohup python telegram-logger.py --mode monitor --interval 30 > /tmp/telegram-logger.log 2>&1 &
        echo $! > "$PID_FILE"
        echo "✅ Telegram логгер запущен (PID: $(cat $PID_FILE))"
        ;;
        
    stop)
        echo "⏹️ Остановка Telegram логгера..."
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if kill -0 "$PID" 2>/dev/null; then
                kill "$PID"
                rm -f "$PID_FILE"
                echo "✅ Telegram логгер остановлен"
            else
                echo "⚠️ Процесс уже не запущен"
                rm -f "$PID_FILE"
            fi
        else
            echo "⚠️ PID файл не найден"
        fi
        ;;
        
    status)
        echo "📊 Статус Telegram логгера..."
        if [ -f "$PID_FILE" ]; then
            PID=$(cat "$PID_FILE")
            if kill -0 "$PID" 2>/dev/null; then
                echo "✅ Запущен (PID: $PID)"
                echo "📋 Логи процесса:"
                tail -5 /tmp/telegram-logger.log 2>/dev/null || echo "Логи не найдены"
            else
                echo "❌ Не запущен (процесс завершен)"
                rm -f "$PID_FILE"
            fi
        else
            echo "❌ Не запущен"
        fi
        ;;
        
    send)
        echo "📤 Отправка текущих логов в Telegram..."
        cd ~/money-printer-parser
        source venv/bin/activate
        
        python telegram-logger.py --mode send --lines 50
        ;;
        
    monitor)
        echo "📊 Запуск мониторинга в интерактивном режиме..."
        cd ~/money-printer-parser
        source venv/bin/activate
        
        python telegram-logger.py --mode monitor --interval 30
        ;;
        
    *)
        echo "Использование: $0 {start|stop|status|send|monitor}"
        echo ""
        echo "Команды:"
        echo "  start   - Запустить логгер в фоне"
        echo "  stop    - Остановить логгер"
        echo "  status  - Показать статус"
        echo "  send    - Отправить текущие логи"
        echo "  monitor - Запустить мониторинг в интерактивном режиме"
        echo ""
        echo "Примеры:"
        echo "  $0 start    # Запуск в фоне"
        echo "  $0 send     # Отправить последние 50 строк"
        echo "  $0 monitor  # Интерактивный мониторинг"
        exit 1
        ;;
esac
