from telebot import types

MANAGER_ID = 7016453953  # ID менеджера
user_manager_mapping = {}  # Словарь для связи пользователя и менеджера


def register_create_apps_handler(bot):
    """Обработчик для кнопки 'Создание мобилок'."""

    @bot.message_handler(func=lambda message: message.text == "📱 Создание мобильных приложений")
    def handle_apps_creation(message):
        """Отправка главного сообщения."""
        bot.send_message(
            message.chat.id,
            "📱 *Создание мобильных приложений:*\n\n"
            "Мы создаём мобильные приложения под Android и iOS. Полный цикл разработки:\n"
            "- Дизайн и прототипирование.\n"
            "- Разработка интерфейса.\n"
            "- Тестирование и публикация.\n\n"
            "👇 *Выберите тип вашего приложения из списка ниже:*",
            parse_mode="Markdown",
            reply_markup=create_main_inline_keyboard()
        )

    def create_main_inline_keyboard():
        """Inline-клавиатура с типами приложений."""
        keyboard = types.InlineKeyboardMarkup(row_width=1)
        buttons = [
            types.InlineKeyboardButton(text="🛒 Интернет-магазин", callback_data="app_shop"),
            types.InlineKeyboardButton(text="📚 Образовательные платформы", callback_data="app_edu"),
            types.InlineKeyboardButton(text="⚙️ Корпоративные приложения", callback_data="app_corporate"),
            types.InlineKeyboardButton(text="🎮 Игры", callback_data="app_games"),
            types.InlineKeyboardButton(text="📱 Другое", callback_data="app_other")
        ]
        keyboard.add(*buttons)
        return keyboard

    def create_back_and_order_keyboard():
        """Кнопки 'Назад' и 'Заказать услугу'."""
        keyboard = types.InlineKeyboardMarkup(row_width=2)
        keyboard.add(
            types.InlineKeyboardButton(text="⬅ Назад", callback_data="app_back"),
            types.InlineKeyboardButton(text="💼 Заказать услугу", callback_data="order_app_service")
        )
        return keyboard

    @bot.callback_query_handler(func=lambda call: call.data.startswith("app_") or call.data == "order_app_service")
    def handle_inline_app_options(call):
        """Обработка выбора опции или заказа услуги."""
        if call.data == "app_shop":
            bot.send_message(
                call.message.chat.id,
                "🛒 *Интернет-магазин*\n\n"
                "Мы разработаем удобное приложение для вашего интернет-магазина:\n"
                "- Каталог товаров.\n"
                "- Онлайн-оплата.\n"
                "- Push-уведомления.\n"
                "- Личный кабинет для клиентов.\n\n"
                "📩 Закажите услугу, если вам подходит этот тип приложения.",
                parse_mode="Markdown",
                reply_markup=create_back_and_order_keyboard()
            )
        elif call.data == "app_edu":
            bot.send_message(
                call.message.chat.id,
                "📚 *Образовательные платформы*\n\n"
                "Мы реализуем учебные приложения:\n"
                "- Онлайн-курсы.\n"
                "- Видеоуроки.\n"
                "- Систему тестирования и сертификации.\n"
                "- Уведомления о прогрессе.\n\n"
                "📩 Готовы приступить к реализации вашей идеи!",
                parse_mode="Markdown",
                reply_markup=create_back_and_order_keyboard()
            )
        elif call.data == "app_corporate":
            bot.send_message(
                call.message.chat.id,
                "⚙️ *Корпоративные приложения*\n\n"
                "Оптимизируйте процессы в вашем бизнесе с помощью:\n"
                "- Систем управления задачами.\n"
                "- Внедрения CRM-решений.\n"
                "- Интеграции с базами данных.\n"
                "- Инструментов для внутреннего общения.\n\n"
                "📩 Готовы реализовать ваш проект — нажмите \"Заказать услугу\".",
                parse_mode="Markdown",
                reply_markup=create_back_and_order_keyboard()
            )
        elif call.data == "app_games":
            bot.send_message(
                call.message.chat.id,
                "🎮 *Игры*\n\n"
                "Мы создаём игры:\n"
                "- Mobile-игры 2D и 3D.\n"
                "- Многопользовательские игры.\n"
                "- Интеграция с социальными сетями.\n\n"
                "📩 Начните процесс создания игры с нами!",
                parse_mode="Markdown",
                reply_markup=create_back_and_order_keyboard()
            )
        elif call.data == "app_other":
            bot.send_message(
                call.message.chat.id,
                "📱 *Другие виды приложений*\n\n"
                "Не нашли подходящий вариант? Мы также берёмся за:\n"
                "- Финансовые приложения.\n"
                "- Приложения для здоровья и фитнеса.\n"
                "- Социальные сети.\n"
                "- Любые кастомные решения.\n\n"
                "📩 Напишите ваше ТЗ, и мы обсудим ваш проект.",
                parse_mode="Markdown",
                reply_markup=create_back_and_order_keyboard()
            )
        elif call.data == "app_back":
            bot.send_message(
                call.message.chat.id,
                "⬅ *Главное меню мобильных приложений*:\n\n"
                "Выберите подходящий тип приложения ниже:",
                parse_mode="Markdown",
                reply_markup=create_main_inline_keyboard()
            )
        elif call.data == "order_app_service":
            bot.send_message(
                call.message.chat.id,
                "📝 *Введите ваш запрос (ТЗ) для мобильного приложения.*\n\n"
                "Опишите ваши требования и идеи, чтобы наш менеджер мог с вами связаться.",
                parse_mode="Markdown"
            )
            bot.register_next_step_handler_by_chat_id(call.message.chat.id, handle_user_tz_submission)

    def handle_user_tz_submission(message):
        """Обработка ТЗ пользователя."""
        user_tz = message.text
        user_manager_mapping[MANAGER_ID] = message.chat.id  # Привязываем ID пользователя к менеджеру
        bot.send_message(
            chat_id=message.chat.id,
            text="✅ *Ваш запрос отправлен менеджеру!*\n"
                 "Ожидайте, он скоро свяжется с вами.",
            parse_mode="Markdown"
        )
        # Сообщение менеджеру с кнопкой "Ответить"
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton(text="✏️ Ответить", callback_data=f"reply_to_user_{message.chat.id}"))

        bot.send_message(
            chat_id=MANAGER_ID,
            text=f"📩 *Новый запрос на мобильное приложение:*\n"
                 f"👤 Пользователь: @{message.from_user.username or 'Нет ника'}\n"
                 f"💬 Текст ТЗ:\n{user_tz}",
            reply_markup=keyboard,
            parse_mode="Markdown"
        )

    @bot.callback_query_handler(func=lambda call: call.data.startswith("reply_to_user_"))
    def handle_reply_to_user(call):
        """Обработка ответа менеджера пользователю."""
        user_id = int(call.data.split("_")[-1])  # Извлечение ID пользователя из callback_data
        bot.send_message(
            chat_id=call.message.chat.id,
            text="✉️ *Введите текст ответа для пользователя.*",
            parse_mode="Markdown"
        )
        bot.register_next_step_handler_by_chat_id(call.message.chat.id, send_reply_to_user, user_id)

    def send_reply_to_user(message, user_id):
        """Отправка ответа менеджера пользователю."""
        # Менеджер отправляет сообщение напрямую пользователю по его ID
        bot.send_message(
            chat_id=user_id,
            text=f"📩 *Ответ от менеджера:*\n{message.text}",
            parse_mode="Markdown"
        )
        bot.send_message(
            chat_id=MANAGER_ID,
            text="✅ Сообщение отправлено пользователю.",
            parse_mode="Markdown"
        )