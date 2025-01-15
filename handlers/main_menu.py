# handlers/main_menu.py
from telebot import types
from handlers.create_sites import register_create_sites_subhandlers  # Импорт обработчиков из create_sites.py


def register_main_menu_handler(bot):
    """Регистрация обработчиков главного меню."""
    register_create_sites_subhandlers(bot)  # Регистрируем обработчики создания сайта

    @bot.callback_query_handler(func=lambda call: call.data == "main_menu")
    def handle_main_menu(call):
        """Обработка нажатия на кнопку 'Главное меню'."""
        bot.delete_message(chat_id=call.message.chat.id, message_id=call.message.id)

        # Создаём клавиатуру
        keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)
        keyboard.add(
            types.KeyboardButton("🤖 Создание ботов")
        )
        keyboard.add(
            types.KeyboardButton("📱 Создание мобильных приложений"),
        )
        keyboard.add(
            types.KeyboardButton("🌐 Создание сайтов"),  # Новая кнопка
        )
        keyboard.add(
            types.KeyboardButton("🛠 Спец. сервисы"),
            types.KeyboardButton("💎 Премиум"),
        )
        keyboard.add(types.KeyboardButton("🔙 Вернуться"))

        # Отправляем сообщение
        bot.send_message(
            chat_id=call.message.chat.id,
            text=(
                "🎉 Добро пожаловать в Главное Меню!\n\n"
                "Выберите одну из наших услуг ниже:\n\n"
                "*1.* 🤖 *Создание ботов*\n"
                "➡ Разработка чат-ботов для бизнеса и личных проектов.\n\n"
                "*2.* 📱 *Создание мобильных приложений*\n"
                "➡ Разработаем приложение под Android или iOS по вашим требованиям.\n\n"
                "*3.* 🌐 *Создание сайтов*\n"
                "➡ Создание профессиональных веб-сайтов для всех нужд.\n\n"
                "*4.* 🛠 *Спец. сервисы*\n"
                "➡ Доступ к необычным и эксклюзивным инструментам.\n\n"
                "*5.* 💎 *Премиум*\n"
                "➡ Доступ к премиум функциям и привилегиям."
            ),
            parse_mode="Markdown",
            reply_markup=keyboard,
        )

    @bot.message_handler(func=lambda message: message.text == "🌐 Создание сайтов")
    def handle_create_sites(message):
        """Обработка нажатия на кнопку 'Создание сайтов'."""
        # Создание инлайн клавиатуры для выбора типа сайта
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton("🛒 Интернет-магазин", callback_data="site_internet_shop"),
            types.InlineKeyboardButton("📷 Instagram Shop", callback_data="site_instagram_shop"),
        )
        keyboard.add(
            types.InlineKeyboardButton("🌍 Веб-сайт – о компании", callback_data="site_web_city")
        )
        keyboard.add(types.InlineKeyboardButton("🔙 Назад", callback_data="main_menu"))

        # Отправка сообщения
        bot.send_message(
            message.chat.id,
            (
                "🌐 *Создание сайтов*\n\n"
                "Выберите тип сайта, который вас интересует:\n\n"
                "🛒 Интернет-магазин — полный функционал для вашего бизнеса.\n"
                "📷 Instagram Shop — интегрированный магазин для Instagram.\n"
                "🌍 Веб-сайт – о компании — современный сайт для продвижения.\n"
            ),
            parse_mode="Markdown",
            reply_markup=keyboard,
        )