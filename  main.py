import telebot
from config import API_TOKEN
from handlers import register_handlers

# Создание экземпляра бота
bot = telebot.TeleBot(API_TOKEN)

# Регистрируем обработчики (из start.py и main_menu.py)
register_handlers(bot)

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен. Нажмите Ctrl+C для остановки.")
    bot.polling(none_stop=True)