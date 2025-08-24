import logging
from datetime import datetime
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.live import Live
from rich.layout import Layout
import config

logger = logging.getLogger(__name__)

class NewsDisplay:
    def __init__(self):
        self.console = Console()
        self.news_count = 0
        self.source_stats = {
            'telegram': 0,
            'rss': 0,
            'websocket': 0
        }
        
    def display_news(self, news_data):
        """Отображение новости с красивым форматированием"""
        try:
            self.news_count += 1
            self.source_stats[news_data['source']] += 1
            
            # Получаем иконку для источника
            icon = config.SOURCE_ICONS.get(news_data['source'], '📰')
            
            # Форматируем время
            timestamp = news_data['timestamp']
            time_str = timestamp.strftime('%H:%M:%S.%f')[:-3]  # Миллисекунды
            
            # Создаем заголовок с иконкой и временем
            header = f"{icon} {news_data['source'].upper()} | {time_str}"
            
            # Обрезаем контент для лучшего отображения
            content = news_data['content']
            if len(content) > 200:
                content = content[:200] + "..."
            
            # Создаем панель с новостью
            panel = Panel(
                Text(content, style="white"),
                title=Text(header, style="bold cyan"),
                border_style="blue",
                padding=(0, 1)
            )
            
            # Выводим статистику
            stats = self._get_stats()
            
            # Очищаем консоль и выводим новую информацию
            self.console.clear()
            self.console.print(stats)
            self.console.print(panel)
            
            # Логируем для отладки
            logger.info(f"Новость #{self.news_count} от {news_data['source']}: {content[:50]}...")
            
        except Exception as e:
            logger.error(f"Ошибка отображения новости: {e}")
    
    def _get_stats(self):
        """Создание таблицы статистики"""
        table = Table(title="📊 Статистика получения новостей")
        table.add_column("Источник", style="cyan", no_wrap=True)
        table.add_column("Количество", style="magenta", justify="right")
        table.add_column("Иконка", style="green", justify="center")
        
        for source, count in self.source_stats.items():
            icon = config.SOURCE_ICONS.get(source, '📰')
            table.add_row(source.upper(), str(count), icon)
        
        table.add_row("ВСЕГО", str(self.news_count), "📈")
        
        return table
    
    def display_startup_info(self):
        """Отображение информации о запуске"""
        self.console.print(Panel(
            "[bold green]🚀 Система мониторинга новостей BWEnews запущена![/bold green]\n\n"
            "[yellow]Мониторинг источников:[/yellow]\n"
            f"📱 Telegram: {config.TELEGRAM_CHANNEL_USERNAME}\n"
            f"📡 RSS: {config.RSS_URL}\n"
            f"🔌 WebSocket: {config.WEBSOCKET_URL}\n\n"
            "[red]Нажмите Ctrl+C для остановки[/red]",
            title="[bold blue]BWEnews Speed Test[/bold blue]",
            border_style="green"
        ))
    
    def display_error(self, error_msg):
        """Отображение ошибки"""
        self.console.print(Panel(
            f"[bold red]❌ Ошибка: {error_msg}[/bold red]",
            border_style="red"
        ))
    
    def display_shutdown(self):
        """Отображение информации о завершении"""
        self.console.print(Panel(
            f"[bold yellow]🛑 Мониторинг остановлен\n"
            f"Всего получено новостей: {self.news_count}[/bold yellow]",
            border_style="yellow"
        ))
