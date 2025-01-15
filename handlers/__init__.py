from .start import register_start_handler
from .main_menu import register_main_menu_handler
from .create_sites import register_create_sites_subhandlers
from .create_bots import register_create_bots_handler
from .create_apps import register_create_apps_handler
from .special_services import register_special_services_handler
from .premium import register_premium_handler
from .admin import register_admin_handler  # Импорт обработчика admin.py


def register_handlers(bot):
    """Регистрация всех обработчиков."""
    register_start_handler(bot)  # Обработчик для команды /start
    register_main_menu_handler(bot)  # Обработчик главного меню
    register_create_sites_subhandlers(bot)  # Дополнительные функции для создания сайтов
    register_create_bots_handler(bot)  # Обработчик для создания ботов
    register_create_apps_handler(bot)  # Обработчик для создания приложений
    register_special_services_handler(bot)  # Обработчик специальных сервисов
    register_premium_handler(bot)  # Обработчик премиум-функций
    register_admin_handler(bot)  # Добавляем обработчик админ-панели